# Importamos los módulos que necesitamos
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

# Instanciamos DB, su migrate y Login Manager
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Función para crear la app
def create_app(config_class=Config):
    app = Flask(__name__)
    # Cargamos la configuración de config.py
    app.config.from_object(config_class)

    # Se inicializan db, migrate y lm
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Importamos rutas de foros
    from app.routes import bp as foros
    app.register_blueprint(foros)

    # Retornamos la app
    return app
