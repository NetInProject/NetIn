# Importamos módulos
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
import requests
from werkzeug.utils import secure_filename
import os
from flask import redirect, url_for
from flask import current_app as app
import os
from flask import send_file
from .models import Forum
from app.forms import formForum, formPublication
from .models import Publication
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import request, current_app

bp = Blueprint('foros_micros', __name__)

# Ruta por si van al raiz
@bp.route('/')
def index():
    return redirect(url_for('foros_micros.verForos'))

# Ruta para registrar un foro

@bp.route('/registrar_foro', methods=['GET', 'POST'])
def register_forum():
    # Instanciamos el formulario de registro de foro
    form = formForum()

    # Verificamos si el formulario fue enviado
    if form.validate_on_submit():
        forum = Forum(
            title=form.title.data,
            description=form.description.data
        )

        # Guardamos la información del foro en la base de datos
        db.session.add(forum)
        db.session.commit()

        flash('Foro registrado exitosamente.', 'success')

    return render_template('registro_foro.html', form=form)



from flask import redirect, url_for
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Ruta para registrar una publicación
@bp.route('/registrar_publicacion/<int:id_forum>', methods=['GET', 'POST'])
def registrar_publicacion(id_forum):

    auth_token = request.cookies.get('auth_token')  # Obtiene el token de autenticación de las cookies
    user_id = validate_auth_token(auth_token)  # Valida el token y obtiene el user_id

    if user_id is None:
        return "Token de autenticación inválido o expirado", 403
    
    # Obtener el usuario correspondiente al ID
    user = User.query.get(user_id)

    # Verificar si el usuario existe
    if not user:
        return "Usuario no encontrado", 404
    else:
        # Instanciamos el formulario de registro de publicación
        form = formPublication()

        # Verificamos si el formulario fue enviado
        if form.validate_on_submit():
            # Obtener los datos del formulario
            name = form.name.data
            content = form.content.data
            description = form.description.data

            # Obtener el archivo de imagen
            image = form.image.data
            filename = None

            if image:
                # Verificar si se seleccionó un archivo
                if allowed_file(image.filename):
                # Generar un nombre seguro para el archivo
                    filename = secure_filename(image.filename)

                    # Guardar la imagen en el directorio de subidas
                    image.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))

            # Crear una nueva publicación con los datos del formulario
        
            publication = Publication(
                name=name,
                content=content,
                description=description,
                image= filename,  # Asignar el nombre de la imagen a la publicación
                forum_id=id_forum,  # Asignar el ID del foro a la publicación
                user_id=user.id
            )

            # Guardar la información de la publicación en la base de datos
            db.session.add(publication)
            db.session.commit()

            flash('Publicación registrada exitosamente.', 'success')

            # Redirigir al usuario a la página de ver publicaciones en el foro
            return redirect(url_for('foros_micros.verPublicacion', idforum=id_forum))

    if user_id is None:
        return "Invalid or expired token", 403
    # Obtener el foro correspondiente al ID
    forum = Forum.query.get(id_forum)

    # Verificar si el foro existe
    if not forum:
        flash('El foro especificado no existe.', 'error')
        return redirect(url_for('foros_micros.verForos'))


    return render_template('registro_publicacion.html', form=form, id_forum=id_forum, user_id=user)




# Ruta para registrar un foro

@bp.route('/VerForo', methods=['GET', 'POST'])
def verForos():
    # Obtener todos los foros de la base de datos
    foros = Forum.query.all()
    return render_template('allForos.html', foros=foros)



@bp.route('/VerPublicacion/<int:idforum>/', methods=['GET', 'POST'])
def verPublicacion(idforum):

    auth_token = request.cookies.get('auth_token')  # Obtiene el token de autenticación de las cookies
    user_id = validate_auth_token(auth_token)  # Valida el token y obtiene el user_id
    # Obtener el usuario correspondiente al ID
    user = User.query.get(user_id)

    form = formPublication()
    # Obtener todos los foros de la base de datos
    publicaciones = Publication.query.filter_by(forum_id=idforum).all()
    return render_template('page.html', publicaciones=publicaciones, idforum = idforum, form=form, user=user)




@bp.route('/verAlumnos', methods=['GET', 'POST'])
def validar():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='A', aprobado =0).all()
    return render_template('veralumnos.html', users=users)


@bp.route('/volverAForos', methods=['GET'])
def volverAForos():
    return redirect(url_for('foros_micros.verForos'))


# Valida el token de autenticación y extrae el user_id del token
def validate_auth_token(auth_token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(auth_token, max_age=600)  # El token expira después de 600 segundos
    except SignatureExpired:
        return None
    return user_id

# Ruta para cerrar sesión
@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # Cerramos sesión y regresa al login
    logout_user()
    return redirect(url_for('http://localhost:5000/'))