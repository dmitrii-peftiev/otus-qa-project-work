import allure
from playwright.sync_api import expect

from src.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    CHECKOUT_BTN = "[data-test='checkout']"

    def get_items_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def wait_for_items_count(self, count: int) -> None:
        expect(self.page.locator(self.CART_ITEM)).to_have_count(count)

    def remove_item(self, item_name: str) -> None:
        with allure.step(f"Remove '{item_name}' from cart"):
            item_card = self.page.locator(self.CART_ITEM).filter(has_text=item_name)
            item_card.locator("button:has-text('Remove')").click()

    def click_checkout(self) -> None:
        self.click(self.CHECKOUT_BTN)
