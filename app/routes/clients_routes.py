from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app import db
from app.models.client_model import Client

client_bp = Blueprint(
    "client",
    __name__,
    url_prefix="/clients"
)


@client_bp.route("/")
def index():

    clients = Client.query.all()

    return render_template(
        "clients/index.html",
        clients=clients
    )


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

        return redirect(url_for("client.index"))

    return render_template("clients/create.html")
