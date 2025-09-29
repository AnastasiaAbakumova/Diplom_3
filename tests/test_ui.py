import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage

@pytest.mark.ui
@allure.feature("Конструктор бургеров")
@allure.story("Проверка кликабельности кнопки 'Конструктор'")
def test_click_constructor(driver):
    page = MainPage(driver)
    page.open()
    page.click_constructor()
    assert page.is_constructor_clickable()

@pytest.mark.ui
@allure.feature("Лента заказов")
@allure.story("Переход на страницу заказов")
def test_click_order_feed(driver):
    page = MainPage(driver)
    page.open()
    page.click_order_feed()
    WebDriverWait(driver, 10).until(EC.url_contains("/feed"))
    assert "/feed" in driver.current_url

@pytest.mark.ui
@allure.feature("Модалки ингредиентов")
@allure.story("Открытие модалки ингредиента")
def test_ingredient_modal(driver):
    page = MainPage(driver)
    page.open()
    page.click_first_ingredient()
    assert page.is_modal_visible()

@pytest.mark.ui
@allure.feature("Модалки ингредиентов")
@allure.story("Закрытие модалки ингредиента крестиком")
def test_close_modal(driver):
    page = MainPage(driver)
    page.open()
    page.click_first_ingredient()
    page.close_modal()
    assert not page.is_modal_visible()
