from flask import Flask, jsonify, request
from app.data_model import data_model as dm
app = Flask(__name__)


@app.route('/')
def welcome():
    return "Hello"


@app.route('/recommendations', methods=["POST"])
def testPOST():
    ap_data = request.get_json(force=True)
    location = ap_data["lat"]+","+ap_data["lng"]
    model_data = dm.filter_similar_categories_according_to_location(
        ap_data["userId"], ap_data["ToD"], location, "50")
    return jsonify(model_data)
