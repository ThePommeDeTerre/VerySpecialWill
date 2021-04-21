from flask import Flask, render_template,session
import secrets
import helpers.SessionHelper as SessionHelper
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


@app.route('/')
def main():
    #response = requests.get("http://149.90.108.93:5000/hello")
    SessionHelper.start_session(app)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
