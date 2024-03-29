from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from requests import get
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys

app = Flask(__name__)
limiter = Limiter(app,
                  key_func=get_remote_address,
                  default_limits=["3 per second"])

user = os.getenv("TAB_USER", 'teamtrees_donations')
tab_token = os.environ['TAB_TOKEN']

amount = 0
latest_transactions = []


def checkTabBalance():
    with app.app_context():
        headers = {
            'Authorization': f'Token token={tab_token}',
            'Accept': 'application/json'
        }
        url = f'https://tab.zeus.gent/users/{user}'
        print("Querrying :", url)
        r = get(url, headers=headers)
        if r.status_code == 406:
            print("Wrong tab request, are you using the correct tab token?")
        else:
            global amount
            global latest_transactions
            print("updating balance...")
            print(r.json())
            amount = r.json()["balance"]

            transactions = get(
                f'https://tab.zeus.gent/users/{user}/transactions',
                headers=headers)

            latest_transactions = list(
                reversed(
                    list(
                        filter(lambda x: x['amount'] >= 200,
                               transactions.json()))))[:6]
            # print(latest_transactions)


@app.before_first_request
def initialize():
    apsched = BackgroundScheduler()
    apsched.add_job(lambda: checkTabBalance(), 'interval', seconds=5)
    apsched.start()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/amount")
def get_amount():
    global amount
    return {"amount": amount, "latest_transactions": latest_transactions}


if __name__ == "__main__":
    if 'TAB_TOKEN' not in os.environ:
        print(
            "Please provide the needed tab token in the env variable 'TAB_TOKEN'"
        )
        sys.exit()

    app.run(host='0.0.0.0', port=5000)
