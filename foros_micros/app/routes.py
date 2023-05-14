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



bp = Blueprint('foros_micros', __name__)

# Ruta por si van al raiz
@bp.route('/')
def index():
    return "Hola mundo"


@bp.route('/verAlumnos', methods=['GET', 'POST'])
def validar():
    # Obtenemos todos los usuarios que están en la base de datos
    users = User.query.filter_by(tipo_usuario='A', aprobado =0).all()
    return render_template('veralumnos.html', users=users)