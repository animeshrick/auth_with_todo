from flask import Flask ,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, abort, Resource
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config["SECRET_KEY"] = "ANIMESH"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:newpassword@localhost:5432/user"
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{username}:{password}@localhost/{database}'


db = SQLAlchemy(app)
api = Api(app)
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
        return {"message": f"User added"}, 201
    
    def get(self):
        return {"users": jsonify(User.query.first)}
    


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if not password and not username:
            return {"message": "Missing username & passowrod"}, 400
        if user and user.password==password:
            token = create_access_token(identity=user.id)
            return {"message": "Success","token" : token}, 400
        
        return {"message": "Error"}, 400
    

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        return {"message": f"Hi USER_{user}, authorized"}
    


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/secure')
    




if __name__ == '__main__':
    app.run(debug=True)
