from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from routes.auth_routes import auth_bp
from routes.diagnosis_routes import diagnosis_bp
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)
CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(diagnosis_bp)

with app.app_context():
    db.create_all()

print(app.url_map)

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
