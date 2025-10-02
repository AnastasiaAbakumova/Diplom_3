import pytest
import allure
from pages.feed_page import FeedPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.ui
@allure.feature("Лента заказов")
@allure.story("При оформлении заказа счётчик 'Выполнено за всё время' увеличивается")
def test_total_orders_increases_after_order(logged_in_browser):
    browser = logged_in_browser
    feed = FeedPage(browser)

    # 1. Заходим в ленту заказов и берём значение счётчика
    feed.open_feed()
    total_before = feed.get_total_orders()

    # 2. Делаем заказ
    feed.open_constructor()
    feed.add_ingredients()
    feed.make_order()
    order_number = feed.wait_for_order_number()
    print(f"Создан заказ: {order_number}")
    feed.close_modal()

    # 3. Возвращаемся в ленту и проверяем, что счётчик увеличился
    feed.return_to_feed()
    total_after = feed.get_total_orders()

    assert total_after > total_before, f"Ожидали рост счётчика, было {total_before}, стало {total_after}"

@pytest.mark.ui
@allure.feature("Лента заказов")
@allure.story("При оформлении заказа счётчик 'Выполнено за сегодня' увеличивается")
def test_today_orders_increases_after_order(logged_in_browser):
    browser = logged_in_browser
    feed = FeedPage(browser)

    # 1. Заходим в ленту заказов и берём значение счётчика "за сегодня"
    feed.open_feed()
    today_before = feed.get_today_orders()

    # 2. Делаем заказ
    feed.open_constructor()
    feed.add_ingredients()
    feed.make_order()
    order_number = feed.wait_for_order_number()
    print(f"Создан заказ: {order_number}")
    feed.close_modal()

    # 3. Возвращаемся в ленту и проверяем, что счётчик увеличился
    feed.return_to_feed()
    today_after = feed.get_today_orders()

    assert today_after > today_before, f"Ожидали рост счётчика 'за сегодня', было {today_before}, стало {today_after}"

def test_order_appears_in_feed_ready(logged_in_browser):
    browser = logged_in_browser
    feed = FeedPage(browser)

    feed.open_constructor()
    feed.add_ingredients()
    feed.make_order()
    order_number = feed.wait_for_order_number()
    print(f"Создан заказ: {order_number}")
    feed.close_modal()

    feed.open_feed()
    feed.wait_for_order_in_ready(order_number)
