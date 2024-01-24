from locust import TaskSet, constant, task, HttpUser, SequentialTaskSet
import json
import random


class PostQueries(TaskSet):
    @task
    def post_users(self):
        headers = {
            "accept": "application/json",
        }

        json_data = json.dumps(
            {
                "charge_code": "",
                "email": "john@doe.com",
                "fullname": f"john doe{random.randint(1,1000)}",
                "phone_number": f"0912{random.randint(1000000,9999999)}",
            }
        )
        x = self.client.post("/customer/", headers=headers, data=json_data)
        if x.status_code != 200:
            print(x.content, x.status_code)
        else:
            print(x.status_code, x.content)


class GetQueries(TaskSet):
    @task
    def post_users(self):
        headers = {
            "accept": "application/json",
        }

        x = self.client.get(
            f"/customer/by-phone/0912{random.randint(1000000,9999999)}", headers=headers
        )
        if x.status_code != 200:
            print(x.content, x.status_code)
        else:
            print(x.status_code, x.content)


class MyLoadTest(HttpUser):
    host = "http://customer:8080"
    tasks = [GetQueries]
    # wait_time = constant(0.5)
