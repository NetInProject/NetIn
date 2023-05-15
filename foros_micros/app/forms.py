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

# Formulario creacion de publicacion
class formPublication(FlaskForm):
    name = StringField('Nombre de la publicación', validators=[DataRequired()])
    content = StringField('Contenido', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Publicar')
