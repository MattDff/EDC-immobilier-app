from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# Permet à Python de trouver config.py depuis le dossier du service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)

    # Si une config de test est fournie, elle écrase la config par défaut
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp
    app.register_blueprint(bp, url_prefix="/api/v1")

    return app