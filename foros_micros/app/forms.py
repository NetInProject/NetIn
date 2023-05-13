# Importamos los módulos
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError
from flask_wtf.file import FileAllowed
from flask import flash
from app.models import User
import re


# Formulario de Crear Foros
class CrearForoForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Crear foro')


# Formulario de Crear Post
class CreatePostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Contenido', validators=[DataRequired()])
    submit = SubmitField('Crear Publicación')



# Formulario de Enviar Comentario
class CreateCommentForm(FlaskForm):
    content = TextAreaField('Contenido', validators=[DataRequired()])
    submit = SubmitField('Enviar Comentario')
