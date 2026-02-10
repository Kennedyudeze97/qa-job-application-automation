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

import pathlib
from datetime import datetime
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or rep.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    artifacts = pathlib.Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{item.name}_{ts}"

    driver.save_screenshot(str(artifacts / f"{name}.png"))
    (artifacts / f"{name}.html").write_text(driver.page_source, encoding="utf-8")

import pathlib
from datetime import datetime
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Only act after the test body runs
    if rep.when != "call":
        return

    # Only capture artifacts on failure
    if rep.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    artifacts_dir = pathlib.Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = item.name

    screenshot_path = artifacts_dir / f"{test_name}_{timestamp}.png"
    html_path = artifacts_dir / f"{test_name}_{timestamp}.html"

    driver.save_screenshot(str(screenshot_path))

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

