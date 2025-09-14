from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    host = "https://ecommerce-playground.lambdatest.io"
    wait_time = between(1, 3)

    # Load the homepage
    def on_start(self):

        self.client.get(
            "/",
            name="Home Page",
        )

    # Load the shop category page
    @task(3)
    def visit_shop(self):
        self.client.get(
            "/index.php?route=product/category&path=20",
            name="Shop Page",
        )

    # Load the registration page
    @task(2)
    def registration_page(self):
        self.client.get(
            "/index.php?route=account/register",
            name="Register Page",
        )

    # Load the login page
    @task(2)
    def login_page(self):
        self.client.get(
            "/index.php?route=account/login",
            name="Login Page",
        )
