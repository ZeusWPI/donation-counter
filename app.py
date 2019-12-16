from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from requests import get
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app,
                  key_func=get_remote_address,
                  default_limits=["1 per second"])

amount = 0


def checkTabBalance():
    with app.app_context():
        headers = {
            'Authorization': 'Token token=W+B8gLY/4pzJBlJ9GnD2pA==',
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
    return render_template("home.html")


@app.route("/amount")
def get_amount():
    global amount
    return str(amount)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
