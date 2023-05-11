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
