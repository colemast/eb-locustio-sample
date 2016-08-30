import random

from locust import Locust, TaskSet, task

from kinesis_client import KinesisClient
import session


class AccountOverview(TaskSet):
    min_wait = 10000
    max_wait = 60000

    @task(1000)
    def account_overview(self):
        self.client.put_data_in_stream("account_overview", "Account Overview")

    @task(100)
    def pending_transactions(self):
        self.client.put_data_in_stream(
            "pending_transactions", "Pending Transactions")

    @task(300)
    def view_transaction(self):
        self.client.put_data_in_stream("view_transaction", "View transaction")

    @task(600)
    def stop(self):
        self.interrupt()


class BenCreation(TaskSet):
    min_wait = 30000
    max_wait = 120000

    @task(1000)
    def add_beneficiary(self):
        self.client.put_data_in_stream("ben_creation", "Beneficiary Creation")
        self.client.put_data_in_stream("payment", "Payment")

    @task(200)
    def stop(self):
        self.interrupt()


class InternationalPayment(TaskSet):
    min_wait = 30000
    max_wait = 120000

    @task(1000)
    def add_beneficiary(self):
        self.client.put_data_in_stream("ben_creation", "Beneficiary Creation")

    @task(200)
    def stop(self):
        self.interrupt()


class Payment(TaskSet):
    min_wait = 30000
    max_wait = 120000

    @task
    def payment(self):
        self.client.put_data_in_stream("payment", "Payment")

    @task
    def transfer(self):
        self.client.put_data_in_stream("transfer", "Transfer")

    @task
    def stop(self):
        self.interrupt()

    tasks = {BenCreation: 15, InternationalPayment: 1,
             payment: 60, transfer: 10, stop: 5}


class NormalUser(TaskSet):

    def on_start(self):
        this_session = session.Session().generate(1)
        this_session["device"] = random.choice(this_session["u"]["devices"])
        this_session["u"]["devices"].pop()
        self.client.put_data_in_stream(session, "Login")

    tasks = {Payment: 15, AccountOverview: 20}


class NormalUserLocust(Locust):
    task_set = NormalUser

    def __init__(self):
        super(NormalUserLocust, self).__init__()
        self.client = KinesisClient("eu-west-1", "galaxy-stream", 1)
