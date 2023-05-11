# Importamos módulos
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Forum
from app.forms import formRegistro, formLogin
import requests
from werkzeug.utils import secure_filename
import os
from flask import redirect, url_for
from app import login_manager
from flask import current_app as app

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
            return redirect(url_for('usuario_micros.foros'))

        flash('Algún campo es incorrecto o aún no has sido validado.', 'success')
    return render_template('login.html', form=form)

#Ruta para foros
@bp.route('/foros')
@login_required
def foros():
    # Obtén los foros disponibles
    forum = Forum.query.all()

    return render_template('foros.html', forum=forum)

@bp.route('/nuevo_foro', methods=['GET', 'POST'])
@login_required
def nuevo_foro():
    if request.method == 'POST':
        # Procesar los datos del formulario de registro de foros
        title = request.form['title']
        description = request.form['description']
        
        # Guardar los datos en la base de datos usando SQLAlchemy
        forum = Forum(title=title, description=description)
        db.session.add(forum)
        db.session


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


