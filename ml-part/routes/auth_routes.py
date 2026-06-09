from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models.user import db
from models.user import User

auth_bp = Blueprint(
    "auth",
    __name__
)

VALID_LICENSES = [
    "DOC123",
    "DOC345",
    "DOC456"
]

@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    try:

        data = request.json

        required_fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "role"
        ]

        for field in required_fields:

            if not data.get(field):

                return jsonify({
                    "message": "Please fill in all required fields."
                }), 400

        first_name = data["first_name"].strip()
        last_name = data["last_name"].strip()
        username = data["username"].strip()
        password = data["password"]
        role = data["role"]
        license_number = data.get("license_number")

        if len(password) < 6:

            return jsonify({
                "message": "Password must contain at least 6 characters."
            }), 400

        if role == "doctor":

            if not license_number:

                return jsonify({
                    "message": "Medical license is required for doctor registration."
                }), 400

            if license_number not in VALID_LICENSES:

                return jsonify({
                    "message": "Invalid medical license."
                }), 400

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return jsonify({
                "message": "Username already in use."
            }), 400

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_password,
            role=role,
            license_number=license_number
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful"
        }), 200

    except Exception as e:

        print("REGISTER ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 400


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        data = request.json

        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:

            return jsonify({
                "message": "Please enter username and password."
            }), 400

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:

            return jsonify({
                "message": "User not found."
            }), 404

        valid_password = check_password_hash(
            user.password,
            password
        )

        if not valid_password:

            return jsonify({
                "message": "Invalid password."
            }), 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role,
                "username": user.username
            }
        )

        return jsonify({
            "token": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_id": user.id,
            "role": user.role,
            "username": user.username
        }), 200

    except Exception as e:

        print("LOGIN ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 400