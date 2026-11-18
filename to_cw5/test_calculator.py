"""Tests for discounts, delivery costs, and calculator validation."""

import pytest
from selenium.webdriver.common.by import By

from helpers import calculator_result, open_page, wait_for


@pytest.mark.parametrize(
    ("loyalty_card", "code", "discount", "delivery", "total"),
    [
        (False, "", "0%", "15.00 zł", "115.00 zł"),
        (True, "", "10%", "0.00 zł", "90.00 zł"),
        (False, "STUDENT10", "10%", "15.00 zł", "105.00 zł"),
        pytest.param(
            True,
            "STUDENT10",
            "15%",
            "0.00 zł",
            "85.00 zł",
            marks=pytest.mark.xfail(reason="DEF-08", strict=True),
        ),
    ],
)
def test_discount_combinations(
    driver, loyalty_card, code, discount, delivery, total
):
    """REQ-KAL-03, REQ-KAL-05, REQ-KAL-07"""
    assert calculator_result(
        driver, "100", loyalty_card=loyalty_card, code=code
    ) == (discount, delivery, total)


@pytest.mark.parametrize(
    ("delivery_method", "delivery_cost", "total"),
    [
        ("kurier", "15.00 zł", "115.00 zł"),
        ("paczkomat", "10.00 zł", "110.00 zł"),
        ("odbior", "0.00 zł", "100.00 zł"),
    ],
)
def test_paid_delivery_methods(driver, delivery_method, delivery_cost, total):
    """REQ-KAL-06, REQ-KAL-07"""
    assert calculator_result(driver, "100", delivery=delivery_method) == (
        "0%",
        delivery_cost,
        total,
    )


def test_delivery_is_free_from_two_hundred_zloty(driver):
    """REQ-KAL-05"""
    assert calculator_result(driver, "200", delivery="kurier") == (
        "0%",
        "0.00 zł",
        "200.00 zł",
    )


def test_discount_code_is_trimmed_and_case_insensitive(driver):
    """REQ-KAL-04"""
    assert calculator_result(driver, "100", code="  student10  ") == (
        "10%",
        "15.00 zł",
        "105.00 zł",
    )


def test_invalid_discount_code_is_ignored_with_message(driver):
    """REQ-KAL-04"""
    assert calculator_result(driver, "100", code="INVALID") == (
        "0%",
        "15.00 zł",
        "115.00 zł",
    )
    assert driver.find_element(By.ID, "kod-info").text == (
        "Nieprawidłowy kod rabatowy – został pominięty."
    )


@pytest.mark.parametrize("invalid_value", ["0", "10000,01", "abc"])
def test_invalid_order_value_reports_error(driver, invalid_value):
    """REQ-KAL-02"""
    open_page(driver, "kalkulator.php", By.ID, "form-kalkulator")
    driver.find_element(By.ID, "wartosc").send_keys(invalid_value)
    driver.find_element(By.ID, "oblicz").click()
    assert wait_for(driver, By.CSS_SELECTOR, "#bledy .blad").text == (
        "Wartość zamówienia musi być liczbą z zakresu 0,01–10000,00."
    )
    assert not driver.find_elements(By.ID, "wynik")


def test_entered_data_remains_after_calculation(driver):
    """REQ-KAL-01"""
    calculator_result(
        driver,
        "150,00",
        loyalty_card=True,
        code="student10",
        delivery="paczkomat",
    )
    assert driver.find_element(By.ID, "wartosc").get_attribute("value") == "150,00"
    assert driver.find_element(By.ID, "karta").is_selected()
    assert driver.find_element(By.ID, "kod").get_attribute("value") == "student10"
    assert driver.find_element(By.ID, "dostawa-paczkomat").is_selected()


@pytest.mark.xfail(reason="DEF-08", strict=True)
def test_specification_calculator_example(driver):
    """REQ-KAL-08"""
    assert calculator_result(
        driver,
        "150",
        loyalty_card=True,
        code="student10",
        delivery="kurier",
    ) == ("15%", "0.00 zł", "127.50 zł")
