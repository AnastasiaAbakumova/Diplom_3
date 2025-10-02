import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage
from locators import ConstructorPageLocators


@pytest.mark.ui
@allure.feature("Конструктор бургеров")
@allure.story("Кнопка 'Конструктор' кликабельна")
def test_click_constructor(browser):
    page = MainPage(browser)
    page.open()
    page.click_constructor()
    assert WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(ConstructorPageLocators.CONSTRUCTOR_BTN)
    )


@pytest.mark.ui
@allure.feature("Лента заказов")
@allure.story("Переход по клику на страницу заказов")
def test_click_order_feed(browser):
    page = MainPage(browser)
    page.open()
    page.click_order_feed()
    WebDriverWait(browser, 10).until(EC.url_contains("/feed"))
    assert "/feed" in browser.current_url


@pytest.mark.ui
@allure.feature("Модальные окна ингредиентов")
@allure.story("Открытие модального окна ингредиента")
def test_ingredient_modal(browser):
    page = MainPage(browser)
    page.open()

    # ждём пока первый ингредиент станет кликабельным
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6"))
    )

    page.click_first_ingredient()
    assert page.is_modal_visible()


@pytest.mark.ui
@allure.feature("Модальные окна ингредиентов")
@allure.story("Закрытие модального окна крестиком")
def test_close_modal(browser):
    page = MainPage(browser)
    page.open()
    page.click_first_ingredient()
    page.close_modal()
    assert not page.is_modal_visible()


@pytest.mark.ui
@allure.feature("Конструктор бургеров")
@allure.story("При добавлении булки в заказ счётчик увеличивается до 2")
def test_add_bun_increases_counter(browser):
    browser.get("https://stellarburgers.nomoreparties.site/")
    wait = WebDriverWait(browser, 10)

    # находим первый ингредиент (булку)
    bun = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6"))
    )

    # находим область конструктора
    constructor = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.BurgerConstructor_basket__list__l9dp_"))
    )

    # проверяем начальный счётчик (0)
    counter_elem = bun.find_element(By.CSS_SELECTOR, ".counter_counter__num__3nue1")
    assert counter_elem.text == "0"

    # перетаскиваем булку в конструктор
    ActionChains(browser).drag_and_drop(bun, constructor).perform()

    # ждём, что счётчик изменится на 2
    wait.until(lambda drv: counter_elem.text == "2")
    assert counter_elem.text == "2"
