import pytest
import requests
from selenium import webdriver
from pages.base_page import BasePage  # ✅ теперь ждём элементы через BasePage

# --- Константы ---
BASE_URL = "https://stellarburgers.nomoreparties.site"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
USERNAME = "banana@ya.ru"
PASSWORD = "qwerty1234"


@pytest.fixture(scope="function")
def browser():
    """Фикстура для запуска браузера"""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def login_tokens():
    """Возвращает dict с accessToken (включая 'Bearer ') и refreshToken"""
    resp = requests.post(LOGIN_URL, json={"email": USERNAME, "password": PASSWORD})
    if resp.status_code != 200:
        raise Exception(f"Login failed: {resp.status_code} {resp.text}")

    data = resp.json()
    access = data.get("accessToken")
    refresh = data.get("refreshToken")

    if not access or not refresh:
        raise Exception(f"Tokens missing in response: {data}")

    return {"accessToken": access, "refreshToken": refresh}


@pytest.fixture(scope="function")
def logged_in_browser(browser, login_tokens):
    """
    Авторизует пользователя:
    - открывает сайт
    - кладёт токены в localStorage и cookies
    - обновляет страницу
    - ждёт появления элемента "Личный Кабинет"
    """
    page = BasePage(browser)
    page.open_url(BASE_URL)

    access = login_tokens["accessToken"]
    refresh = login_tokens["refreshToken"]

    # Устанавливаем токены
    browser.execute_script("window.localStorage.setItem('accessToken', arguments[0]);", access)
    browser.execute_script("window.localStorage.setItem('refreshToken', arguments[0]);", refresh)

    # Добавляем refreshToken в cookies
    browser.add_cookie({
        "name": "refreshToken",
        "value": refresh,
        "domain": "stellarburgers.nomoreparties.site",
        "path": "/",
    })

    browser.refresh()

    # ✅ Ожидание появления кнопки "Личный Кабинет" через BasePage
    page.wait_for_presence(("xpath", "//p[text()='Личный Кабинет']"))

    yield browser
