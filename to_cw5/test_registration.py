"""Tests for account registration and server-side validation."""

import pytest
from selenium.webdriver.common.by import By

from helpers import log_in, open_page, wait_for


def submit_registration(
    driver,
    *,
    login,
    email,
    age,
    password,
    repeated_password,
    accept_terms,
):
    """Fill and submit the registration form."""
    open_page(driver, "rejestracja.php", By.ID, "form-rejestracja")
    values = {
        "login": login,
        "email": email,
        "wiek": age,
        "haslo": password,
        "haslo2": repeated_password,
    }
    for field_id, value in values.items():
        driver.find_element(By.ID, field_id).send_keys(str(value))
    if accept_terms:
        driver.find_element(By.ID, "regulamin").click()
    driver.find_element(By.ID, "zarejestruj").click()
    wait_for(driver, By.CSS_SELECTOR, "#bledy, #sukces")


def test_empty_registration_reports_all_field_errors(driver, clean_db):
    """REQ-REJ-02, REQ-REJ-04 - REQ-REJ-09"""
    submit_registration(
        driver,
        login="",
        email="",
        age="",
        password="",
        repeated_password="different",
        accept_terms=False,
    )
    errors = driver.find_elements(By.CSS_SELECTOR, "#bledy li.blad")
    assert [error.get_attribute("data-pole") for error in errors] == [
        "login",
        "email",
        "wiek",
        "haslo",
        "haslo2",
        "regulamin",
    ]


def test_invalid_registration_preserves_plain_fields(driver, clean_db):
    """REQ-REJ-09"""
    submit_registration(
        driver,
        login="ab",
        email="invalid",
        age="17",
        password="short",
        repeated_password="other",
        accept_terms=False,
    )
    assert driver.find_element(By.ID, "login").get_attribute("value") == "ab"
    assert driver.find_element(By.ID, "email").get_attribute("value") == "invalid"
    assert driver.find_element(By.ID, "wiek").get_attribute("value") == "17"


@pytest.mark.xfail(reason="DEF-05", strict=True)
def test_uppercase_login_is_rejected(driver, clean_db):
    """REQ-REJ-02"""
    submit_registration(
        driver,
        login="User123",
        email="user@example.com",
        age="25",
        password="Password1",
        repeated_password="Password1",
        accept_terms=True,
    )
    assert driver.find_element(By.CSS_SELECTOR, '[data-pole="login"]').text == (
        "Login musi mieć od 3 do 20 znaków (małe litery, cyfry, _)."
    )


@pytest.mark.xfail(reason="DEF-06", strict=True)
def test_age_one_hundred_is_rejected(driver, clean_db):
    """REQ-REJ-05"""
    submit_registration(
        driver,
        login="user123",
        email="user@example.com",
        age="100",
        password="Password1",
        repeated_password="Password1",
        accept_terms=True,
    )
    assert driver.find_element(By.CSS_SELECTOR, '[data-pole="wiek"]').text == (
        "Wiek musi być liczbą całkowitą z zakresu 18–99."
    )


def test_valid_registration_creates_active_login(driver, clean_db):
    """REQ-REJ-10"""
    submit_registration(
        driver,
        login="new_user",
        email="new@example.com",
        age="27",
        password="Password1",
        repeated_password="Password1",
        accept_terms=True,
    )
    assert driver.find_element(By.ID, "sukces").text == (
        "Konto zostało utworzone. Możesz się zalogować."
    )
    assert driver.find_element(By.ID, "login").get_attribute("value") == ""
    assert log_in(driver, "new_user", "Password1").text == (
        "Zalogowano jako new_user."
    )
