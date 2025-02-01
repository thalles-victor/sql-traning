from flask import Flask, make_response, jsonify, request
from database.db import cars
import uuid
from repositories.BrandRepository import BrandRepository
from datetime import datetime

brandRepository = BrandRepository()

app = Flask(__name__)
app.json.sort_keys = False


@app.route("/cars", methods=["GET"], )
def get_cars():
    return make_response(
        jsonify(message="list of the cars", data =cars)
    )

@app.route("/brand", methods=["POST"])
def create_car():
    body = request.json

    brandEntity = {
        "id": str(uuid.uuid4()),
        "name": body["name"],
        "description": body["description"],
        "created_at": datetime.now().isoformat()
    }

    created_brand = brandRepository.create(
        brandEntity["id"],
        brandEntity["name"],
        brandEntity["description"],
        brandEntity["created_at"],
    )

    return make_response(
        jsonify(message="Brand created", data=created_brand)
    )


app.run()