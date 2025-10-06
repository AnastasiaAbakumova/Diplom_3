from selenium.webdriver.common.by import By

class FeedPageLocators:
    FEED_LINK = (By.XPATH, "//p[text()='Лента Заказов']/..")
    COUNTER_TOTAL = (By.CSS_SELECTOR, "p.OrderFeed_number__2MbrQ")
    COUNTER_TODAY = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    FEED_HEADER_LINK = (By.XPATH, "//a[@href='/feed']")
    ORDERS_READY = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem li")

class ConstructorPageLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//p[text()='Конструктор']/..")
    BUN = (By.XPATH, "//p[text()='Флюоресцентная булка R2-D3']/..")
    SAUCE = (By.XPATH, "//p[text()='Соус Spicy-X']/..")
    BASKET = (By.CLASS_NAME, "BurgerConstructor_basket__list__l9dp_")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    CONSTRUCTOR_BTN = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BTN = (By.XPATH, "//p[text()='Лента Заказов']")
    FIRST_INGREDIENT = (By.CSS_SELECTOR, "a.BurgerIngredient_ingredient__1TVf6")
    MODAL = (By.CLASS_NAME, "Modal_modal__contentBox__sCy8X")
    MODAL_CLOSE_BTN = (By.CLASS_NAME, "Modal_modal__close_modified__3V5XS")
    COUNTER = (By.CSS_SELECTOR, ".counter_counter__num__3nue1")
    
class ModalLocators:
    MODAL_CONTENT = (By.CSS_SELECTOR, "div.Modal_modal__contentBox__sCy8X")
    ORDER_NUMBER = (By.CSS_SELECTOR, "div.Modal_modal__contentBox__sCy8X h2")
    CLOSE_BTN = (By.CSS_SELECTOR, "button.Modal_modal__close__TnseK")