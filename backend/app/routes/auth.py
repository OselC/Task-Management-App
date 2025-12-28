from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    print(data) # DEBUG LINE

    # Accept either 'username' or legacy 'user' field and trim whitespace
    username = (data.get("username") or data.get("user") or "").strip()
    password = (data.get("password") or "").strip()

    if username == "admin" and password == "admin123":
        token = create_access_token(identity="admin")
        return jsonify(access_token=token)

    return jsonify(message="Invalid credentials"), 401
