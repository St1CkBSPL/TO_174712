"""Shared Selenium fixtures for the SklepTO test suite."""

from __future__ import annotations

import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


SKLEPTO_URL = os.getenv("SKLEPTO_URL", "http://localhost/sklepto").rstrip("/")
WAIT_SECONDS = float(os.getenv("SKLEPTO_WAIT_SECONDS", "5"))


def reset_database(driver: webdriver.Chrome) -> None:
    """Restore the initial users and orders described in Appendix A."""
    driver.get(f"{SKLEPTO_URL}/install.php?reset=1")
    status = WebDriverWait(driver, WAIT_SECONDS).until(
        lambda current_driver: current_driver.find_element(By.ID, "install-status")
    )
    assert status.text == "OK", "Database reset failed - is MySQL running?"
    driver.delete_all_cookies()


@pytest.fixture(scope="session")
def driver():
    """Use one Chrome instance for the complete test session."""
    options = webdriver.ChromeOptions()
    if os.getenv("SKLEPTO_HEADLESS", "1") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-search-engine-choice-screen")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    reset_database(browser)
    yield browser
    browser.quit()


@pytest.fixture(autouse=True)
def logged_out(driver):
    """Start every test with a fresh, logged-out PHP session."""
    driver.delete_all_cookies()


@pytest.fixture
def clean_db(driver):
    """Reset mutable application data immediately before a test."""
    reset_database(driver)
