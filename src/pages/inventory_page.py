import allure

from src.pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = ".title"
    SORT_SELECT = "[data-test='product-sort-container']"
    ITEM_NAMES = ".inventory_item_name"
    ITEM_PRICES = ".inventory_item_price"
    ADD_BACKPACK_BTN = "[data-test='add-to-cart-sauce-labs-backpack']"
    REMOVE_BACKPACK_BTN = "[data-test='remove-sauce-labs-backpack']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    BURGER_MENU_BTN = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def get_title(self) -> str:
        return self.get_text(self.TITLE)

    def select_sort(self, value: str) -> None:
        with allure.step(f"Sort products by '{value}'"):
            self.page.locator(self.SORT_SELECT).select_option(value)

    def get_all_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    def get_all_prices(self) -> list[float]:
        texts = self.page.locator(self.ITEM_PRICES).all_inner_texts()
        return [float(price.replace("$", "")) for price in texts]

    def add_backpack_to_cart(self) -> None:
        self.click(self.ADD_BACKPACK_BTN)

    def remove_backpack_from_cart(self) -> None:
        self.click(self.REMOVE_BACKPACK_BTN)

    def get_cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def logout(self) -> None:
        with allure.step("Logout from application"):
            self.click(self.BURGER_MENU_BTN)
            self.page.locator(self.LOGOUT_LINK).wait_for(state="visible")
            self.click(self.LOGOUT_LINK)
