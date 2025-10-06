import allure
from selenium.webdriver import ActionChains
from pages.base_page import BasePage
from locators import FeedPageLocators, ConstructorPageLocators, ModalLocators


class FeedPage(BasePage):

    @allure.step("Открываем Ленту заказов")
    def open_feed(self):
        self.wait_for_clickable(FeedPageLocators.FEED_LINK).click()

    @allure.step("Получаем значение счётчика 'Выполнено за всё время'")
    def get_total_orders(self):
        counter = self.wait_for_presence(FeedPageLocators.COUNTER_TOTAL)
        return int(counter.text)

    @allure.step("Открываем Конструктор")
    def open_constructor(self):
        self.wait_for_clickable(ConstructorPageLocators.CONSTRUCTOR_LINK).click()

    @allure.step("Добавляем ингредиенты в корзину")
    def add_ingredients(self):
        actions = ActionChains(self.driver)
        bun = self.wait_for_presence(ConstructorPageLocators.BUN)
        basket = self.wait_for_presence(ConstructorPageLocators.BASKET)
        actions.drag_and_drop(bun, basket).perform()

        sauce = self.wait_for_presence(ConstructorPageLocators.SAUCE)
        actions.drag_and_drop(sauce, basket).perform()

    @allure.step("Оформляем заказ")
    def make_order(self):
        self.wait_for_clickable(ConstructorPageLocators.ORDER_BUTTON).click()

    @allure.step("Ждём появления номера заказа в модалке")
    def wait_for_order_number(self):
        elem = self.wait_for_visible(ModalLocators.ORDER_NUMBER)
        self.wait_until(lambda d: elem.text.isdigit() and elem.text != "9999")
        return elem.text

    @allure.step("Закрываем модалку заказа")
    def close_modal(self):
        self.wait_for_clickable(ModalLocators.CLOSE_BTN).click()
        self.wait_for_invisible(ModalLocators.MODAL_CONTENT)

    @allure.step("Возвращаемся в Ленту заказов через шапку")
    def return_to_feed(self):
        self.wait_for_clickable(FeedPageLocators.FEED_HEADER_LINK).click()

    @allure.step("Получаем значение счётчика 'Выполнено за сегодня'")
    def get_today_orders(self):
        counter = self.wait_for_presence(FeedPageLocators.COUNTER_TODAY)
        return int(counter.text)

    @allure.step("Ждём появления заказа {order_number} в разделе 'Готовы'")
    def wait_for_order_in_ready(self, order_number: str):
        order_number_ui = order_number.zfill(7)

        def order_in_ready(_):
            orders_ready = self.find_elements(FeedPageLocators.ORDERS_READY)
            numbers = [elem.text.strip().lstrip("#") for elem in orders_ready]
            return order_number_ui in numbers

        self.wait_until(order_in_ready, f"Заказ {order_number_ui} не появился в разделе 'Готовы'")
        return order_number_ui

    @allure.step("Ждём, пока счётчик 'Выполнено за сегодня' увеличится")
    def wait_for_today_counter_increase(self, before_value):
        """Ожидаем, что счётчик 'за сегодня' станет больше предыдущего значения"""
        def counter_increased(_):
            return self.get_today_orders() > before_value
        self.wait_until(counter_increased, "Счётчик 'за сегодня' не увеличился вовремя")
