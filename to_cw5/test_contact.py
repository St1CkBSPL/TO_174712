"""Tests for the contact form."""

from selenium.webdriver.common.by import By

from helpers import open_page


def test_valid_contact_message_is_accepted(driver, clean_db):
    """REQ-KON-05"""
    open_page(driver, "kontakt.php", By.ID, "form-kontakt")
    driver.find_element(By.ID, "imie").send_keys("Jan")
    driver.find_element(By.ID, "email").send_keys("jan@example.com")
    driver.find_element(By.ID, "wiadomosc").send_keys("Test message")
    driver.find_element(By.ID, "wyslij").click()
    assert driver.find_element(By.ID, "sukces").text == (
        "Dziękujemy za wiadomość."
    )


def test_empty_contact_form_reports_three_errors(driver, clean_db):
    """REQ-KON-02, REQ-KON-03, REQ-KON-04"""
    open_page(driver, "kontakt.php", By.ID, "form-kontakt")
    driver.find_element(By.ID, "wyslij").click()
    assert [
        error.text for error in driver.find_elements(By.CSS_SELECTOR, "#bledy li")
    ] == [
        "Podaj imię.",
        "Niepoprawny adres e-mail.",
        "Wpisz treść wiadomości.",
    ]
