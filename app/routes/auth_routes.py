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
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Obter email e senha do formulário
        email = request.form.get(
            "email"
        ).strip()

        password = request.form.get(
            "password"
        )

        # Buscar usuário no banco de dados
        user = User.query.filter_by(
            email=email
        ).first()

        # Verificar se o usuário existe e a senha está correta
        if user and user.check_password(password):

            # Realizar login do usuário
            login_user(user)

            # Exibir mensagem de sucesso
            flash(
                "Login realizado com sucesso.",
                "success"
            )
            # Redirecionar para a página inicial
            return redirect("/")

        # Exibir mensagem de erro para credenciais inválidas
        flash(
            "Email ou senha inválidos.",
            "danger"
        )

    # Renderizar template de login
    return render_template(
        "auth/login.html"
    )

# Rota para logout
@auth_bp.route("/logout")
@login_required
def logout():

    # Realizar logout do usuário
    logout_user()

    # Exibir mensagem de sucesso
    flash(
        "Logout realizado.",
        "success"
    )
    
    # Redirecionar para a página de login
    return redirect(
        url_for("auth.login")
    )
