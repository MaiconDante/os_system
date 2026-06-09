from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from app import db

from app.models.user_model import User

# Blueprint para rotas de autenticação
auth_bp = Blueprint(
    "auth",
    __name__
)

# Rota para login
@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        ).strip()

        password = request.form.get(
            "password"
        )


        user = User.query.filter_by(
            email=email
        ).first()


        if user and user.check_password(password):

            login_user(user)


            flash(
                "Login realizado com sucesso.",
                "success"
            )

            return redirect("/")


        flash(
            "Email ou senha inválidos.",
            "danger"
        )


    return render_template(
        "auth/login.html"
    )

# Rota para logout
@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()


    flash(
        "Logout realizado.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )
