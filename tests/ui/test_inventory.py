import allure
import pytest

from src.pages.inventory_page import InventoryPage


@allure.feature("UI: Inventory & Sorting")
@pytest.mark.ui
class TestInventory:
    @allure.title("Sort products by price: {sort_type}")
    @pytest.mark.parametrize(
        "sort_type, reverse",
        [
            ("lohi", False),
            ("hilo", True),
        ],
    )
    def test_sort_by_price(self, logged_in_page, sort_type, reverse):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.select_sort(sort_type)

        with allure.step("Check prices are sorted properly"):
            prices = inventory_page.get_all_prices()
            assert prices == sorted(prices, reverse=reverse)

    @allure.title("Sort products by name: {sort_type}")
    @pytest.mark.parametrize(
        "sort_type, reverse",
        [
            ("az", False),
            ("za", True),
        ],
    )
    def test_sort_by_name(self, logged_in_page, sort_type, reverse):
        inventory_page = InventoryPage(logged_in_page)
        inventory_page.select_sort(sort_type)

        with allure.step("Check product names are sorted properly"):
            names = inventory_page.get_all_names()
            assert names == sorted(names, reverse=reverse)
