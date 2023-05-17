# Importamos módulos
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import formRegistro, formLogin
import requests
from werkzeug.utils import secure_filename
import os
from flask import redirect, url_for
from app import login_manager
from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer
from flask import make_response

bp = Blueprint('usuario_micros', __name__)

# Ruta por si van al raiz
@bp.route('/')
def index():
    return redirect(url_for('usuario_micros.register'))

# Carga al usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta para registrar un usuario
@bp.route('/registrate', methods=['GET', 'POST'])
def register():
    # Instanciamos el formulario de registro
    form = formRegistro()

    # Verificamos si el formulario fue enviado
    if form.validate_on_submit():
        # Guardamos el archivo PDF del estudiante si se mandó
        if form.estudiante_pdf.data:
            pdf = form.estudiante_pdf.data
            pdf_filename = secure_filename(pdf.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            pdf.save(pdf_path)
        else:
            pdf_path = None

        user = User(
            tipo_usuario=form.tipo_usuario.data,
            nombre=form.nombre.data,
            ap_paterno=form.ap_paterno.data,
            ap_materno=form.ap_materno.data,
            email=form.email.data,
            cedula_profesional=form.cedula_profesional.data,
            estudiante_pdf=pdf_filename if pdf_path else None
        )
        # Hasheamos la contrasenia
        user.set_password(form.password.data)

        # Guardamos la información del usuario en la base de datos
        db.session.add(user)
        db.session.commit()

        flash('Gracias por el registro. Validaremos próximamente tus datos.', 'success')
        return redirect(url_for('usuario_micros.login'))

    return render_template('registro.html', form=form)

# Ruta para iniciar sesión
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Instanciamos el formulario de login
    form = formLogin()

    # Verificamos si el formulario fue enviado
    if form.validate_on_submit():
        # Si el email está en la bd
        user = User.query.filter_by(email=form.email.data).first()
        # Si la contrasenia coincide y verifica si está aprobado
        if user is not None and user.check_password(form.password.data) and user.aprobado:
            login_user(user)
            auth_token = generate_auth_token(user.id)  # Genera un token de autenticación
            if user.es_admin:  # Si el usuario es admin
                response = make_response(redirect(url_for('usuario_micros.validar_usuarios')))  # Redirige a la validación
            else:
                response = make_response(redirect('http://localhost:5001/'))  # Redirige al microservicio de foros
            response.set_cookie('auth_token', auth_token)  # Establece el token de autenticación como una cookie
            return response

        flash('Algún campo es incorrecto o aún no has sido validado.', 'danger')
    return render_template('login.html', form=form)

# Ruta para cerrar sesión
@bp.route('/logout')
@login_required
def logout():
    # Cerramos sesión y regresa al login
    logout_user()
    return redirect(url_for('usuario_micros.login'))

@bp.route('/validar_usuarios', methods=['GET', 'POST'])
@login_required
def validar_usuarios():
    # Verificar si el usuario actual es administrador
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('usuario_micros.login'))

    # Obtener la lista de usuarios no validados
    usuarios_no_validados = User.query.filter_by(aprobado=False).all()

    return render_template('validar_usuarios.html', usuarios=usuarios_no_validados)

@bp.route('/validar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def validar_usuario(usuario_id):
    # Verificar si el usuario actual es administrador
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('usuario_micros.login'))

    # Encontrar al usuario por id
    usuario = User.query.get(usuario_id)
    if usuario:
        # Validar al usuario y guardar en la base de datos
        usuario.aprobado = True
        db.session.commit()

        flash('El usuario ha sido validado.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')

    return redirect(url_for('usuario_micros.validar_usuarios'))

# Genera un token de autenticación después de que el usuario inicia sesión
def generate_auth_token(user_id, expiration=600):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps(user_id)