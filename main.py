from datetime import timedelta

import redis
from flask import Flask
from flask_jwt_extended import JWTManager

from auth.user_model import db

app = Flask(__name__)

redis_host = "127.0.0.1"
redis_port = 6379

# Configure Redis connection
r = redis.Redis(
    host="redis-10928.c277.us-east-1-3.ec2.redns.redis-cloud.com",
    port=10928,
    password="RVffeYzkh3NbAvV0jEA9LMlPxPr1hlAr",
)

# Optional configurations
app.config["SESSION_PERMANENT"] = False  # Session expires when browser closes
app.config["SESSION_USE_SIGNER"] = True  # Sign session data for security

app.config["SECRET_KEY"] = "ANIMESH"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:newpassword@localhost:5432/user"

db.init_app(app)  # Initialize SQLAlchemy with the app

app.config["JWT_SECRET_KEY"] = "jwt-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=10)

jwt = JWTManager(app)

# Import and register the auth blueprint
from auth.authentication import auth_bp

app.register_blueprint(auth_bp, url_prefix="/auth")

with app.app_context():
    db.create_all()
    print("Tables created successfully.")

if __name__ == "__main__":
    app.run(debug=True)
