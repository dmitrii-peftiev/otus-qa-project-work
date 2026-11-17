import time

import allure
import pytest

from src.api.endpoints import Endpoints
from src.api.schemas import ResourcesListResponse, SingleResourceResponse


@allure.feature("API: Resources")
@pytest.mark.api
class TestResources:
    @allure.title("Get list of resources")
    def test_get_resources_list(self, api_client):
        response = api_client.get(Endpoints.RESOURCES)

        with allure.step("Check status code 200 and items count"):
            assert response.status_code == 200
            data = ResourcesListResponse(**response.json())
            assert len(data.data) == 6

    @allure.title("Get single resource by id {resource_id}")
    @pytest.mark.parametrize(
        "resource_id, name",
        [
            (1, "cerulean"),
            (2, "fuchsia rose"),
            (3, "true red"),
        ],
    )
    def test_get_single_resource(self, api_client, resource_id, name):
        response = api_client.get(Endpoints.resource_by_id(resource_id))

        with allure.step("Check status code 200 and resource name"):
            assert response.status_code == 200
            data = SingleResourceResponse(**response.json())
            assert data.data.name == name

    @allure.title("Get non-existent resource returns 404")
    def test_get_resource_not_found(self, api_client):
        response = api_client.get(Endpoints.resource_by_id(23))

        with allure.step("Check status code 404"):
            assert response.status_code == 404
            assert response.json() == {}

    @allure.title("Check delayed response")
    def test_delayed_response(self, api_client):
        start = time.perf_counter()
        response = api_client.get(Endpoints.USERS, params={"delay": 2})
        duration = time.perf_counter() - start

        with allure.step("Check status code 200 and delay >= 2 seconds"):
            assert response.status_code == 200
            assert duration >= 2.0
