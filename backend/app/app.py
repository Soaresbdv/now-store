from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend import db  
from .models.user import User 
from .models.products import Product

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Usuário já existe'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    try:
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username
        }
    }), 200

@auth_bp.route('/products_inside', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    
    required_fields = ['name', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    
    try:
        new_product = Product(
            name=data['name'],
            description=data.get('description', ''),
            category=data['category'],
            color=data.get('color'),
            model=data.get('model'),
            user_id=get_jwt_identity() 
        )
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            "message": "Produto adicionado!",
            "product_id": new_product.id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500