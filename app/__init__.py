from flask import Flask
from .routes.cat_routes import cats_bp

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.register_blueprint(cats_bp)

    return app