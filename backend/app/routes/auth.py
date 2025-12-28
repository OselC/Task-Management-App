from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if data["username"] == "admin" and data["password"] == "admin123":
        token = create_access_token(identity="admin")
        return jsonify(access_token=token)

    return jsonify(message="Invalid credentials"), 401
