import allure
import pytest

from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.inventory_page import InventoryPage
from src.pages.login_page import LoginPage
from src.utils.data_generator import get_random_checkout_info


@allure.feature("UI: Cart & Checkout")
@pytest.mark.ui
class TestCheckout:
    @allure.title("Add and remove item from cart")
    def test_add_and_remove_item(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        cart_page = CartPage(logged_in_page)

        inventory_page.add_backpack_to_cart()
        with allure.step("Check item is added to cart"):
            assert inventory_page.get_cart_count() == 1

        inventory_page.go_to_cart()
        with allure.step("Check cart has 1 item and remove it"):
            cart_page.wait_for_items_count(1)
            cart_page.remove_backpack()
            cart_page.wait_for_items_count(0)

    @allure.title("Complete end-to-end order flow")
    def test_full_checkout_flow(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        checkout_page = CheckoutPage(logged_in_page)
        customer = get_random_checkout_info()

        inventory_page.add_backpack_to_cart()
        inventory_page.go_to_cart()
        cart_page.click_checkout()

        checkout_page.fill_customer_info(
            customer["first_name"], customer["last_name"], customer["postal_code"]
        )
        checkout_page.finish_checkout()

        with allure.step("Check order completion message"):
            assert checkout_page.get_complete_message() == "Thank you for your order!"

    @allure.title("Checkout fails with empty customer info")
    def test_checkout_empty_fields(self, logged_in_page):
        inventory_page = InventoryPage(logged_in_page)
        cart_page = CartPage(logged_in_page)
        checkout_page = CheckoutPage(logged_in_page)

        inventory_page.add_backpack_to_cart()
        inventory_page.go_to_cart()
        cart_page.click_checkout()

        checkout_page.fill_customer_info("", "", "")

        with allure.step("Check validation error message"):
            assert "First Name is required" in checkout_page.get_error_text()

    @allure.title("Logout from application")
    def test_logout(self, logged_in_page):
        login_page = LoginPage(logged_in_page)
        inventory_page = InventoryPage(logged_in_page)

        inventory_page.logout()

        with allure.step("Check login button is visible again"):
            assert login_page.is_login_button_visible()
