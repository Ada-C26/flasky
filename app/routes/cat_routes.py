from flask import Blueprint, abort, make_response
from ..models.cat import cats

cats_bp = Blueprint("cats_bp", __name__, url_prefix="/cats")


@cats_bp.get("")
def get_all_cats():
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
    for cat in cats:
        if cat.id == id:
            return cat
    abort(make_response({"message": f"cat {id} not found"}, 404))
