# Importamos los módulos
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError
from flask_wtf.file import FileAllowed
from flask import flash
from app.models import User
import re

# Formulario de registro de foro
class formForum(FlaskForm):
    title = StringField('Nombre del foro', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Registrar foro')
    def validate(self):
        # Realiza las validaciones generales del formulario
        if not super().validate():
            return False

        # Validar campos individuales
        if not self.title.data.strip():
            flash('Debes proporcionar un nombre al foro.', 'danger')
            return False

        if not self.description.data.strip():
            flash('Debes proporcionar una descripcion al foro', 'danger')
            return False

        return True



# Formulario creacion de publicacion
class formPublication(FlaskForm):
    name = StringField('Nombre de la publicación', validators=[DataRequired()])
    content = StringField('Contenido', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Publicar')
    def validate(self):
        # Realiza las validaciones generales del formulario
        if not super().validate():
            return False

        # Validar campos individuales
        if not self.name.data.strip():
            flash('Debes proporcionar un nombre a tu publicacion', 'danger')
            return False

        if not self.content.data.strip():
            flash('Debes proporcionar contenido a tu publicacion', 'danger')
            return False

        if not self.description.data.strip():
            flash('La descripción de la publicación es requerida.', 'danger')
            return False

        return True