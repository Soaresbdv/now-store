from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from backend.app.models.user import User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = User.query.get(get_jwt_identity())
        if not current_user or not current_user.is_admin:
            return jsonify({"error": "Acesso restrito a administradores"}), 403
        return fn(*args, **kwargs)
    return wrapper