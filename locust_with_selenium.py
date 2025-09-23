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
        self.failed = False

    def record_event(self, name, action):
        start_time = time.time()
        exception = None
        size_bytes = 0

        try:
            html = action() or ""
            size_bytes = len(html.encode("utf-8"))
        except Exception as e:
            exception = e
            self.failed = True

        total_time = int((time.time() - start_time) * 1000)

        events.request.fire(
            request_type="SELENIUM",
            name=name,
            response_time=total_time,
            response_length=size_bytes,
            exception=exception,
        )

    @task
    def load_homepage(self):
        def action():
            self.driver.get(self.host)
            return self.driver.page_source

        self.record_event("load_homepage", action)

    @task
    def goto_product(self):
        def action():
            self.driver.get(self.host)  # Ensure on homepage
            wait = WebDriverWait(self.driver, 10)
            product = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div.swiper-slide[aria-label="1 / 10"]')
                )
            )
            product.click()
            return self.driver.page_source

        self.record_event("goto_product", action)

    def on_stop(self):
        status = "failed" if self.failed else "passed"
        try:
            self.driver.execute_script(f"lambda-status={status}")
        except Exception as e:
            print(f"Could not set lambda-status: {e}")
        finally:
            setting.tearDown()
