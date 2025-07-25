from flask import Flask
from flask_migrate import Migrate
from .models import db

def configure_migrations(app):
    migrate = Migrate(app, db)
    return app