from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    host = "http://localhost:8000/"
    wait_time = between(1, 3)

    def on_start(self):
        self.client.get("/", name="Load Root")

    @task(2)
    def list_users(self):
        self.client.get("/users/", name="List Users")

    @task(1)
    def get_user(self):
        self.client.get("/users/1", name="Get User 1")

    @task(2)
    def list_items(self):
        self.client.get("/items/", name="List Items")

    @task(1)
    def get_item(self):
        self.client.get("/items/1", name="Get Item 1")
