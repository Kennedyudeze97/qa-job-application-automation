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

    # Only after the test body runs, and only on failures
    if rep.when != "call" or rep.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    import pathlib
    from datetime import datetime
    from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

    artifacts_dir = pathlib.Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{item.name}_{timestamp}"

    screenshot_path = artifacts_dir / f"{name}.png"
    html_path = artifacts_dir / f"{name}.html"
    alert_path = artifacts_dir / f"{name}.alert.txt"

    # If an alert is open, record it and try to close it so screenshot works
    try:
        alert = driver.switch_to.alert
        alert_path.write_text((alert.text or ""), encoding="utf-8")
        try:
            alert.accept()
        except Exception:
            pass
    except NoAlertPresentException:
        pass
    except Exception:
        pass

    # Screenshot (guard against alerts blocking webdriver commands)
    try:
        driver.save_screenshot(str(screenshot_path))
    except UnexpectedAlertPresentException:
        try:
            alert = driver.switch_to.alert
            alert_path.write_text((alert.text or ""), encoding="utf-8")
            alert.accept()
            driver.save_screenshot(str(screenshot_path))
        except Exception:
            pass
    except Exception:
        pass

    # HTML dump
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception:
        pass

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
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when != "call" or rep.passed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    artifacts_dir = pathlib.Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{item.name}_{timestamp}"

    screenshot_path = artifacts_dir / f"{name}.png"
    html_path = artifacts_dir / f"{name}.html"
    alert_path = artifacts_dir / f"{name}.alert.txt"

    # If an alert is open, record it and try to close it so screenshot works
    try:
        alert = driver.switch_to.alert
        text = alert.text or ""
        alert_path.write_text(text, encoding="utf-8")
        try:
            alert.accept()
        except Exception:
            pass
    except NoAlertPresentException:
        pass
    except Exception:
        # don't let artifact collection crash pytest
        pass

    # Screenshot (guard against alerts blocking webdriver commands)
    try:
        driver.save_screenshot(str(screenshot_path))
    except UnexpectedAlertPresentException:
        # Try once more after accepting the alert
        try:
            alert = driver.switch_to.alert
            alert_path.write_text((alert.text or ""), encoding="utf-8")
            alert.accept()
            driver.save_screenshot(str(screenshot_path))
        except Exception:
            pass
    except Exception:
        pass

    # HTML dump
    try:
        html_path.write_text(driver.page_source, encoding="utf-8")
    except Exception:
        pass

