from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend import db  
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
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

    
def product_owner_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request() 
        product = Product.query.get_or_404(kwargs['id'])
        if product.user_id != get_jwt_identity():
            return jsonify({"error": "Acesso negado: você não é o dono deste produto"}), 403
        return fn(*args, **kwargs)
    return wrapper

@auth_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@auth_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        category=data['category'],
        user_id=get_jwt_identity()
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

# Rota para atualizar produto (apenas dono)
@auth_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
@product_owner_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    
    db.session.commit()
    return jsonify(product.to_dict())

# Rota para deletar produto (apenas dono)
@auth_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
@product_owner_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Produto deletado com sucesso"}), 200

# Rota para detalhes de um produto (público)
@auth_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@auth_bp.route('/my_products', methods=['GET'])
@jwt_required()
def show_user_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    query = Product.query.filter_by(user_id=get_jwt_identity())
    

    if category:
        query = query.filter_by(category=category)
    
    products_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    products_data = [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'created_at': p.created_at.isoformat()
    } for p in products_paginated.items]
    
    return jsonify({
        'products': products_data,
        'total_items': products_paginated.total,
        'current_page': page,
        'items_per_page': per_page
    })