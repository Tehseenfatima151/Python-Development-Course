"""Flask extension instances — imported by the app factory and models."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

# Celery instance — fully configured in create_app via init_celery()
celery = Celery(__name__)
