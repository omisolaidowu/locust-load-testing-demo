import time
from locust import User, task, between, events
from selenium_setup.setup import Setting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

setting = Setting("Locust load testing with Selenium")


class SeleniumUser(User):
    host = "https://ecommerce-playground.lambdatest.io"
    wait_time = between(1, 3)  # Random pause between tasks

    def on_start(self):
        setting.setUp()
        self.driver = setting.driver

    @task
    def load_homepage(self):
        start_time = time.time()
        exception = None
        size_bytes = 0
        try:
            self.driver.get(self.host)
            html = self.driver.page_source
            size_bytes = len(html.encode("utf-8"))
        except Exception as e:
            exception = e
        total_time = int((time.time() - start_time) * 1000)
        events.request.fire(
            request_type="SELENIUM",
            name="load_homepage",
            response_time=total_time,
            response_length=size_bytes,
            exception=exception,
        )

    @task
    def goto_product(self):
        start_time = time.time()
        exception = None
        size_bytes = 0
        try:
            self.driver.get(self.host)  # Ensure on homepage
            wait = WebDriverWait(self.driver, 10)
            product = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div.swiper-slide[aria-label="1 / 10"]')
                )
            )
            product.click()
            html = self.driver.page_source
            size_bytes = len(html.encode("utf-8"))
        except Exception as e:
            exception = e
        total_time = int((time.time() - start_time) * 1000)
        events.request.fire(
            request_type="SELENIUM",
            name="goto_product",
            response_time=total_time,
            response_length=size_bytes,
            exception=exception,
        )

    def on_stop(self):
        setting.tearDown()
