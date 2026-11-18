"""Reusable browser actions for SklepTO tests."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import SKLEPTO_URL, WAIT_SECONDS


def wait_for(driver, by, value):
    """Return an element once it is visible."""
    return WebDriverWait(driver, WAIT_SECONDS).until(
        EC.visibility_of_element_located((by, value))
    )


def open_page(driver, path, by=By.TAG_NAME, value="body"):
    """Open an application page and wait for its identifying element."""
    driver.get(f"{SKLEPTO_URL}/{path.lstrip('/')}")
    WebDriverWait(driver, WAIT_SECONDS).until(
        lambda current_driver: current_driver.execute_script(
            "return document.readyState"
        )
        == "complete"
    )
    return wait_for(driver, by, value)


def log_in(driver, login="jan", password="Haslo123"):
    """Submit the login form and return the resulting flash message."""
    open_page(driver, "logowanie.php", By.ID, "form-logowanie")
    driver.find_element(By.ID, "login").send_keys(login)
    driver.find_element(By.ID, "haslo").send_keys(password)
    driver.find_element(By.ID, "zaloguj").click()
    return wait_for(driver, By.ID, "flash")


def calculator_result(
    driver,
    value,
    *,
    loyalty_card=False,
    code="",
    delivery="kurier",
):
    """Submit calculator data and return discount, delivery, and total."""
    open_page(driver, "kalkulator.php", By.ID, "form-kalkulator")
    driver.find_element(By.ID, "wartosc").send_keys(str(value))
    if loyalty_card:
        driver.find_element(By.ID, "karta").click()
    if code:
        driver.find_element(By.ID, "kod").send_keys(code)
    driver.find_element(By.ID, f"dostawa-{delivery}").click()
    driver.find_element(By.ID, "oblicz").click()
    wait_for(driver, By.ID, "wynik")
    return (
        driver.find_element(By.ID, "rabat").text,
        driver.find_element(By.ID, "koszt-dostawy").text,
        driver.find_element(By.ID, "do-zaplaty").text,
    )
