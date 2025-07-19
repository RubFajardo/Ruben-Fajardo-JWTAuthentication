"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/user/register', methods=['POST'])
def register_user():

    body = request.get_json()
    new_user = User()
    new_user.name = body["name"]
    new_user.email = body["email"]

    new_pass = bcrypt.hashpw(body["password"].encode(), bcrypt.gensalt())

    new_user.password = new_pass.decode()
    new_user.is_active = True

    db.session.add(new_user)
    db.session.commit()


    return jsonify("Usuario registrado"), 200


@api.route('/user/login', methods=['POST'])
def login_user():
    body = request.get_json()
    user = User.query.filter_by(email=body["email"]).first()
    user_data = user.serialize()

    if user is None:
        return jsonify("Usuario no encontrado"), 404
    
    if bcrypt.checkpw(body["password"].encode(), user.password.encode()):
        access_token = create_access_token(identity=str(user_data["id"]))
        return jsonify({"token": access_token, "user_id": user.id}), 200
    
    return jsonify("Invalid Password")

@api.route('/user', methods=['GET'])
@jwt_required()
def user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"user": user.serialize()})