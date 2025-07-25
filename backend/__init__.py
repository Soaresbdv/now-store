from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta'
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from backend.app.app import auth_bp  
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    return app