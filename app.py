"""Rest API module for LBM"""
from flask import Blueprint
from flask import Flask, request
import json

main = Blueprint('main', __name__)


@main.route("/")
def status_up():
    return "Server is up!"

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app

