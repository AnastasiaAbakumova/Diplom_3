import pytest
import allure
from pages.main_page import MainPage
from locators import ConstructorPageLocators

@pytest.mark.ui
@allure.feature("Главная страница и конструктор")
class TestMainPage:

    @allure.title("Кнопка 'Конструктор' кликабельна")
    def test_click_constructor(self, browser):
        page = MainPage(browser)
        page.open()
        page.click_constructor()
        # Проверим, что после клика URL изменился
        page.wait_for_url_contains("/")
        assert "stellarburgers.nomoreparties.site" in browser.current_url

    @allure.title("Переход по клику на страницу заказов")
    def test_click_order_feed(self, browser):
        page = MainPage(browser)
        page.open()
        page.click_order_feed()
        page.wait_for_url_contains("/feed")
        assert "/feed" in browser.current_url

    @allure.title("Открытие модального окна ингредиента")
    def test_ingredient_modal(self, browser):
        page = MainPage(browser)
        page.open()
        page.click_first_ingredient()
        assert page.is_modal_visible()

    @allure.title("Закрытие модального окна ингредиента")
    def test_close_modal(self, browser):
        page = MainPage(browser)
        page.open()
        page.click_first_ingredient()
        page.close_modal()
        assert not page.is_modal_visible()

    @allure.title("При добавлении булки в заказ счётчик увеличивается до 2")
    def test_add_bun_increases_counter(self, browser):
        page = MainPage(browser)
        page.open()

        # берём булку
        bun = page.wait_for_presence(ConstructorPageLocators.BUN)

        # проверяем, что счётчик = 0
        assert page.get_counter_value(bun) == "0"

        # перетаскиваем булку в конструктор
        page.drag_bun_to_constructor()

        # проверяем, что счётчик стал = 2
        assert page.get_counter_value(bun) == "2"
