import allure
from selenium.webdriver.common.action_chains import ActionChains
from locators import ConstructorPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    URL = "https://stellarburgers.nomoreparties.site/"

    @allure.step("Открываем главную страницу Stellar Burgers")
    def open(self):
        self.open_url(self.URL)

    @allure.step("Кликаем на кнопку 'Конструктор'")
    def click_constructor(self):
        self.wait_for_clickable(ConstructorPageLocators.CONSTRUCTOR_BTN).click()

    @allure.step("Кликаем на кнопку 'Лента заказов'")
    def click_order_feed(self):
        element = self.wait_for_clickable(ConstructorPageLocators.ORDER_FEED_BTN)
        try:
            element.click()
        except:
            self.click_via_js(element)

    @allure.step("Кликаем на первый ингредиент")
    def click_first_ingredient(self):
        self.wait_for_clickable(ConstructorPageLocators.FIRST_INGREDIENT).click()

    @allure.step("Проверяем, что модалка ингредиента видна")
    def is_modal_visible(self):
        return self.is_visible(ConstructorPageLocators.MODAL)

    @allure.step("Закрываем модалку ингредиента крестиком")
    def close_modal(self):
        self.wait_for_clickable(ConstructorPageLocators.MODAL_CLOSE_BTN).click()
        self.wait_for_invisible(ConstructorPageLocators.MODAL)

    @allure.step("Перетаскиваем булку в конструктор")
    def drag_bun_to_constructor(self):
        bun = self.wait_for_clickable(ConstructorPageLocators.BUN)
        basket = self.wait_for_visible(ConstructorPageLocators.BASKET)
        self.drag_and_drop(bun, basket)
        return bun

    @allure.step("Получаем текущее значение счётчика ингредиента")
    def get_counter_value(self, element):
        counter = self.find_child_element(element, ConstructorPageLocators.COUNTER)
        return counter.text

    @allure.step("Ждём пока значение счётчика изменится")
    def wait_for_counter_value(self, element, expected_value):
        def counter_updated(_):
            return self.get_counter_value(element) == expected_value

        self.wait_until(counter_updated, f"Счётчик не стал {expected_value}")
        return self.get_counter_value(element)
