import pytest
import allure
from pages.feed_page import FeedPage


@pytest.mark.ui
@allure.feature("Лента заказов")
class TestFeedOrders:

    @allure.story("Счётчики заказов")
    @allure.title("При оформлении заказа счётчик 'Выполнено за всё время' увеличивается")
    def test_total_orders_increases_after_order(self, logged_in_browser):
        feed = FeedPage(logged_in_browser)

        feed.open_feed()
        total_before = feed.get_total_orders()

        feed.open_constructor()
        feed.add_ingredients()
        feed.make_order()
        order_number = feed.wait_for_order_number()
        allure.attach(str(order_number), name="Создан заказ")
        feed.close_modal()

        feed.return_to_feed()
        total_after = feed.get_total_orders()

        assert total_after > total_before, (
            f"Ожидали рост счётчика, было {total_before}, стало {total_after}"
        )

    @allure.story("Счётчики заказов")
    @allure.title("При оформлении заказа счётчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_increases_after_order(self, logged_in_browser):
        feed = FeedPage(logged_in_browser)

        feed.open_feed()
        today_before = feed.get_today_orders()

        feed.open_constructor()
        feed.add_ingredients()
        feed.make_order()
        order_number = feed.wait_for_order_number()
        allure.attach(str(order_number), name="Создан заказ")
        feed.close_modal()

        feed.return_to_feed()

        # 🔹 Ждём пока число увеличится
        def counter_updated(_):
            return feed.get_today_orders() > today_before

        feed.wait_until(counter_updated, "Счётчик 'за сегодня' не увеличился вовремя")

        today_after = feed.get_today_orders()
        assert today_after > today_before, f"Ожидали рост счётчика, было {today_before}, стало {today_after}"

    @allure.story("Отображение заказов")
    @allure.title("Заказ отображается в списке готовых заказов")
    def test_order_appears_in_feed_ready(self, logged_in_browser):
        feed = FeedPage(logged_in_browser)

        feed.open_constructor()
        feed.add_ingredients()
        feed.make_order()
        order_number = feed.wait_for_order_number()
        allure.attach(str(order_number), name="Создан заказ")
        feed.close_modal()

        feed.open_feed()
        found_order = feed.wait_for_order_in_ready(order_number)

        assert found_order, f"Заказ {order_number} не появился в разделе 'Готовы'"
