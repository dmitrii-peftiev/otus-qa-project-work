import allure
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        with allure.step(f"Open URL: {url}"):
            self.page.goto(url)

    def click(self, locator: str) -> None:
        with allure.step(f"Click element: {locator}"):
            self.page.locator(locator).click()

    def fill(self, locator: str, text: str, mask: bool = False) -> None:
        display_text = "***" if mask else text
        with allure.step(f"Fill '{locator}' with '{display_text}'"):
            self.page.locator(locator).fill(text)

    def get_text(self, locator: str) -> str:
        return self.page.locator(locator).inner_text()

    def expect_visible(self, locator: str) -> None:
        expect(self.page.locator(locator)).to_be_visible()

    def is_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()
