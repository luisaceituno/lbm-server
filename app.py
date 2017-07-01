"""Rest API module for LBM"""
from flask import Blueprint
from flask import Flask, request, jsonify
import json
from flask_cors import CORS, cross_origin
from engine import Engine

main = Blueprint('main', __name__)

@main.route("/")
def status_up():
    return "Server is up!"

@main.route("/get/songlist/<float:lon>/<float:lat>")
def get_songlist(lon, lat):
    engine = Engine()
    songlist = engine.get_top_songlist(lon, lat, 250) #radius => 250m 
    return json.dumps(songlist)

@main.route("/get/songlist_city/<float:lon>/<float:lat>")
def get_songlist_city(lon, lat):
    engine = Engine()
    songlist = engine.get_top_songlist(lon, lat, 10000) #radius => 10km
    return json.dumps(songlist)

@main.route("/post/vote", methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def post_vote():
    engine = Engine()
    data = request.get_json(force = True)
    data = json.dumps(data)
    engine.post_vote(data)

    response = jsonify({'reponse': 'success'})
    return response

def create_app(): 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'TEST'
    app.config['CORS_HEADERS'] = 'application/json'
    cors = CORS(app, resources={r"/post/vote": {"origins": "*"}})

    app.register_blueprint(main)
    return app


@main.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# s = get_songlist(8, 49)
# print(s)