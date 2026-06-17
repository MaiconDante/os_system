from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from datetime import datetime
from app import db
from app.models.order_service_model import OrderService
from app.models.client_model import Client

from flask_login import login_required

# Blueprint para o módulo de ordem de serviço
order_service_bp = Blueprint("order_service", __name__, url_prefix="/orders")

# Rota para exibir a lista de ordens de serviço
@order_service_bp.route("/")
@login_required
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )


    search = request.args.get(
        "search",
        ""
    ).strip()


    status = request.args.get(
        "status",
        ""
    ).strip()


    sort = request.args.get(
        "sort",
        "newest"
    )


    query = OrderService.query


    if search:

        query = query.filter(
            OrderService.title.ilike(
                f"%{search}%"
            )
        )


    if status:

        query = query.filter(
            OrderService.status == status
        )


    if sort == "oldest":

        query = query.order_by(
            OrderService.id.asc()
        )

    else:

        query = query.order_by(
            OrderService.id.desc()
        )


    orders = query.paginate(
        page=page,
        per_page=5
    )

    return render_template(
        "orders/index.html",
        orders=orders,
        search=search,
        status=status,
        sort=sort
    )

# Rota para exibir os detalhes de uma ordem de serviço específica
@order_service_bp.route(
    "/<int:order_id>"
)
@login_required
def details(order_id):

    order = OrderService.query.get_or_404(
        order_id
    )

    service_time = None

    if order.closed_at:

        difference = (
            order.closed_at -
            order.created_at
        )

        days = difference.days

        hours = (
            difference.seconds // 3600
        )

        minutes = (
            difference.seconds % 3600
        ) // 60

        if days > 0:

            service_time = (
                f"{days} dia(s) "
                f"e {hours} hora(s)"
            )

        elif hours > 0:

            service_time = (
                f"{hours} hora(s) "
                f"e {minutes} minuto(s)"
            )

        else:

            service_time = (
                f"{minutes} minuto(s)"
            )

    return render_template(
        "orders/details.html",
        order=order,
        service_time=service_time
    )

# Rota para criar uma nova ordem de serviço
@order_service_bp.route("/create", methods=["GET", "POST"])
@login_required
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


        if status == "Finalizado":
            new_order.closed_at = datetime.utcnow()


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

# Rota para editar uma ordem de serviço existente
@order_service_bp.route(
    "/<int:order_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(order_id):

    order = OrderService.query.get_or_404(
        order_id
    )

    if order.status == "Finalizado":

        flash(
            "Ordens finalizadas não podem ser editadas.",
            "danger"
        )

        return redirect(
            url_for("order_service.index")
        )


    clients = Client.query.order_by(
        Client.name.asc()
    ).all()


    if request.method == "POST":

        order.title = request.form.get(
            "title"
        ).strip()

        order.equipment = request.form.get(
            "equipment"
        ).strip()

        order.description = request.form.get(
            "description"
        ).strip()

        order.technical_notes = request.form.get(
            "technical_notes"
        ).strip()

        order.status = request.form.get(
            "status"
        )

        if order.status == "Finalizado" and order.closed_at is None:

            order.closed_at = datetime.utcnow()

        order.client_id = request.form.get(
            "client_id"
        )


        if not order.title:

            flash(
                "Título é obrigatório.",
                "danger"
            )

            return redirect(
                url_for(
                    "order_service.edit",
                    order_id=order.id
                )
            )


        db.session.commit()


        flash(
            "Ordem atualizada com sucesso.",
            "success"
        )

        return redirect(
            url_for("order_service.index")
        )


    return render_template(
        "orders/edit.html",
        order=order,
        clients=clients
    )

# Rota para excluir uma ordem de serviço
@order_service_bp.route("/<int:order_id>/delete", methods=["POST"])
@login_required
def delete(order_id):

    order = OrderService.query.get_or_404(
        order_id
    )

    if order.status == "Finalizado":

        flash(
            "Ordens finalizadas não podem ser excluídas.",
            "danger"
        )

        return redirect(
            url_for("order_service.index")
        )

    db.session.delete(order)

    db.session.commit()


    flash(
        "Ordem de serviço removida com sucesso.",
        "success"
    )

    return redirect(
        url_for("order_service.index")
    )
