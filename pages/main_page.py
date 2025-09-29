import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    URL = "https://stellarburgers.nomoreparties.site/"

    # Элементы страницы
    CONSTRUCTOR_BTN = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BTN = (By.XPATH, "//p[text()='Лента Заказов']")
    FIRST_INGREDIENT = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")
    MODAL = (By.CLASS_NAME, "Modal_modal__contentBox__sCy8X")
    MODAL_CLOSE_BTN = (By.CLASS_NAME, "Modal_modal__close_modified__3V5XS")  # крестик

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открываем главную страницу Stellar Burgers")
    def open(self):
        self.driver.get(self.URL)

    @allure.step("Кликаем на кнопку 'Конструктор'")
    def click_constructor(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONSTRUCTOR_BTN)
        ).click()

    @allure.step("Проверяем, что кнопка 'Конструктор' кликабельна")
    def is_constructor_clickable(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.CONSTRUCTOR_BTN)
        )

    @allure.step("Кликаем на кнопку 'Лента Заказов'")
    def click_order_feed(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ORDER_FEED_BTN)
        ).click()

    @allure.step("Кликаем на первый ингредиент в конструкторе")
    def click_first_ingredient(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FIRST_INGREDIENT)
        ).click()

    @allure.step("Проверяем видимость модалки ингредиента")
    def is_modal_visible(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.MODAL)
            )
            return True
        except:
            return False

    @allure.step("Закрываем модалку ингредиента крестиком")
    def close_modal(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.MODAL_CLOSE_BTN)
        ).click()
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(self.MODAL)
        )
