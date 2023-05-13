# Importamos módulos
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Forum, User
from app.forms import CrearForoForm
import requests
from werkzeug.utils import secure_filename
import os
from flask import redirect, url_for
from app import login_manager
from flask import current_app as app

bp = Blueprint('foros_micros', __name__)

# Ruta por si van al raiz
@bp.route('/')
def index():
    return redirect(url_for('foros_micros.foros'))

# Carga al usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Ruta para foros
@bp.route('/foros')
@login_required
def foros():
    # Obtén los foros disponibles
    forum = Forum.query.all()

    return render_template('foros.html', forum=forum)

# Ruta para crear un nuevo foro
@bp.route('/nuevo_foro', methods=['GET', 'POST'])
@login_required
def nuevo_foro():
    form = CrearForoForm()

    if form.validate_on_submit():
        # Procesa los datos del formulario de creación de foros
        title = form.title.data
        description = form.description.data
        
        # Guarda los datos en la base de datos usando SQLAlchemy
        forum = Forum(title=title, description=description)
        db.session.add(forum)
        db.session.commit()

        flash('Tu foro creado exitosamente', 'success')
        return redirect(url_for('foros_micros.foros'))

    return render_template('nuevo_foro.html', form=form)