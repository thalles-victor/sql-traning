
from database.run_migrations import run_migrations
from flask import Flask, make_response, jsonify, request
from database.db import cars
import uuid
from repositories.BrandRepository import BrandRepository
from repositories.CarRepository import CarRepository
from datetime import datetime
from database.connection import connection_config
from marshmallow import Schema, fields, ValidationError
from schemas.schemas import CreateCarSchema, CreateBrandSchema

run_migrations()

brandRepository = BrandRepository()
carRepository = CarRepository()

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/brand", methods=["POST"])
def create_brand():
    createBrandSchema = CreateBrandSchema()

    try:
        data = createBrandSchema.load(request.json)
    
        created_brand = brandRepository.create(
           id=str(uuid.uuid4()),
           name= data["name"],
           description=data.get("description", None),
           created_at= datetime.now().isoformat()
        )

        return make_response(
            jsonify(message="Brand created", data=created_brand)
        )
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400


@app.route("/brands", methods=["GET"])
def find_brands():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    filters = {}
    if "name" in request.args:
        filters["name"] = request.args["name"]
    if "description" in request.args:
        filters["description"] = request.args["description"]
    
    result = brandRepository.find_many(page=page, limit=limit, filters=filters)
    
    print(result)
    meta = {
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"],
        "total_pages": result["total_pages"]
    }

    print(result["data"])

    return  make_response(jsonify(message="Brands limit", data = result["data"], meta=meta))

@app.route("/cars", methods=["POST"])
def create_car():
    createCarDtoSchema= CreateCarSchema()

    try:
        data = createCarDtoSchema.load(request.json)

        brand = brandRepository.getBy(unqKey="id", valueFromUnqKey=data["brand_id"])

        if not brand:
            return jsonify({"message": "brand not found", "status": 404})

        carCreated = carRepository.create(
            id = str(uuid.uuid4()),
            name = data["name"],
            model = data["model"],
            year= data["year"],
            created_at= datetime.now().isoformat(),
            brand_id= data["brand_id"]
        )

        return jsonify({"message": "car created", "data": carCreated})
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    


if __name__ == "__main__": 
    app.run(debug=True)