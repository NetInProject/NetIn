# Importamos el módulo de Operative System
import os

# Clase config para hacer la conexión con la BD
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ' '
    MYSQL_USER = os.environ.get('MYSQL_USER') or ' '
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ' '
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or ' '
    MYSQL_DB = os.environ.get('MYSQL_DB') or ' '

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER1 = './app/static/images'
