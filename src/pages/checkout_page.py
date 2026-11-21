import allure

from src.pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BTN = "[data-test='continue']"
    FINISH_BTN = "[data-test='finish']"
    COMPLETE_HEADER = ".complete-header"
    ERROR_MESSAGE = "[data-test='error']"

    def fill_customer_info(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        with allure.step("Fill checkout customer info"):
            self.fill(self.FIRST_NAME_INPUT, first_name)
            self.fill(self.LAST_NAME_INPUT, last_name)
            self.fill(self.POSTAL_CODE_INPUT, postal_code)
            self.click(self.CONTINUE_BTN)

    def finish_checkout(self) -> None:
        self.click(self.FINISH_BTN)

    def get_complete_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
