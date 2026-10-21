from flask import Blueprint, request, Response
from .route_utilities import validate_model, create_model_with_response, get_models_with_filters_with_response
from ..models.cat import Cat
from ..db import db

bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

@bp.post("")
def create_cat():
    request_body = request.get_json()

    return create_model_with_response(Cat, request_body)

@bp.get("")
def get_all_cats():
    return get_models_with_filters_with_response(Cat, request.args)


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


