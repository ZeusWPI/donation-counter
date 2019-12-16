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
                  default_limits=["1 per second"])

tab_token = os.environ['TAB_TOKEN']
amount = 0


def checkTabBalance():
    with app.app_context():
        headers = {
            'Authorization': f'Token token={tab_token}',
            'Accept': 'application/json'
        }
        r = get("https://tab.zeus.gent/users/teamtrees_donations",
                headers=headers)
        global amount
        print("updating balance...")
        amount = r.json()["balance"]


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
    return str(amount)


if __name__ == "__main__":
    if 'TAB_TOKEN' not in os.environ:
        print(
            "Please provide the needed tab token in the env variable 'TAB_TOKEN'"
        )
        sys.exit()

    app.run(host='0.0.0.0', port=5000)
