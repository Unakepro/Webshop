from flask_restful import request
from flask import Blueprint
from ..db.models import Category
import json
from marshmallow import ValidationError
from .schemas import CategorySchema
from bson.objectid import ObjectId

blue_category = Blueprint("category", __name__)
blue_category_post = Blueprint("category_post", __name__)


@blue_category.route("/tg/category/<name>", methods=('GET', 'PUT', 'DELETE'))
def category(name):
    if request.method == "GET":
        try:
            category_obj = Category.objects(id=name)[0]
            category_list = []
            for sub in category_obj.subcategories:
                category_list.append(sub.title)

            return f"{category_obj.title} <br>\n" \
                   f"{category_list}"
        except:
            return "No category"

    elif request.method == "DELETE":
        try:
            category_obj = Category.objects(id=name)[0]
            category_obj.delete()
            return "OK"
        except:
            return "No category"

    elif request.method == "Put":
        try:
            Category.objects(id=name).update(**request.json)
            return request.json
        except:
            return "No category"


@blue_category_post.route('/tg/category', methods=('GET', 'POST'))
def post():
    if request.method == "GET":
        return "Nothing here"
    elif request.method == "POST":
        json_data = json.dumps(request.json)
        try:
            res = CategorySchema().loads(json_data)
            res = json.loads(CategorySchema().dumps(res))
            sub_list = []

            try:
                parent = res['parent']

                try:
                    subcategories = res['subcategories']
                    del res['parent']
                    del res['subcategories']
                    for i in subcategories:
                        sub_list.append(ObjectId(i))
                    Category.objects.create(**res, parent=ObjectId(parent), subcategories=sub_list)

                except KeyError:
                    del res['parent']
                    Category.objects.create(**res, parent=ObjectId(parent))

            except KeyError:

                try:
                    subcategories = res['subcategories']
                    del res['subcategories']
                    for i in subcategories:
                        sub_list.append(ObjectId(i))
                    Category.objects.create(**res, subcategories=sub_list)

                except KeyError:
                    Category.objects.create(**res)

        except ValidationError as err:
            res = err.messages
        return res
