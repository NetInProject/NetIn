# Importamos los módulos
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError
from flask_wtf.file import FileAllowed
from flask import flash
from app.models import User
import re

# Función para validar el pdf
def validar_pdf(form, field):
        tipo_usuario = form.tipo_usuario.data
        # Si es alumno, debe dar un pdf
        if tipo_usuario == 'A' and not field.data:
            flash('Debes proporcionar un archivo PDF.', 'danger')
            raise ValidationError('Debes proporcionar un archivo PDF.')
        # Si es egresado no puede dar un pdf
        elif tipo_usuario == 'E' and field.data:
            flash('No se permite proporcionar un archivo PDF para el tipo de usuario Egresado.', 'danger')
            raise ValidationError('No se permite proporcionar un archivo PDF para el tipo de usuario Egresado.')


# Función para validar la cédula
def validar_cedula(form, field):
        tipo_usuario = form.tipo_usuario.data
        # Si es egresado debe de dar cédula
        if tipo_usuario == 'E' and not field.data:
            flash('Debes proporcionar una cédula profesional.', 'danger')
            raise ValidationError('Debes proporcionar una cédula profesional.')
        # Si es alumno, no puede dar cédula
        elif tipo_usuario == 'A' and field.data:
            flash('No se permite proporcionar una cédula profesional para el tipo de usuario Alumno.', 'danger')
            raise ValidationError('No se permite proporcionar una cédula profesional para el tipo de usuario Alumno.')
        # regex para que la cédula sean 8 números
        elif field.data:
            if not re.fullmatch(r'^\d{8}$', field.data):
                flash('La cédula profesional debe de contener exactamente 8 números.', 'danger')
                raise ValidationError('La cédula profesional debe contener exactamente 8 números.')
            # Checamos si la cédula ya fue registrada anteriormente
            user = User.query.filter_by(cedula_profesional=field.data).first()
            if user:
                flash('La cédula profesional ya está registrada. Por favor, elige una diferente.', 'danger')
                raise ValidationError('La cédula profesional ya está registrada. Por favor, elige una diferente.')

# Función para validar formato mínimo y duplicidad de email
def validar_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    # regex básico de correo
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", field.data):
        flash('El correo electrónico ingresado no es válido.', 'danger')
        raise ValidationError('El correo electrónico ingresado no es válido.')
    # Si el correo ya fue registrado anteriormente
    if user:
        flash('El correo electrónico ya está registrado. Por favor, elige uno diferente.', 'danger')
        raise ValidationError('El correo electrónico ya está registrado. Por favor, elige uno diferente.')

# Función para validar que la contrasenia sea válida
def validar_contrasenia(form, field):
    password = field.data
    # Si la contraseña es menor a 8 digitos, no tiene al menos una mayuscula y un número
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
        flash('La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.', 'danger')
        raise ValidationError('La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.')

# Formulario de registro
class formRegistro(FlaskForm):
    tipo_usuario = SelectField('Tipo de usuario', choices=[('A', 'Alumno'), ('E', 'Egresado')])
    nombre = StringField('Nombre', validators=[DataRequired()])
    ap_paterno = StringField('Apellido paterno', validators=[DataRequired()])
    ap_materno = StringField('Apellido materno', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), validar_email])
    password = PasswordField('Contraseña', validators=[DataRequired(), validar_contrasenia])
    password2 = PasswordField('Repita la contraseña', validators=[DataRequired(), EqualTo('password')])
    cedula_profesional = StringField('Cédula profesional', validators=[Optional(), validar_cedula])
    estudiante_pdf = FileField('Subir archivo PDF', validators=[Optional(), FileAllowed(['pdf'], 'Solo se permiten archivos PDF'), validar_pdf], render_kw={'accept': 'application/pdf'})
    submit = SubmitField('Registrarse')

# Formulario de login
class formLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
