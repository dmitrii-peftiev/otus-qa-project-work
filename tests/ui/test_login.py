import allure
import pytest

from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage
from src.utils.config import config


@allure.feature("UI: Login")
@pytest.mark.ui
class TestLogin:
    @allure.title("Successful login with standard user")
    def test_valid_login(self, page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)

        login_page.open_login_page()
        login_page.login(config.STANDARD_USER, config.USER_PASSWORD)

        with allure.step("Check Products page is opened"):
            assert inventory_page.get_title() == "Products"

    @allure.title("Login fails for locked out user")
    def test_locked_user_login(self, page):
        login_page = LoginPage(page)

        login_page.open_login_page()
        login_page.login(config.LOCKED_USER, config.USER_PASSWORD)

        with allure.step("Check locked out error message"):
            assert "Sorry, this user has been locked out" in login_page.get_error_text()

    @allure.title("Login fails with invalid credentials: {case}")
    @pytest.mark.parametrize(
        "case, username, password, expected_error",
        [
            (
                "Wrong password",
                "standard_user",
                "wrong_pass",
                "Username and password do not match",
            ),
            ("Empty username", "", "secret_sauce", "Username is required"),
            ("Empty password", "standard_user", "", "Password is required"),
        ],
    )
    def test_invalid_login(self, page, case, username, password, expected_error):
        login_page = LoginPage(page)

        login_page.open_login_page()
        login_page.login(username, password)

        with allure.step("Check validation error text"):
            assert expected_error in login_page.get_error_text()
