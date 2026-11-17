import json

import allure
import requests

from src.utils.config import config


def attach_logs(response: requests.Response) -> None:
    request_text = (
        f"Method: {response.request.method}\n"
        f"URL: {response.request.url}\n"
        f"Body: {response.request.body}"
    )
    allure.attach(
        request_text, name="Request", attachment_type=allure.attachment_type.TEXT
    )

    try:
        response_text = json.dumps(response.json(), indent=4)
        file_type = allure.attachment_type.JSON
    except ValueError:
        response_text = response.text or "Empty response"
        file_type = allure.attachment_type.TEXT

    allure.attach(
        f"Status: {response.status_code}\n\n{response_text}",
        name="Response",
        attachment_type=file_type,
    )


class ApiClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.session = requests.Session()
        if config.API_KEY:
            self.session.headers.update({"x-api-key": config.API_KEY})

    def send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
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
