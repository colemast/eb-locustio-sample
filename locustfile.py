import random
import datetime

from locust import Locust, TaskSet, task

from api_gateway_client import ApiGatewayClient
import session

import jinja2
import os

NOTIFYSESSION_URL = "https://m0nbfibj40.execute-api.eu-west-1.amazonaws.com/beta/notifysession"

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    template =  jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)
    return template.replace("\n","").replace("\t","")

class Logout(TaskSet):
    @task
    def logout(self):
        print("LOGOUT")
        s = list(session.SessionFactory().generate(1))[0]
        s["device"] = random.choice(s["u"]["devices"])
        s["u"]["devices"].pop()
        event = {   "party_id": s["u"]["party_id"],
                    "session_id": s["mida_session_id"],
                    "timestamp": datetime.datetime.now().isoformat(),
                    "device_id": s["device"]["device_id"],
                    "device_type": s["device"]["device_type"]}
        xml_event = render("templates/notify_session.xml", event)
        self.locust.client.send_event(xml_event)


class AccountOverview(TaskSet):
    min_wait = 10000
    max_wait = 60000

    @task(1000)
    def account_overview(self):
        pass

    @task(100)
    def pending_transactions(self):
        pass

    @task(300)
    def view_transaction(self):
        pass

    @task(600)
    def stop(self):
        self.interrupt()

    tasks = {account_overview: 1000, pending_transactions: 100,
             view_transaction: 300, stop: 600, Logout: 800}


class BenCreation(TaskSet):
    min_wait = 30000
    max_wait = 120000

    @task(1000)
    def add_beneficiary(self):
        pass

    @task(200)
    def stop(self):
        self.interrupt()


class InternationalPayment(TaskSet):
    min_wait = 30000
    max_wait = 120000

    @task(1000)
    def add_beneficiary(self):
        pass

    @task(200)
    def stop(self):
        self.interrupt()


class Payment(TaskSet):
    min_wait = 30000
    max_wait = 120000

    @task
    def payment(self):
        pass

    @task
    def transfer(self):
        pass

    @task
    def stop(self):
        self.interrupt()

    tasks = {BenCreation: 15, InternationalPayment: 1,
             payment: 60, transfer: 10, stop: 5, Logout: 20}


class NormalUser(TaskSet):

    def on_start(self):
        s = list(session.SessionFactory().generate(1))[0]
        s["device"] = random.choice(s["u"]["devices"])
        s["u"]["devices"].pop()
        event = {   "party_id": s["u"]["party_id"],
                    "session_id": s["mida_session_id"],
                    "timestamp": datetime.datetime.now().isoformat(),
                    "device_id": s["device"]["device_id"],
                    "device_type": s["device"]["device_type"]}
        xml_event = render("templates/notify_session.xml", event)
        self.locust.client.send_event(xml_event)

    tasks = {Payment: 15, AccountOverview: 20}


class NormalUserLocust(Locust):
    task_set = NormalUser

    def __init__(self):
        super(NormalUserLocust, self).__init__()
        self.client = ApiGatewayClient(NOTIFYSESSION_URL)
