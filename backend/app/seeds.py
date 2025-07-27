from backend.app.models import Category
from backend import db  

def seed_categories():
    categories = [
        {'name': 'Eletrônicos', 'description': 'Dispositivos eletrônicos'},
        {'name': 'Vestuário', 'description': 'Roupas e acessórios'},
        {'name': 'Alimentos', 'description': 'Produtos alimentícios'}
    ]
    
    for cat in categories:
        if not Category.query.filter_by(name=cat['name']).first():
            db.session.add(Category(**cat))
    db.session.commit()