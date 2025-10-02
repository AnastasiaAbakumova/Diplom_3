import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import FeedPageLocators, ConstructorPageLocators, ModalLocators


class FeedPage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открываем Ленту заказов")
    def open_feed(self):
        self.wait.until(EC.element_to_be_clickable(FeedPageLocators.FEED_LINK)).click()

    @allure.step("Получаем текущее значение счётчика 'Выполнено за всё время'")
    def get_total_orders(self):
        counter = self.wait.until(EC.presence_of_element_located(FeedPageLocators.COUNTER_TOTAL))
        return int(counter.text)

    @allure.step("Открываем Конструктор")
    def open_constructor(self):
        self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.CONSTRUCTOR_LINK)).click()

    @allure.step("Добавляем ингредиенты в корзину")
    def add_ingredients(self):
        actions = ActionChains(self.driver)
        bun = self.wait.until(EC.presence_of_element_located(ConstructorPageLocators.BUN))
        basket = self.wait.until(EC.presence_of_element_located(ConstructorPageLocators.BASKET))
        actions.drag_and_drop(bun, basket).perform()

        sauce = self.wait.until(EC.presence_of_element_located(ConstructorPageLocators.SAUCE))
        actions.drag_and_drop(sauce, basket).perform()

    @allure.step("Оформляем заказ")
    def make_order(self):
        self.wait.until(EC.element_to_be_clickable(ConstructorPageLocators.ORDER_BUTTON)).click()

    @allure.step("Ждём номер заказа в модалке")
    def wait_for_order_number(self):
        elem = self.wait.until(EC.visibility_of_element_located(ModalLocators.ORDER_NUMBER))
        self.wait.until(lambda d: elem.text.isdigit() and elem.text != "9999")
        return elem.text

    @allure.step("Закрываем модалку заказа крестиком")
    def close_modal(self):
        self.wait.until(EC.element_to_be_clickable(ModalLocators.CLOSE_BTN)).click()
        self.wait.until(EC.invisibility_of_element_located(ModalLocators.MODAL_CONTENT))

    @allure.step("Возвращаемся в Ленту заказов через шапку")
    def return_to_feed(self):
        self.wait.until(EC.element_to_be_clickable(FeedPageLocators.FEED_HEADER_LINK)).click()

    @allure.step("Получаем текущее значение счётчика 'Выполнено за сегодня'")
    def get_today_orders(self):
        counter = self.wait.until(EC.presence_of_element_located(FeedPageLocators.COUNTER_TODAY))
        return int(counter.text)

    @allure.step("Ждём появления заказа в 'Готовы'")
    def wait_for_order_in_ready(self, order_number: str):
        order_number_ui = order_number.zfill(7)

        def order_in_ready(driver):
            orders_ready = driver.find_elements(
                *FeedPageLocators.ORDERS_READY
            )
            numbers = [elem.text.strip().lstrip("#") for elem in orders_ready]
            print(f"Сейчас в разделе 'Готовы': {numbers}")
            return order_number_ui in numbers

        self.wait.until(order_in_ready, f"Заказ {order_number_ui} не появился в разделе 'Готовы'")
        return order_number_ui