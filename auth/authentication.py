from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import redis

from auth.user_model import User, db

# Initialize Redis connection
r = redis.Redis(
    host="redis-10928.c277.us-east-1-3.ec2.redns.redis-cloud.com",
    port=10928,
    password="RVffeYzkh3NbAvV0jEA9LMlPxPr1hlAr",
)

auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        if not password and not username:
            return {"message": "Missing username & passowrod"}, 400
        if User.query.filter_by(username=username).first():
            return {"message": f"Username({username}) already exist"}, 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": f"User registered"}, 201

    def get(self):
        users = User.query.all()
        users_list = [
            {"id": user.id, "username": user.username, "password": ""} for user in users
        ]
        return {"users": users_list}, 200


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        user = User.query.filter_by(username=username).first()

        if not password and not username:
            return {"message": "Missing username & passowrod"}, 400
        if user and user.password == password:
            token = create_access_token(identity=user.id, fresh=True)
            rtoken = create_access_token(identity=user.id)

            r.hset(
                f"user_{user.id}_jwt_token",
                mapping={
                    "token": token,
                    "rtoken": rtoken,
                    "user_id": user.id,
                    "dt": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f"),
                },
            )
            return {"message": "Success", "token": token, "rToken": rtoken}, 200

        return {"message": "Error"}, 400


class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user = get_jwt_identity()
            return {"message": f"Hi USER_{user}, authorized"}
        except Exception as e:
            return {"message": f"Error {e}"}


class ProtectedResourceRToken(Resource):
    @jwt_required(refresh=True)
    def get(self):
        try:
            user = get_jwt_identity()
            new_access_token = create_access_token(identity=user)
            return jsonify(access_token=new_access_token)
        except Exception as e:
            return {"message": f"Error {e}"}


api.add_resource(UserRegistration, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(ProtectedResource, "/secure")
api.add_resource(ProtectedResourceRToken, "/rTokenSecure")
