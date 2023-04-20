
# Aquí crea las rutas y funciones que llamarán los html

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from . import db
from .forms import LoginForm, RegistrationForm
from .models import User
from . import login_manager

# Crea un Blueprint llamado "auth" que manejará las rutas relacionadas con la autenticación
auth_blueprint = Blueprint("auth", __name__, template_folder="../frontend/templates")

# Usa el user_id para buscar el usuario correspondiente en la Base de Datos
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta de la página principal
@auth_blueprint.route("/")
def index():
    # Redirecciona al usuario a la ruta "/login"
    return redirect(url_for("auth.login"))

# Ruta para iniciar sesión
@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # Si el usuario ya está autenticado, redirige a la página principal del usuario
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))

    # Crea una instancia del formulario LoginForm
    form = LoginForm()

    # Si el formulario se ha enviado y es válido
    if form.validate_on_submit():
        # Busca al usuario en la base de datos por correo electrónico
        user = User.query.filter_by(email=form.email.data).first()

        # Si el usuario existe y la contraseña es correcta
        if user is not None and user.check_password(form.password.data):
            # Inicia sesión del usuario
            login_user(user)
            # Obtiene la siguiente página a la que se debe redirigir al usuario
            next_page = request.args.get("next")
            # Redirecciona al usuario a la página siguiente o al panel de control
            return redirect(next_page or url_for("auth.index"))
        else:
            # Muestra un mensaje de error si el correo electrónico o la contraseña no son válidos
            flash("Invalid email or password")

    # Renderiza la plantilla de inicio de sesión con el formulario
    return render_template("login.html", title="Sign In", form=form)

# Ruta para registrarse
@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    # Si el usuario ya está autenticado, redirige a la página principal del usuario
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))

    # Crea una instancia del formulario RegistrationForm
    form = RegistrationForm()

    # Si el formulario se ha enviado y es válido
    if form.validate_on_submit():
        # Crea un nuevo objeto de usuario con los datos del formulario
        user = User(email=form.email.data)  # Elimina la referencia a username aquí
        user.set_password(form.password.data)

        # Guarda el nuevo usuario en la base de datos
        db.session.add(user)
        db.session.commit()

        # Muestra un mensaje de éxito y redirige al usuario a la página de inicio de sesión
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))

    # Renderiza la plantilla de registro con el formulario
    return render_template("register.html", title="Register", form=form)

# Ruta para cerrar sesión
@auth_blueprint.route("/logout")
@login_required  # Requiere que el usuario haya iniciado sesión
def logout():
    # Cierra la sesión del usuario
    logout_user()

    # Redirige al usuario a la página de inicio de sesión
    return redirect(url_for("auth.login"))