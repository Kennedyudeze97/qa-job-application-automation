import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()

    # Headless only in CI
    if os.getenv("CI", "").lower() == "true":
        options.add_argument("--headless=new")

    # Stability flags for Linux runners
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

