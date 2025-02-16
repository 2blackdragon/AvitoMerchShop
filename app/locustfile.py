import random
from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):

    def on_start(self):
        self.username = f"test_user_{random.randint(1000, 9999)}"
        self.password = "qwerty"

        self.headers = {"accept": "application/json"}

        self.client.post("http://localhost:8080/api/auth", data={"username": "toUser", "password": self.password})

        response = self.client.post("http://localhost:8080/api/auth", data={"username": self.username, "password": self.password})
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers["Authorization"] = f"Bearer {self.token}"
        else:
            self.token = None
            self.headers = {}

    @task(2)
    def get_user_info(self):
        self.client.get("http://localhost:8080/api/info", headers=self.headers)

    @task(1)
    def buy_merch(self):
        response = self.client.get("http://localhost:8080/api/buy/cup?quantity=1", headers=self.headers)
        if response.status_code != 200:
            print(f"❌ Ошибка покупки: {response.status_code} {response.detail}")

    @task(1)
    def send_coins(self):
        response = self.client.post(
            "http://localhost:8080/api/sendCoin",
            json={"toUser": "testUser2", "amount": 10},
            headers=self.headers
        )
        if response.status_code != 200:
            print(f"❌ Ошибка перевода монет: {response.status_code} {response.detail}")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
