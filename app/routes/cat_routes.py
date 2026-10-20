from flask import Blueprint, abort, make_response, request, Response
from .route_utilities import validate_model
from ..models.cat import Cat
from ..db import db

bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

@bp.post("")
def create_cat():
    request_body = request.get_json()

    new_cat = Cat.from_dict(request_body)
    db.session.add(new_cat)
    db.session.commit()

    return new_cat.to_dict(), 201


@bp.get("")
def get_all_cats():

    query = db.select(Cat)
    name_param = request.args.get("name")

    if name_param:
        query = query.where(Cat.name == name_param)

    color_param = request.args.get("color")
    if color_param:
        query = query.where(Cat.color.ilike(f"%{color_param}%"))
        
    query = query.order_by(Cat.id.desc())

    cats = db.session.scalars(query)

    results_list = []

    for cat in cats: 
        results_list.append(cat.to_dict())

    return results_list


@bp.get("/<id>")
def handle_cat(id):
    cat = validate_model(Cat, id)

    return cat.to_dict()

@bp.put("/<id>")
def replace_cat(id):
    cat = validate_model(Cat, id)

    request_body = request.get_json()
    cat.name = request_body["name"]
    cat.color = request_body["color"]
    cat.personality = request_body["personality"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_cat(id):
    cat = validate_model(Cat, id)

    db.session.delete(cat)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


