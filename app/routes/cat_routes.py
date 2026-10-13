from flask import Blueprint, abort, make_response, request, Response
from ..models.cat import Cat
from ..db import db

cats_bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

@cats_bp.post("")
def create_cat():
    request_body = request.get_json()
    name = request_body["name"]
    color = request_body["color"]
    personality = request_body["personality"]

    new_cat = Cat(name=name, color=color, personality=personality)
    db.session.add(new_cat)
    db.session.commit()

    response = dict(
            id=new_cat.id, 
            name=new_cat.name, 
            color=new_cat.color,
            personality=new_cat.personality
        )

    return response, 201




@cats_bp.get("")
def get_all_cats():
    query = db.select(Cat).order_by(Cat.id)
    cats = db.session.scalars(query)

    results_list = []

    for cat in cats: 
        results_list.append(dict(
            id=cat.id, 
            name=cat.name, 
            color=cat.color,
            personality=cat.personality
        ))

    return results_list


@cats_bp.get("/<id>")
def handle_cat(id):
    cat = validate_cat(id)

    return dict(
        id=cat.id,
        name=cat.name,
        color=cat.color,
        personality=cat.personality
    )


def validate_cat(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"cat {id} invalid"}, 400))

    query = db.select(Cat).where(Cat.id == id)
    cat = db.session.scalar(query)
    if not cat:
        abort(make_response({"message": f"cat {id} not found"}, 404))

    return cat

@cats_bp.put("/<id>")
def replace_cat(id):
    cat = validate_cat(id)

    request_body = request.get_json()
    cat.name = request_body["name"]
    cat.color = request_body["color"]
    cat.personality = request_body["personality"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@cats_bp.delete("/<id>")
def delete_cat(id):
    cat = validate_cat(id)

    db.session.delete(cat)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


