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

    ITEM_NAME = ".inventory_item_name"
    ITEM_QTY = ".cart_quantity"
    ITEM_PRICE = ".inventory_item_price"
    SUBTOTAL_LABEL = ".summary_subtotal_label"
    TAX_LABEL = ".summary_tax_label"
    TOTAL_LABEL = ".summary_total_label"

    def fill_customer_info(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        with allure.step("Fill checkout customer info"):
            self.fill(self.FIRST_NAME_INPUT, first_name)
            self.fill(self.LAST_NAME_INPUT, last_name)
            self.fill(self.POSTAL_CODE_INPUT, postal_code)
            self.click(self.CONTINUE_BTN)

    def get_overview_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def get_overview_item_quantities(self) -> list[int]:
        return [int(q) for q in self.page.locator(self.ITEM_QTY).all_inner_texts()]

    def get_overview_item_prices(self) -> list[float]:
        texts = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in texts]

    def get_subtotal(self) -> float:
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.split("$")[1])

    def get_tax(self) -> float:
        text = self.get_text(self.TAX_LABEL)
        return float(text.split("$")[1])

    def get_total(self) -> float:
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.split("$")[1])

    def finish_checkout(self) -> None:
        self.click(self.FINISH_BTN)

    def get_complete_message(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
