import allure
import pytest

from src.api.endpoints import Endpoints
from src.api.schemas import ErrorResponse, LoginSuccessResponse, RegisterSuccessResponse
from src.utils.data_generator import get_random_password


@allure.feature("API: Auth")
@pytest.mark.api
class TestAuth:
    @allure.title("Successful registration")
    def test_register_success(self, api_client):
        payload = {"email": "eve.holt@reqres.in", "password": get_random_password()}
        response = api_client.post(Endpoints.REGISTER, json_data=payload)

        with allure.step("Check status code 200 and token"):
            assert response.status_code == 200
            data = RegisterSuccessResponse(**response.json())
            assert data.id > 0
            assert data.token != ""

    @allure.title("Failed registration: {case}")
    @pytest.mark.parametrize(
        "case, payload, error_text",
        [
            ("No password", {"email": "sydney@fife"}, "Missing password"),
            ("No email", {"password": "pistol"}, "Missing email or username"),
            ("Empty body", {}, "Missing email or username"),
        ],
    )
    def test_register_fail(self, api_client, case, payload, error_text):
        response = api_client.post(Endpoints.REGISTER, json_data=payload)

        with allure.step("Check status code 400 and error text"):
            assert response.status_code == 400
            data = ErrorResponse(**response.json())
            assert data.error == error_text

    @allure.title("Successful login")
    def test_login_success(self, api_client):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = api_client.post(Endpoints.LOGIN, json_data=payload)

        with allure.step("Check status code 200 and token"):
            assert response.status_code == 200
            data = LoginSuccessResponse(**response.json())
            assert data.token != ""

    @allure.title("Failed login: {case}")
    @pytest.mark.parametrize(
        "case, payload, error_text",
        [
            ("No password", {"email": "peter@klaven"}, "Missing password"),
            ("No email", {"password": "cityslicka"}, "Missing email or username"),
            (
                "Unknown user",
                {"email": "nobody@reqres.in", "password": "123"},
                "user not found",
            ),
        ],
    )
    def test_login_fail(self, api_client, case, payload, error_text):
        response = api_client.post(Endpoints.LOGIN, json_data=payload)

        with allure.step("Check status code 400 and error text"):
            assert response.status_code == 400
            data = ErrorResponse(**response.json())
            assert data.error == error_text
