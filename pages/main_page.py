import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from locators import ConstructorPageLocators

class MainPage:
    URL = "https://stellarburgers.nomoreparties.site/"

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открываем главную страницу Stellar Burgers")
    def open(self):
        self.driver.get(self.URL)

    @allure.step("Кликаем на кнопку 'Конструктор'")
    def click_constructor(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ConstructorPageLocators.CONSTRUCTOR_BTN)
        ).click()

    @allure.step("Кликаем на кнопку 'Лента Заказов'")
    def click_order_feed(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ConstructorPageLocators.ORDER_FEED_BTN)
        )
        try:
            element.click()
        except:
            # запасной вариант на случай перекрытия
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Кликаем на первый ингредиент")
    def click_first_ingredient(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ConstructorPageLocators.FIRST_INGREDIENT)
        ).click()

    @allure.step("Проверяем видимость модалки ингредиента")
    def is_modal_visible(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(ConstructorPageLocators.MODAL)
            )
            return True
        except:
            return False

    @allure.step("Закрываем модалку ингредиента крестиком")
    def close_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ConstructorPageLocators.MODAL_CLOSE_BTN)
        ).click()
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(ConstructorPageLocators.MODAL)
        )
