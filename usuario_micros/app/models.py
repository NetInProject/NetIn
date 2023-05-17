# Importamos módulos
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Clase User (tabla User)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_usuario = db.Column(db.String(2), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    ap_paterno = db.Column(db.String(100), nullable=False)
    ap_materno = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    estudiante_pdf = db.Column(db.String(255), nullable=True)
    cedula_profesional = db.Column(db.String(8), nullable=True)
    es_admin = db.Column(db.Boolean, default=False)
    aprobado = db.Column(db.Boolean, default=False)

    # Establece la contraseña del usuario hasheando la contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verifica la contraseña del usuario
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)