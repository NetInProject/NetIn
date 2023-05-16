# Importamos el módulo de Operative System
import os

# Clase config para hacer la conexión con la BD
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '423eb91ccd4e24906f9d7d3e8a8a491f'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Capiyuyu123'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'prueba'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER1 = './app/static/images'
