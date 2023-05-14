# Importamos los módulos que necesitamos
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Instanciamos DB, su migrate y Login Manager
db = SQLAlchemy()
migrate = Migrate()

# Función para crear la app
def create_app(config_class=Config):
    app = Flask(__name__)
    # Cargamos la configuración de config.py
    app.config.from_object(config_class)

    # Se inicializan db, migrate y lm
    db.init_app(app)
    migrate.init_app(app, db)

    # Importamos rutas
    from app.routes import bp as foros_micros
    app.register_blueprint(foros_micros)

    # Retornamos la app
    return app
