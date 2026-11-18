"""Tests for order access and lifecycle transitions."""

import pytest
from selenium.webdriver.common.by import By

from conftest import SKLEPTO_URL
from helpers import log_in, open_page, wait_for


def open_orders_as_jan(driver):
    """Log in as Jan and open his orders."""
    log_in(driver)
    return open_page(driver, "zamowienia.php", By.ID, "zamowienia")


def test_logged_out_user_is_redirected_to_login(driver, clean_db):
    """REQ-ZAM-01"""
    open_page(driver, "zamowienia.php", By.ID, "flash")
    assert "logowanie.php" in driver.current_url
    assert driver.find_element(By.ID, "flash").text == (
        "Zaloguj się, aby zobaczyć zamówienia."
    )


def test_jan_sees_only_five_own_orders_and_statuses(driver, clean_db):
    """REQ-ZAM-02"""
    open_orders_as_jan(driver)
    rows = driver.find_elements(By.CSS_SELECTOR, "#zamowienia tr[id^='zam-']")
    assert len(rows) == 5
    assert [
        (
            row.find_element(By.CLASS_NAME, "nr").text,
            row.find_element(By.CLASS_NAME, "kwota").text,
            row.find_element(By.CLASS_NAME, "status").text,
        )
        for row in rows
    ] == [
        ("1", "100.00 zł", "Nowe"),
        ("2", "250.00 zł", "Opłacone"),
        ("3", "80.00 zł", "Wysłane"),
        ("4", "40.00 zł", "Dostarczone"),
        ("5", "60.00 zł", "Anulowane"),
    ]


@pytest.mark.parametrize(
    ("order_id", "expected_actions"),
    [
        (1, ["anuluj", "oplac"]),
        (2, ["anuluj", "wyslij"]),
        pytest.param(
            3,
            ["dostarcz"],
            marks=pytest.mark.xfail(reason="DEF-09", strict=True),
        ),
        (4, []),
        (5, []),
    ],
)
def test_action_buttons_match_order_state(
    driver, clean_db, order_id, expected_actions
):
    """REQ-ZAM-05"""
    open_orders_as_jan(driver)
    row = driver.find_element(By.ID, f"zam-{order_id}")
    classes = [
        next(
            class_name.removeprefix("akcja-")
            for class_name in button.get_attribute("class").split()
            if class_name.startswith("akcja-")
        )
        for button in row.find_elements(By.TAG_NAME, "button")
    ]
    assert sorted(classes) == expected_actions


def test_new_order_has_new_status_and_number(driver, clean_db):
    """REQ-ZAM-03"""
    open_orders_as_jan(driver)
    amount = driver.find_element(By.ID, "kwota")
    amount.clear()
    amount.send_keys("125,50")
    driver.find_element(By.ID, "nowe-zamowienie").click()
    assert wait_for(driver, By.ID, "flash").text == "Utworzono zamówienie #7."
    row = driver.find_element(By.ID, "zam-7")
    assert row.find_element(By.CLASS_NAME, "kwota").text == "125.50 zł"
    assert row.find_element(By.CLASS_NAME, "status").text == "Nowe"


@pytest.mark.parametrize("invalid_amount", ["0", "-1", "abc"])
def test_invalid_new_order_amount_is_rejected(driver, clean_db, invalid_amount):
    """REQ-ZAM-03"""
    open_orders_as_jan(driver)
    amount = driver.find_element(By.ID, "kwota")
    amount.clear()
    amount.send_keys(invalid_amount)
    driver.find_element(By.ID, "nowe-zamowienie").click()
    assert wait_for(driver, By.ID, "flash").text == (
        "Kwota zamówienia musi być dodatnią liczbą."
    )
    assert len(driver.find_elements(By.CSS_SELECTOR, "#zamowienia tr[id^='zam-']")) == 5


def test_pay_new_order_changes_status(driver, clean_db):
    """REQ-ZAM-04, REQ-ZAM-06"""
    open_orders_as_jan(driver)
    driver.find_element(By.CSS_SELECTOR, "#zam-1 .akcja-oplac").click()
    assert wait_for(driver, By.ID, "flash").text == (
        "Zamówienie #1: Nowe → Opłacone."
    )
    row = driver.find_element(By.ID, "zam-1")
    assert row.find_element(By.CLASS_NAME, "status").text == "Opłacone"


def test_forbidden_direct_transition_does_not_change_status(driver, clean_db):
    """REQ-ZAM-07"""
    open_orders_as_jan(driver)
    driver.get(f"{SKLEPTO_URL}/akcja.php?id=4&akcja=anuluj")
    assert wait_for(driver, By.ID, "flash").text == (
        "Niedozwolone przejście: Dostarczone → anuluj."
    )
    assert driver.find_element(By.CSS_SELECTOR, "#zam-4 .status").text == (
        "Dostarczone"
    )


def test_action_on_another_users_order_is_rejected(driver, clean_db):
    """REQ-ZAM-08"""
    open_orders_as_jan(driver)
    driver.get(f"{SKLEPTO_URL}/akcja.php?id=6&akcja=oplac")
    assert wait_for(driver, By.ID, "flash").text == "Nie znaleziono zamówienia."
    assert not driver.find_elements(By.ID, "zam-6")
