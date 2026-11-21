from playwright.sync_api import expect

from src.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = ".cart_item"
    REMOVE_BACKPACK_BTN = "[data-test='remove-sauce-labs-backpack']"
    CHECKOUT_BTN = "[data-test='checkout']"

    def get_items_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def wait_for_items_count(self, count: int) -> None:
        expect(self.page.locator(self.CART_ITEM)).to_have_count(count)

    def remove_backpack(self) -> None:
        self.click(self.REMOVE_BACKPACK_BTN)

    def click_checkout(self) -> None:
        self.click(self.CHECKOUT_BTN)
