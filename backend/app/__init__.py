from flask import Flask
from .config import Config
from .extensions import db, jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Allow routes to be matched with or without a trailing slash
    app.url_map.strict_slashes = False

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .routes.auth import auth_bp
    from .routes.task import task_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(task_bp, url_prefix="/api/tasks")

    return app
