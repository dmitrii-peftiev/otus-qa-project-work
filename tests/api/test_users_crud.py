import allure
import pytest

from src.api.endpoints import Endpoints
from src.api.schemas import (
    CreateUserResponse,
    SingleUserResponse,
    UpdateUserResponse,
    UsersListResponse,
)
from src.utils.data_generator import get_random_user


@allure.feature("API: Users")
@pytest.mark.api
class TestUsersCrud:
    @allure.title("Get users list on page {page}")
    @pytest.mark.parametrize("page", [1, 2])
    def test_get_users_list(self, api_client, page):
        response = api_client.get(Endpoints.USERS, params={"page": page})

        with allure.step("Check status code 200 and response body"):
            assert response.status_code == 200
            data = UsersListResponse(**response.json())
            assert data.page == page
            assert len(data.data) > 0

    @allure.title("Get single user by id {user_id}")
    @pytest.mark.parametrize(
        "user_id, email",
        [
            (1, "george.bluth@reqres.in"),
            (2, "janet.weaver@reqres.in"),
            (3, "emma.wong@reqres.in"),
        ],
    )
    def test_get_single_user(self, api_client, user_id, email):
        response = api_client.get(Endpoints.user_by_id(user_id))

        with allure.step("Check status code 200 and user email"):
            assert response.status_code == 200
            data = SingleUserResponse(**response.json())
            assert data.data.id == user_id
            assert data.data.email == email

    @allure.title("Get non-existent user returns 404 (id={user_id})")
    @pytest.mark.parametrize("user_id", [23, 999])
    def test_get_user_not_found(self, api_client, user_id):
        response = api_client.get(Endpoints.user_by_id(user_id))

        with allure.step("Check status code 404"):
            assert response.status_code == 404
            assert response.json() == {}

    @allure.title("Create new user")
    def test_create_user(self, api_client):
        payload = get_random_user()
        response = api_client.post(Endpoints.USERS, json_data=payload)

        with allure.step("Check status code 201 and created fields"):
            assert response.status_code == 201
            data = CreateUserResponse(**response.json())
            assert data.name == payload["name"]
            assert data.job == payload["job"]

    @allure.title("Update user with PUT")
    def test_update_user_put(self, api_client):
        payload = get_random_user()
        response = api_client.put(Endpoints.user_by_id(2), json_data=payload)

        with allure.step("Check status code 200 and updated fields"):
            assert response.status_code == 200
            data = UpdateUserResponse(**response.json())
            assert data.name == payload["name"]
            assert data.job == payload["job"]

    @allure.title("Update user with PATCH")
    def test_update_user_patch(self, api_client):
        payload = {"job": "QA Engineer"}
        response = api_client.patch(Endpoints.user_by_id(2), json_data=payload)

        with allure.step("Check status code 200 and updated job"):
            assert response.status_code == 200
            data = UpdateUserResponse(**response.json())
            assert data.job == payload["job"]

    @allure.title("Delete user")
    def test_delete_user(self, api_client):
        response = api_client.delete(Endpoints.user_by_id(2))

        with allure.step("Check status code 204"):
            assert response.status_code == 204
            assert response.text == ""
