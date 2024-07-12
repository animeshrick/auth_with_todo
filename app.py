from flask import Flask ,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta

from datetime import datetime
import redis
from flask_session import Session

app = Flask(__name__)

redis_host = "127.0.0.1"
redis_port = 6379

# Configure Redis connection
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = redis.from_url(f'redis://{redis_host}:{redis_port}')

r = redis.Redis(
  host='redis-10928.c277.us-east-1-3.ec2.redns.redis-cloud.com',
  port=10928,
  password='RVffeYzkh3NbAvV0jEA9LMlPxPr1hlAr')


# Optional configurations
app.config['SESSION_PERMANENT'] = False  # Session expires when browser closes
app.config['SESSION_USE_SIGNER'] = True  # Sign session data for security

app.config["SECRET_KEY"] = "ANIMESH"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:newpassword@localhost:5432/user"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{password}@localhost/{database}'


db = SQLAlchemy(app)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "jwt-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=10)

jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)

with app.app_context():
    db.create_all()
    print("Tables created successfully.")


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not password and not username:
            return {"message": "Missing username & passowrod"}, 400
        if User.query.filter_by(username=username).first():
            return {"message": f"Username({username}) already exist"}, 400
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"message": f"User registered"}, 201
    
    def get(self):
        return {"users": []}
    


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if not password and not username:
            return {"message": "Missing username & passowrod"}, 400
        if user and user.password==password:
            token = create_access_token(identity=user.id, fresh=True)
            rtoken = create_access_token(identity=user.id)

            r.hset(f"user_{user.id}_jwt_token", mapping={"token": token, "rtoken": rtoken, "user_id": user.id,"dt": datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f')})
            # user_jwt_token = r.hgetall("user_jwt_token")
            # print(f"user_jwt_token {user_jwt_token}")

            return {"message": "Success", "token" : token, 'rToken': rtoken}, 200
        
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


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/secure')
api.add_resource(ProtectedResourceRToken, '/rTokenSecure')
    




if __name__ == '__main__':
    app.run(debug=True)
