from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

# Importando o banco de dados e o modelo de cliente
from app import db
from app.models.client_model import Client

# Blueprint para as rotas de clientes
client_bp = Blueprint(
    "client",
    __name__,
    url_prefix="/clients"
)

# Rota para listar os clientes
@client_bp.route("/")
def index():

    clients = Client.query.all()

    return render_template(
        "clients/index.html",
        clients=clients
    )

# Rota para criar um novo cliente
@client_bp.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":

        new_client = Client(
            name=request.form.get("name"),
            phone=request.form.get("phone"),
            email=request.form.get("email")
        )

        db.session.add(new_client)

        db.session.commit()

        flash(
            "Cliente cadastrado com sucesso!",
            "success"
        )

        return redirect(url_for("client.index"))

    return render_template("clients/create.html")

# Rota para editar um cliente existente
@client_bp.route("/<int:client_id>/edit", methods=["GET", "POST"])
def edit(client_id):

    client = Client.query.get_or_404(client_id)

    if request.method == "POST":

        client.name = request.form.get("name")

        client.phone = request.form.get("phone")

        client.email = request.form.get("email")

        db.session.commit()

        flash(
            "Cliente atualizado com sucesso!",
            "success"
        )

        return redirect(url_for("client.index"))

    return render_template(
        "clients/edit.html",
        client=client
    )

# Rota para deletar um cliente
@client_bp.route("/<int:client_id>/delete", methods=["POST"])
def delete(client_id):

    client = Client.query.get_or_404(client_id)

    db.session.delete(client)

    db.session.commit()

    flash(
        "Cliente removido com sucesso!",
        "danger"
    )

    return redirect(url_for("client.index"))
