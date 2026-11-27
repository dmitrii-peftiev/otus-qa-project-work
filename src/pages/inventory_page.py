import allure

from src.pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = ".title"
    SORT_SELECT = "[data-test='product-sort-container']"
    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAMES = ".inventory_item_name"
    ITEM_PRICES = ".inventory_item_price"
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

    def _get_item_card(self, item_name: str):
        return self.page.locator(self.INVENTORY_ITEM).filter(has_text=item_name)

    def get_item_price(self, item_name: str) -> float:
        price_text = (
            self._get_item_card(item_name).locator(self.ITEM_PRICES).inner_text()
        )
        return float(price_text.replace("$", ""))

    def add_item_to_cart(self, item_name: str) -> None:
        with allure.step(f"Add '{item_name}' to cart"):
            self._get_item_card(item_name).locator(
                "button:has-text('Add to cart')"
            ).click()

    def remove_item_from_cart(self, item_name: str) -> None:
        with allure.step(f"Remove '{item_name}' from cart"):
            self._get_item_card(item_name).locator("button:has-text('Remove')").click()

    def get_cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def logout(self) -> None:
        with allure.step("Logout from application"):
            self.click(self.BURGER_MENU_BTN)
            self.expect_visible(self.LOGOUT_LINK)
            self.click(self.LOGOUT_LINK)
