from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv(".env")
LT_USERNAME = os.getenv("LT_USERNAME")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")
EXEC_PLATFORM = os.getenv("EXEC_PLATFORM")


class Setting:
    def __init__(self, test_name):
        self.test_name = test_name
        if EXEC_PLATFORM == "cloud":
            options = webdriver.ChromeOptions()
            options.browser_version = "latest"
            options.platform_name = "Windows 11"
            lt_options = {}
            lt_options["username"] = os.getenv("LT_USERNAME")
            lt_options["accessKey"] = os.getenv("LT_ACCESS_KEY")
            lt_options["build"] = "Load testing with locust demo"
            lt_options["project"] = "Load Testing"
            lt_options["name"] = self.test_name
            lt_options["console"] = "error"
            lt_options["w3c"] = True
            lt_options["plugin"] = "python-python"

            options.set_capability("LT:Options", lt_options)

            lt_hub = "@hub.lambdatest.com/wd/hub"

            gridURL = f"https://{LT_USERNAME}:{LT_ACCESS_KEY}{lt_hub}"

            self.driver = webdriver.Remote(
                command_executor=gridURL,
                options=options,
            )
        elif EXEC_PLATFORM == "local":
            self.chrome_options = webdriver.ChromeOptions()
            self.chrome_options.add_argument("--headless=new")
            self.driver = webdriver.Chrome(options=self.chrome_options)

    def setUp(self):
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def tearDown(self):
        if self.driver is not None:
            self.driver.quit()
