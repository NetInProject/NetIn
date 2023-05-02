# Importamos los módulos
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError
from flask_wtf.file import FileAllowed

# Función para validar si hay o cedula o pdf
def validar_probatorio(form, field):
    tipo_usuario = form.tipo_usuario.data
    # Si se seleccionó alumno
    if tipo_usuario == 'A':
        if not form.estudiante_pdf.data:
            raise ValidationError('Debes proporcionar un archivo PDF.')
        if form.cedula_profesional.data:
            raise ValidationError('No se permite proporcionar una cédula profesional para el tipo de usuario Alumno.')
    # Si se seleccionó egresado
    elif tipo_usuario == 'E':
        if not form.cedula_profesional.data:
            raise ValidationError('Debes proporcionar una cédula profesional.')
        if form.estudiante_pdf.data:
            raise ValidationError('No se permite proporcionar un archivo PDF para el tipo de usuario Egresado.')


# Formulario de registro
class formRegistro(FlaskForm):
    tipo_usuario = SelectField('Tipo de usuario', choices=[('A', 'Alumno'), ('E', 'Egresado')])
    nombre = StringField('Nombre', validators=[DataRequired()])
    ap_paterno = StringField('Apellido paterno', validators=[DataRequired()])
    ap_materno = StringField('Apellido materno', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repita la contraseña', validators=[DataRequired(), EqualTo('password')])
    cedula_profesional = StringField('Cédula profesional', validators=[Optional(), validar_probatorio])
    estudiante_pdf = FileField('Subir archivo PDF', validators=[Optional(), FileAllowed(['pdf'], 'Solo se permiten archivos PDF'), validar_probatorio])
    submit = SubmitField('Registrarse')

# Formulario de login
class formLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
