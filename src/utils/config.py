import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://reqres.in/api")
    API_KEY = os.getenv("API_KEY", "")

    UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.saucedemo.com")
    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
    USER_PASSWORD = os.getenv("USER_PASSWORD", "secret_sauce")
    HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"


config = Config()
