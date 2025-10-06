import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Базовые ожидания ----------
    @allure.step("Ожидаем кликабельности элемента {locator}")
    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Ожидаем присутствия элемента {locator}")
    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    @allure.step("Ожидаем видимости элемента {locator}")
    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Ожидаем, пока элемент {locator} исчезнет")
    def wait_for_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Ожидаем, что в URL содержится '{url_part}'")
    def wait_for_url_contains(self, url_part):
        return self.wait.until(EC.url_contains(url_part))

    # ---------- Универсальные ----------
    def wait_until(self, condition, message=None):
        return self.wait.until(condition, message)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_child_element(self, parent, locator):
        return parent.find_element(*locator)

    def open_url(self, url):
        self.driver.get(url)

    def click_via_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def is_visible(self, locator):
        try:
            self.wait_for_visible(locator)
            return True
        except:
            return False
