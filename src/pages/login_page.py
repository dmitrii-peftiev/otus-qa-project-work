import allure

from src.pages.base_page import BasePage
from src.utils.config import config


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def open_login_page(self) -> None:
        self.open(config.UI_BASE_URL)

    def login(self, username: str, password: str) -> None:
        with allure.step(f"Login as '{username}'"):
            self.fill(self.USERNAME_INPUT, username)
            self.fill(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_button_visible(self) -> bool:
        self.page.locator(self.LOGIN_BUTTON).wait_for(state="visible")
        return self.is_visible(self.LOGIN_BUTTON)
