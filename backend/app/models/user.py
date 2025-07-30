from backend import db 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    products = db.relationship('Product', backref='owner', lazy=True)

    def __init__(self, username, email, password, is_admin=False): 
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.set_password(password)  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 

    def __repr__(self):
        return f'<User {self.username}>'