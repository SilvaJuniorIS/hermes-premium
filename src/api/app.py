from api import app
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hermes online!"

__all__ = ["app"]