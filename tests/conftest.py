from collections.abc import Generator
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, sync_playwright

from src.api.client import ApiClient
from src.pages.login_page import LoginPage
from src.utils.config import config


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    return ApiClient()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=config.HEADLESS, args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser, request) -> Generator[Page, Any, None]:
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.set_default_timeout(10000)
    try:
        yield page
    finally:
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name=f"screenshot_{request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )
        context.close()


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    login_page = LoginPage(page)
    login_page.open_login_page()
    login_page.login(config.STANDARD_USER, config.USER_PASSWORD)
    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
