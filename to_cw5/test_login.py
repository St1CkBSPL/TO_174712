"""Tests for login, logout, and account locking."""

import pytest
from selenium.webdriver.common.by import By

from helpers import log_in, open_page, wait_for


def test_valid_login_changes_menu(driver, clean_db):
    """REQ-LOG-02, REQ-UI-01"""
    message = log_in(driver)
    assert message.text == "Zalogowano jako jan."
    assert "index.php" in driver.current_url
    assert driver.find_element(By.ID, "zalogowany").text == "Zalogowano: jan"
    assert driver.find_element(By.ID, "nav-wyloguj").text == "Wyloguj"
    assert not driver.find_elements(By.ID, "nav-logowanie")


@pytest.mark.parametrize(
    ("login", "password", "expected"),
    [
        ("jan", "wrong", "Błędny login lub hasło. Pozostało prób: 2."),
        ("unknown", "Haslo123", "Błędny login lub hasło."),
        (
            "zablokowany",
            "Haslo123",
            "Konto jest zablokowane. Skontaktuj się z administratorem.",
        ),
        ("", "", "Błędny login lub hasło."),
    ],
)
def test_invalid_login_classes(driver, clean_db, login, password, expected):
    """REQ-LOG-03, REQ-LOG-05, REQ-LOG-06"""
    assert log_in(driver, login, password).text == expected


def test_logout_ends_session(driver, clean_db):
    """REQ-LOG-07"""
    log_in(driver)
    driver.find_element(By.ID, "nav-wyloguj").click()
    assert wait_for(driver, By.ID, "flash").text == "Wylogowano."
    assert driver.find_elements(By.ID, "nav-logowanie")
    assert not driver.find_elements(By.ID, "zalogowany")


def test_flash_message_is_styled_and_disappears_after_refresh(driver, clean_db):
    """REQ-UI-06"""
    flash = log_in(driver)
    assert "success" in flash.get_attribute("class").split()
    driver.refresh()
    assert not driver.find_elements(By.ID, "flash")


def test_third_wrong_password_locks_account_in_admin_panel(driver, clean_db):
    """REQ-LOG-03, REQ-LOG-04, REQ-LOG-08"""
    assert log_in(driver, "jan", "wrong").text.endswith("Pozostało prób: 2.")
    assert log_in(driver, "jan", "wrong").text.endswith("Pozostało prób: 1.")
    assert (
        log_in(driver, "jan", "wrong").text
        == "Konto zostało zablokowane po 3 nieudanych próbach."
    )

    open_page(driver, "admin.php", By.CSS_SELECTOR, 'tr[data-login="jan"]')
    row = driver.find_element(By.CSS_SELECTOR, 'tr[data-login="jan"]')
    assert row.find_element(By.CLASS_NAME, "proby").text == "3"
    assert row.find_element(By.CLASS_NAME, "status").text == "LOCKED"
    assert row.find_element(By.CLASS_NAME, "odblokuj").text == "Odblokuj"


@pytest.mark.xfail(reason="DEF-07", strict=True)
def test_successful_login_resets_failed_attempt_counter(driver, clean_db):
    """REQ-LOG-02"""
    log_in(driver, "jan", "wrong")
    log_in(driver, "jan", "Haslo123")
    open_page(driver, "admin.php", By.CSS_SELECTOR, 'tr[data-login="jan"]')
    row = driver.find_element(By.CSS_SELECTOR, 'tr[data-login="jan"]')
    assert row.find_element(By.CLASS_NAME, "proby").text == "0"


def test_unlock_changes_status_and_resets_counter(driver, clean_db):
    """REQ-LOG-09"""
    open_page(
        driver, "admin.php", By.CSS_SELECTOR, 'tr[data-login="zablokowany"]'
    )
    row = driver.find_element(By.CSS_SELECTOR, 'tr[data-login="zablokowany"]')
    row.find_element(By.CLASS_NAME, "odblokuj").click()
    assert wait_for(driver, By.ID, "flash").text == (
        "Odblokowano konto zablokowany."
    )
    row = driver.find_element(By.CSS_SELECTOR, 'tr[data-login="zablokowany"]')
    assert row.find_element(By.CLASS_NAME, "proby").text == "0"
    assert row.find_element(By.CLASS_NAME, "status").text == "ACTIVE"
    assert not row.find_elements(By.CLASS_NAME, "odblokuj")
