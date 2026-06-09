from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from app import db
from app.models.order_service_model import OrderService
from app.models.client_model import Client

# Blueprint para o módulo de ordem de serviço
order_service_bp = Blueprint(
    "order_service",
    __name__,
    url_prefix="/orders"
)

# Rota para exibir a lista de ordens de serviço
@order_service_bp.route("/")
def index():

    orders = OrderService.query.order_by(
        OrderService.id.desc()
    ).all()

    return render_template(
        "orders/index.html",
        orders=orders
    )

# Rota para criar uma nova ordem de serviço
@order_service_bp.route(
    "/create",
    methods=["GET", "POST"]
)
def create():

    clients = Client.query.order_by(
        Client.name.asc()
    ).all()


    if request.method == "POST":

        title = request.form.get(
            "title"
        ).strip()

        equipment = request.form.get(
            "equipment"
        ).strip()

        description = request.form.get(
            "description"
        ).strip()

        technical_notes = request.form.get(
            "technical_notes"
        ).strip()

        status = request.form.get(
            "status"
        )

        client_id = request.form.get(
            "client_id"
        )


        if not title:

            flash(
                "Título é obrigatório.",
                "danger"
            )

            return redirect(
                url_for("order_service.create")
            )


        new_order = OrderService(
            title=title,
            equipment=equipment,
            description=description,
            technical_notes=technical_notes,
            status=status,
            client_id=client_id
        )


        db.session.add(new_order)

        db.session.commit()


        flash(
            "Ordem de serviço criada com sucesso.",
            "success"
        )

        return redirect(
            url_for("order_service.index")
        )


    return render_template(
        "orders/create.html",
        clients=clients
    )
