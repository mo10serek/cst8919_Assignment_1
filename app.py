import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
import logging
import sys

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

# Explicitly configure logging to stdout
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)

app.logger.handlers = []   # Replace default handlers
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

def log(description):
    email = session.get("user").get("userinfo").get("email")
    user_id = session.get("user").get("userinfo").get("sub").split('|', 1)[1]
    datetime = session.get("user").get("userinfo").get("updated_at")
    app.logger.info(json.dumps({
                        "descripton": description, 
                        "user id": user_id, 
                        "email": email, 
                        "timestamp": datetime
                        })
                    )


# Controllers API
@app.route("/")
def home():
    print("the user open the page")
    app.logger.info("the user open the page")

    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    log("the user log in")
    if not 'user' in session:
        app.logger.info("the user has unauthorized attempt")
        print("the user has unauthorized attempt")
    return redirect("/")


@app.route("/login")
def login():
    app.logger.info("the user is going to log in")
    print("the user is going to log in")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True, _scheme="https")
    )


@app.route("/logout")
def logout():
    app.logger.info("the user is going to log out")
    print("the user is going to log out")
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


@app.route("/protected")
def protected():
    if 'user' in session:
        log("the user is trying to access the protected page")
        print("the user is trying to access the protected page")
        return render_template("protected.html")
    else:
        app.logger.info("the user is trying to access the protected page but not able to access it")
        print("the user is trying to access the protected page but not able to access it")
        return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
