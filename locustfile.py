import random

from locust import Locust, TaskSet, task

from kinesis_client import KinesisClient
import session


class AccountOverview(TaskSet):
    min_wait = 1000
    max_wait = 6000

    @task(1000)
    def account_overview(self):
        pass
        #self.client.put_data_in_stream("account_overview", "Account Overview")

    @task(100)
    def pending_transactions(self):
        pass
        #self.client.put_data_in_stream(
        #    "pending_transactions", "Pending Transactions")

    @task(300)
    def view_transaction(self):
        pass
        #self.client.put_data_in_stream("view_transaction", "View transaction")

    @task(600)
    def stop(self):
        pass
        #self.interrupt()


class BenCreation(TaskSet):
    min_wait = 3000
    max_wait = 12000

    @task(1000)
    def add_beneficiary(self):
        pass
        #self.client.put_data_in_stream("ben_creation", "Beneficiary Creation")
        #self.client.put_data_in_stream("payment", "Payment")

    @task(200)
    def stop(self):
        pass
        #self.interrupt()


class InternationalPayment(TaskSet):
    min_wait = 3000
    max_wait = 12000

    @task(1000)
    def add_beneficiary(self):
        pass
        #self.client.put_data_in_stream("ben_creation", "Beneficiary Creation")

    @task(200)
    def stop(self):
        pass
        #self.interrupt()


class Payment(TaskSet):
    min_wait = 3000
    max_wait = 12000

    @task
    def payment(self):
        pass
        #self.client.put_data_in_stream("payment", "Payment")

    @task
    def transfer(self):
        pass
        #self.client.put_data_in_stream("transfer", "Transfer")

    @task
    def stop(self):
        pass
        #self.interrupt()

    tasks = {BenCreation: 15, InternationalPayment: 1,
             payment: 60, transfer: 10, stop: 5}


class NormalUser(TaskSet):

    def on_start(self):
        self.new_session()

    @task(30)
    def new_session(self):
        if self.locust.session:
            self.locust.end_session()
        self.locust.create_session()

    tasks = {Payment: 15, AccountOverview: 20}


class NormalUserLocust(Locust):
    task_set = NormalUser

    def __init__(self):
        super(NormalUserLocust, self).__init__()
        self.session = None
        self.client = KinesisClient("eu-west-1", "galaxy-stream", 1)

    def end_session(self):
        self.session = None

    def create_session(self):
        self.session = list(session.SessionFactory().generate(1))[0]
        self.session["device"] = random.choice(self.session["u"]["devices"])
        #self.session["u"]["devices"].pop()
        self.client.put_data_in_stream(self.session, "Login")
