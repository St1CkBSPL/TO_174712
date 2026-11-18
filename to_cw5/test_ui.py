"""Tests for navigation and general user-interface requirements."""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import WAIT_SECONDS
from helpers import open_page


PAGES = [
    ("index.php", "SklepTO – strona główna"),
    ("rejestracja.php", "SklepTO – rejestracja"),
    ("logowanie.php", "SklepTO – logowanie"),
    ("kalkulator.php", "SklepTO – kalkulator zamówienia"),
    ("admin.php", "SklepTO – administracja"),
    pytest.param(
        "kontakt.php",
        "SklepTO – kontakt",
        marks=pytest.mark.xfail(reason="DEF-01", strict=True),
    ),
]


@pytest.mark.parametrize(("path", "expected_title"), PAGES)
def test_page_has_descriptive_title(driver, path, expected_title):
    """REQ-UI-02"""
    open_page(driver, path)
    assert driver.title == expected_title


def test_logged_out_menu_contains_required_items(driver):
    """REQ-UI-01"""
    open_page(driver, "index.php", By.ID, "menu")
    menu = driver.find_element(By.ID, "menu")
    assert [link.text for link in menu.find_elements(By.TAG_NAME, "a")] == [
        "Start",
        "Rejestracja",
        "Kalkulator",
        "Zamówienia",
        "Kontakt",
        "Administracja",
        "Logowanie",
    ]


def test_footer_contains_application_version(driver):
    """REQ-UI-07"""
    open_page(driver, "index.php", By.ID, "stopka")
    assert "Wersja 1.0" in driver.find_element(By.ID, "stopka").text


@pytest.mark.parametrize(
    ("link_id", "expected_path", "expected_heading"),
    [
        ("nav-home", "index.php", "Witaj w SklepTO"),
        ("nav-rejestracja", "rejestracja.php", "Rejestracja konta"),
        ("nav-kalkulator", "kalkulator.php", "Kalkulator zamówienia"),
        ("nav-kontakt", "kontakt.php", "Kontakt"),
        ("nav-admin", "admin.php", "Użytkownicy"),
        ("nav-logowanie", "logowanie.php", "Logowanie"),
    ],
)
def test_menu_link_opens_expected_page(
    driver, link_id, expected_path, expected_heading
):
    """REQ-UI-01"""
    open_page(driver, "index.php", By.ID, "menu")
    old_body = driver.find_element(By.TAG_NAME, "body")
    link = driver.find_element(By.ID, link_id)
    driver.execute_script("arguments[0].click();", link)
    WebDriverWait(driver, WAIT_SECONDS).until(EC.staleness_of(old_body))
    WebDriverWait(driver, WAIT_SECONDS).until(EC.url_contains(expected_path))
    heading = driver.find_element(By.TAG_NAME, "h2")
    assert expected_path in driver.current_url
    assert heading.text == expected_heading


@pytest.mark.xfail(reason="DEF-02", strict=True)
def test_every_image_has_non_empty_alt_text(driver):
    """REQ-UI-03"""
    open_page(driver, "kontakt.php")
    images = driver.find_elements(By.TAG_NAME, "img")
    assert images
    assert all((image.get_attribute("alt") or "").strip() for image in images)


@pytest.mark.xfail(reason="DEF-03", strict=True)
def test_contact_fields_have_associated_labels(driver):
    """REQ-UI-04"""
    open_page(driver, "kontakt.php", By.ID, "form-kontakt")
    for field_id in ("imie", "email", "wiadomosc"):
        assert driver.find_elements(By.CSS_SELECTOR, f'label[for="{field_id}"]')


@pytest.mark.xfail(reason="DEF-04", strict=True)
def test_contact_email_field_uses_email_type(driver):
    """REQ-UI-05"""
    open_page(driver, "kontakt.php", By.ID, "email")
    assert driver.find_element(By.ID, "email").get_attribute("type") == "email"
