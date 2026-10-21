# place in a top-level file. call it something like seed.py

from app import create_app, db
from app.models.caretaker import Caretaker
from app.models.cat import Cat
from dotenv import load_dotenv

caretakers = [
    {
        "name": "Alpha",
        "cats": [
            {"name": "Luna", "color": "ash", "personality": "Tomato Queen"},
            {"name": "Simon", "color": "black",
                "personality": "might be a human stuck in a cats body"},
            {"name": "Midnight", "color": "black", "personality": "skittish"},
        ],
    },
    {
        "name": "Bravo",
        "cats": [
            {"name": "Leo", "color": "gray tabby", "personality": "friendly"},
            {"name": "Ash", "color": "gray", "personality": "stinker"},
            {"name": "Alder", "color": "tawny",
                "personality": "bouncy, trouncy, flouncy, pouncy, fun, fun, fun, fun, fun"},
        ],
    },
    {
        "name": "Charlie",
        "cats": [
            {"name": "Morty", "color": "orange", "personality": "orange"},
            {"name": "fluffy", "color": "white",
                "personality": "evil with a hint of benevolent"},
            {"name": "Reginold", "color": "orange",
                "personality": "only has one brain cell, but is descendent of Reginold the Great Tabby"},
        ],
    },
    {
        "name": "Delta",
        "cats": [
            {"name": "Katosa", "color": "gray tabby",
                "personality": "Crazy Hunter"},
            {"name": "Milly", "color": "Tortoiseshell",
                "personality": "Loves you a lot but will probably sneeze all over you"},
            {"name": "Meryl", "color": "Tortoiseshell",
                "personality": "Bossy but tries to pass as the sweet one"},

        ],
    },
    {
        "name": "Echo",
        "cats": [
            {"name": "Zelda", "color": "white, gray", "personality": "a mystery"},
            {"name": "Jupiter", "color": "orange",
                "personality": "socially selective"},
            {"name": "Neo", "color": "black", "personality": "stoic"},

        ],
    },
    {
        "name": "Foxtrot",
        "cats": [
            {"name": "Gato", "color": "grey", "personality": "fun"},
            {"name": "Red XIII", "color": "red", "personality": "serious"},
            {"name": "Gizzy", "color": "white", "personality": "unbothered"},

        ],
    },
]

loaners = [
    {"name": "Nimbus", "color": "white", "personality": "floats through life"},
    {"name": "Pixel", "color": "calico", "personality": "always in the details"},
    {"name": "Shadowfax", "color": "silver", "personality": "runs like the wind"},
]

def get_model_by_field(cls, data_dict, key_name):
    value = data_dict[key_name]
    stmt = db.select(cls).where(getattr(cls, key_name) == value)
    return db.session.scalar(stmt)

load_dotenv()
my_app = create_app()
with my_app.app_context():

    for caretaker_data in caretakers:
        caretaker = get_model_by_field(Caretaker, caretaker_data, "name")
        if not caretaker:
            caretaker = Caretaker(name=caretaker_data["name"])
            db.session.add(caretaker)
            db.session.flush()  # get caretaker.id

        for cat_data in caretaker_data["cats"]:
            cat = get_model_by_field(Cat, cat_data, "name")
            if not cat:
                cat = Cat(
                    name=cat_data["name"],
                    color=cat_data["color"],
                    personality=cat_data["personality"],
                    caretaker_id=caretaker.id
                )
                db.session.add(cat)

    # Add loaner cats (no caretaker)
    for cat_data in loaners:
        cat = get_model_by_field(Cat, cat_data, "name")
        if not cat:
            cat = Cat(
                name=cat_data["name"],
                color=cat_data["color"],
                personality=cat_data["personality"],
                caretaker_id=None
            )
            db.session.add(cat)

    db.session.commit()