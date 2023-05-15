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
import os
from flask import send_file



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
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pdf.filename))
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
            estudiante_pdf=pdf_path
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
            return redirect(url_for('index'))

        flash('Algún campo es incorrecto o aún no has sido validado.', 'success')
    return render_template('login.html', form=form)

# Ruta para cerrar sesión
@bp.route('/logout')
@login_required
def logout():
    # Cerramos sesión y regresa al login
    logout_user()
    return redirect(url_for('usuario_micros.login'))

# Función para obtener información de un usuario a partir de su token de autenticación
def perfil(auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get('http://localhost:5001/api/user', headers=headers)

    # Verifica si la respuesta es exitosa
    if response.status_code == 200:
        # Retorna response en json
        return response.json()
    return None


@bp.route('/validarAlumnos', methods=['GET', 'POST'])
def validar():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='A', aprobado =0).all()
    return render_template('validarAlumnos.html', users=users)

@bp.route('/validarEgresado', methods=['GET', 'POST'])
def validarE():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='E', aprobado =0).all()
    return render_template('validarEgresado.html', users=users)

@bp.route('/actualizar-usuario/<int:usuario_id>', methods=['POST'])
def actualizar_usuario(usuario_id):
    # Obtener el usuario de la base de datos
    usuario = User.query.get(usuario_id)
    if usuario:
        # Actualizar el campo "aprobado" del usuario
        usuario.aprobado = 1
        # Guardar los cambios en la base de datos
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado correctamente.'}), 200
    else:
        return jsonify({'message': 'No se encontró el usuario.'}), 404

@bp.route('/allAlumnosV', methods=['GET', 'POST'])
def verAlumnos():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='A', aprobado = 1).all()
    return render_template('allAlumnosV.html', users=users)


@bp.route('/allEgresadosV', methods=['GET', 'POST'])
def verEgresados():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='E', aprobado = 1).all()
    return render_template('allEgresadosV.html', users=users)