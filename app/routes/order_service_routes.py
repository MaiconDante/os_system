from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)
import os
from io import BytesIO
from reportlab.pdfgen import canvas
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

@order_service_bp.route(
    "/<int:order_id>/pdf"
)
@login_required
def generate_pdf(order_id):

    order = OrderService.query.get_or_404(
        order_id
    )

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    logo_path = os.path.join(
        "app",
        "static",
        "images",
        "os.png"
    )

    if os.path.exists(logo_path):

        pdf.drawImage(
        logo_path,
        240,
        730,
        width=120,
        height=60,
        preserveAspectRatio=True,
        mask="auto"
    )

    pdf.setTitle(
        f"OS_{order.id}"
    )

    y = 700

    # CLIENTE

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        620,
        "CLIENTE"
    )


    pdf.roundRect(
        45,
        530,
        500,
        80,
        8
    )


    pdf.setFont(
        "Helvetica",
        11
    )


    pdf.drawString(
        60,
        580,
        f"Nome: {order.client.name}"
    )


    pdf.drawString(
        60,
        560,
        f"Telefone: {order.client.phone or '-'}"
    )


    pdf.drawString(
        60,
        540,
        f"E-mail: {order.client.email or '-'}"
    )

    # DADOS DA ORDEM

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        500,
        "DADOS DA ORDEM"
    )


    pdf.roundRect(
        45,
        410,
        500,
        80,
        8
    )


    pdf.setFont(
        "Helvetica",
        11
    )


    pdf.drawString(
        60,
        460,
        f"Equipamento: {order.equipment}"
    )


    pdf.drawString(
        60,
        440,
        f"Status: {order.status}"
    )


    pdf.drawString(
        60,
        420,
        f"OS Nº: {order.id}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawCentredString(
        300,
        700,
        "ORDEM DE SERVIÇO"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        300,
        680,
        f"Nº {order.id}"
    )

    y -= 40

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        390,
        "DESCRIÇÃO DO PROBLEMA"
    )


    pdf.rect(
        45,
        280,
        500,
        90
    )


    pdf.setFont(
        "Helvetica",
        11
    )


    descricao = order.description or "-"


    pdf.drawString(
        60,
        340,
        descricao[:90]
    )

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=False,
        download_name=f"os_{order.id}.pdf",
        mimetype="application/pdf"
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
