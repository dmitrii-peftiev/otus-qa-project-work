import json
from typing import Any

import allure
import requests

from src.utils.config import config

SENSITIVE_KEYS = {"password", "token", "api_key", "x-api-key"}


def _mask_body(body: Any) -> str:
    if not body:
        return "None"
    try:
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        data = json.loads(body) if isinstance(body, str) else body
        if isinstance(data, dict):
            masked = {
                k: "***" if k.lower() in SENSITIVE_KEYS else v for k, v in data.items()
            }
            return json.dumps(masked, indent=4, ensure_ascii=False)
    except (ValueError, TypeError):
        pass
    return str(body)


def attach_logs(response: requests.Response) -> None:
    masked_request_body = _mask_body(response.request.body)
    request_text = (
        f"Method: {response.request.method}\n"
        f"URL: {response.request.url}\n"
        f"Body:\n{masked_request_body}"
    )
    allure.attach(
        request_text, name="Request", attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        str(response.status_code),
        name="Response Status",
        attachment_type=allure.attachment_type.TEXT,
    )

    try:
        response_text = json.dumps(response.json(), indent=4, ensure_ascii=False)
        file_type = allure.attachment_type.JSON
    except ValueError:
        response_text = response.text or "Empty response"
        file_type = allure.attachment_type.TEXT

    allure.attach(
        response_text,
        name="Response Body",
        attachment_type=file_type,
    )


class ApiClient:
    def __init__(self, timeout: int = config.API_TIMEOUT):
        self.base_url = config.API_BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
        if config.API_KEY:
            self.session.headers.update({"x-api-key": config.API_KEY})

    def send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        with allure.step(f"Send {method} request to {endpoint}"):
            response = self.session.request(method=method, url=url, **kwargs)
            attach_logs(response)
            return response

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        return self.send_request("GET", endpoint, params=params)

    def post(self, endpoint: str, json_data: dict | None = None) -> requests.Response:
        return self.send_request("POST", endpoint, json=json_data)

    def put(self, endpoint: str, json_data: dict | None = None) -> requests.Response:
        return self.send_request("PUT", endpoint, json=json_data)

    def patch(self, endpoint: str, json_data: dict | None = None) -> requests.Response:
        return self.send_request("PATCH", endpoint, json=json_data)

    def delete(self, endpoint: str) -> requests.Response:
        return self.send_request("DELETE", endpoint)

    def close(self) -> None:
        self.session.close()
