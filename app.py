"""Rest API module for LBM"""
from flask import Blueprint
from flask import Flask, request, jsonify
import json
from engine import Engine

main = Blueprint('main', __name__)

@main.route("/")
def status_up():
    return "Server is up!"

@main.route("/get/songlist/<float:lon>/<float:lat>")
def get_songlist(lon, lat):
    engine = Engine()
    songlist = engine.get_top_songlist(lon, lat)
    return json.dumps(songlist)

@main.route("/post/vote/", methods=['POST'])
def post_vote():
    engine = Engine()
    data = request.get_json(force = True)
    data = json.dumps(data)
    engine.post_vote(data)
    return "success"

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


s = get_songlist(8, 49)
print(s)