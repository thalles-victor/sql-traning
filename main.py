from flask import Flask, make_response, jsonify, request
from database.db import cars
import uuid

app = Flask(__name__)
app.json.sort_keys = False


@app.route("/cars", methods=["GET"], )
def get_cars():
    return make_response(
        jsonify(message="list of the cars", data =cars)
    )

@app.route("/cars", methods=["POST"])
def create_car():
    body = request.json

    carEntity = {
        "id": uuid.uuid4(),
        "brand": body["brand"],
        "model": body["model"],
        "year": body["year"]
    }

    cars.append(carEntity)
    return make_response(
      jsonify(message="car created", data=carEntity)
    )

app.run()