# Importamos módulos
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
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



bp = Blueprint('foros_micros', __name__)

# Ruta por si van al raiz
@bp.route('/')
def index():
    return "Comunicar servicio"

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



@bp.route('/registrar_publicacion/<int:id_forum>', methods=['GET', 'POST'])
def registrar_publicacion(id_forum):
    # Obtener el foro correspondiente al ID
    forum = Forum.query.get(id_forum)

    # Verificar si el foro existe
    if not forum:
        flash('El foro especificado no existe.', 'error')
        return redirect(url_for('verForos'))

    # Instanciamos el formulario de registro de publicación
    form = formPublication()

    # Verificamos si el formulario fue enviado
    if form.validate_on_submit():
        publication = Publication(
            name=form.name.data,
            content=form.content.data,
            description=form.description.data,
            forum_id=id_forum  # Asignar el ID del foro a la publicación
        )

        # Guardamos la información de la publicación en la base de datos
        db.session.add(publication)
        db.session.commit()

        flash('Publicación registrada exitosamente.', 'success')

    return render_template('registro_publicacion.html', form=form, id_forum=id_forum)




# Ruta para registrar un foro

@bp.route('/VerForo', methods=['GET', 'POST'])
def verForos():
    # Obtener todos los foros de la base de datos
    foros = Forum.query.all()
    return render_template('allForos.html', foros=foros)







@bp.route('/verAlumnos', methods=['GET', 'POST'])
def validar():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='A', aprobado =0).all()
    return render_template('veralumnos.html', users=users)



