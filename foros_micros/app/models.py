# Importamos módulos
from usuario_micros.app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Clase Forum (tabla forum)

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Forum {self.title}>"