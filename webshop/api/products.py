from flask_restful import request
from flask import Blueprint
from ..db.models import Products
import json
from marshmallow import ValidationError
from .schemas import ProductSchema
from bson.objectid import ObjectId

blue_products = Blueprint("products", __name__)
blue_products_post = Blueprint("post_products", __name__)


@blue_products.route("/tg/product/<name>", methods=('GET', 'PUT', 'DELETE'))
def product(name):
    if request.method == "GET":
        try:
            product_obj = Products.objects(id=name)[0]
            discount = product_obj.price * (100 - product_obj.discount) / 100
            return f"{product_obj.title} <br>\n" \
                   f"{product_obj.description} <br>\n" \
                   f"{product_obj.created} <br>\n" \
                   f"Цена без скидки: {product_obj.price} <br>\n" \
                   f"Цена со скидкой: {discount}"
        except:
            return "No products"

    elif request.method == "PUT":
        try:
            Products.objects(id=name).update(**request.json)
            return request.json
        except:
            return "No product"

    elif request.method == "DELETE":
        try:
            product_obj = Products.objects(id=name)
            product_obj.delete()
            return "OK"
        except:
            return "No delete"


@blue_products_post.route("/tg/product", methods=("GET", "POST"))
def post():
    if request.method == "GET":
        return "Nothing here"
    elif request.method == "POST":
        json_data = json.dumps(request.json)
        try:
            res = ProductSchema().loads(json_data)
            res = json.loads(ProductSchema().dumps(res))

            category = res['category']
            del res['category']
            with open("webshop/db/images/routers/asus.jpg", "rb") as image:
                Products.objects.create(**res, category=ObjectId(category), image=image)
        except ValidationError as err:
            res = err.messages
        return res
