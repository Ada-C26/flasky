from flask import Blueprint, request
from ..models.caretaker import Caretaker
from ..models.cat import Cat
from .route_utilities import validate_model, create_model_with_response, get_models_with_filters_with_response
from ..db import db

bp = Blueprint("caretakers_bp", __name__, url_prefix="/caretakers")

@bp.post("")
def create_caretaker():
    request_body = request.get_json()

    return create_model_with_response(Caretaker, request_body)

@bp.get("")
def get_all_caretakers():
    query = db.select(Caretaker)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Caretaker.name == name_param)
    
    caretakers = db.session.scalars(query)

    caretakers_response = []
    for caretaker in caretakers:
        caretakers_response.append(caretaker.to_dict())
    
    return caretakers_response

@bp.post("/<id>/cats")
def create_cat_with_caretaker_id(id):
    caretaker = validate_model(Caretaker, id)

    request_body = request.get_json()
    request_body["caretaker_id"] = caretaker.id

    return create_model_with_response(Cat, request_body)

@bp.get("/<id>/cats")
def get_all_caretaker_cats(id):
    caretaker = validate_model(Caretaker, id)
    cats = [cat.to_dict() for cat in caretaker.cats]

    return cats