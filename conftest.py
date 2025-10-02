import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Константы
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
    access = data.get("accessToken")      # "Bearer <token>"
    refresh = data.get("refreshToken")    # refresh token string
    if not access or not refresh:
        raise Exception(f"Tokens missing in response: {data}")
    return {"accessToken": access, "refreshToken": refresh}


@pytest.fixture(scope="function")
def logged_in_browser(browser, login_tokens):
    """
    Открывает сайт, прописывает accessToken в localStorage (с 'Bearer '),
    кладёт refreshToken в cookies и в localStorage, обновляет страницу и ждёт
    появления 'Личный Кабинет'.
    """
    browser.get(BASE_URL)  # обязательно открыть домен прежде чем добавлять cookie

    access = login_tokens["accessToken"]    # уже с "Bearer ..."
    refresh = login_tokens["refreshToken"]

    # 1) Положим accessToken в localStorage (как ожидает фронт)
    browser.execute_script(
        "window.localStorage.setItem('accessToken', arguments[0]);",
        access,
    )

    # 2) Для надёжности положим refreshToken и в localStorage и в cookie
    browser.execute_script(
        "window.localStorage.setItem('refreshToken', arguments[0]);",
        refresh,
    )

    # cookie можно добавить только после загрузки страницы домена
    browser.add_cookie({
        "name": "refreshToken",
        "value": refresh,
        "domain": "stellarburgers.nomoreparties.site",
        "path": "/",
    })

    # обновляем страницу, чтобы фронт увидел токены
    browser.refresh()

    # --- отладка: распечатаем, что у нас в localStorage (удали после отладки) ---
    stored_access = browser.execute_script("return window.localStorage.getItem('accessToken');")
    stored_refresh = browser.execute_script("return window.localStorage.getItem('refreshToken');")
    print("DEBUG: localStorage.accessToken:", stored_access)
    print("DEBUG: localStorage.refreshToken:", stored_refresh)
    # ---------------------------------------------------------------------------

    # Ждём подтверждения авторизации (появление "Личный Кабинет")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[text()='Личный Кабинет']"))
    )

    yield browser