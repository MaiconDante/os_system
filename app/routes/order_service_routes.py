from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
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

def draw_wrapped_text(
    pdf,
    text,
    x,
    y,
    max_width,
    line_height=14
):
    words = text.split()

    line = ""

    for word in words:

        test_line = f"{line} {word}".strip()

        if stringWidth(
            test_line,
            "Helvetica",
            11
        ) < max_width:

            line = test_line

        else:

            pdf.drawString(
                x,
                y,
                line
            )

            y -= line_height

            line = word

    if line:

        pdf.drawString(
            x,
            y,
            line
        )

    return y

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

    def draw_multiline_text(
        pdf,
        text,
        x,
        y,
        line_height=15
    ):
        for line in text.split("\n"):

            pdf.drawString(
                x,
                y,
                line
            )

            y -= line_height

        return y

    order = OrderService.query.get_or_404(
        order_id
    )

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle(
        f"OS_{order.id}"
    )

    y = 760

    # =========================
    # CABEÇALHO
    # =========================

    logo_path = os.path.join(
        "app",
        "static",
        "images",
        "os.png"
    )

    if os.path.exists(logo_path):

        pdf.drawImage(
        logo_path,
        250,
        775,
        width=120,
        height=60,
        preserveAspectRatio=True,
        mask="auto"
    )

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        300,
        y,
        "ORDEM DE SERVIÇO"
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        300,
        y - 25,
        f"Nº {order.id}"
    )

    # =========================
    # CLIENTE
    # =========================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        650,
        "CLIENTE"
    )

    pdf.roundRect(
        45,
        560,
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
        610,
        f"Nome: {order.client.name}"
    )

    pdf.drawString(
        60,
        590,
        f"Telefone: {order.client.phone or '-'}"
    )

    pdf.drawString(
        60,
        570,
        f"E-mail: {order.client.email or '-'}"
    )

    # =========================
    # DADOS DA ORDEM
    # =========================

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        530,
        "DADOS DA ORDEM"
    )

    pdf.roundRect(
        45,
        420,
        500,
        100,
        8
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        60,
        490,
        f"Título: {order.title}"
    )

    pdf.drawString(
        60,
        470,
        f"Equipamento: {order.equipment}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        60,
        450,
        "STATUS:"
    )

    if order.status == "Aberto":

        pdf.setFillColor(
            colors.orange
        )

    elif order.status == "Em andamento":

        pdf.setFillColor(
            colors.blue
        )

    else:

        pdf.setFillColor(
            colors.green
        )

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        120,
        450,
        f"● {order.status.upper()}"
    )

    pdf.setFillColor(
        colors.black
    )

    pdf.drawString(
        60,
        430,
        f"OS Nº: {order.id}"
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        390,
        "DESCRIÇÃO DO PROBLEMA"
    )

    pdf.roundRect(
        45,
        280,
        500,
        90,
        8
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    descricao = (
        order.description or "-"
    )

    draw_wrapped_text(
        pdf,
        descricao,
        60,
        340,
        450
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        250,
        "OBSERVAÇÕES TÉCNICAS"
    )

    pdf.roundRect(
        45,
        140,
        500,
        90,
        8
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    observacoes = (
        order.technical_notes or "-"
    )

    draw_wrapped_text(
        pdf,
        observacoes,
        60,
        200,
        450
    )

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        110,
        "INFORMAÇÕES DO ATENDIMENTO"
    )

    pdf.roundRect(
        45,
        45,
        500,
        50,
        8
    )

    pdf.line(
        210,
        45,
        210,
        95
    )

    pdf.line(
        390,
        45,
        390,
        95
    )

    pdf.setFont(
        "Helvetica",
        11
    )


    abertura = order.created_at.strftime(
        "%d/%m/%Y %H:%M"
    )


    if order.closed_at:

        encerramento = order.closed_at.strftime(
            "%d/%m/%Y %H:%M"
        )

        tempo = order.closed_at - order.created_at

        dias = tempo.days

        horas = tempo.seconds // 3600

        minutos = (
            tempo.seconds % 3600
        ) // 60


        if dias > 0:

            tempo_texto = (
                f"{dias} dia(s) e "
                f"{horas} hora(s)"
            )

        elif horas > 0:

            tempo_texto = (
                f"{horas} hora(s) e "
                f"{minutos} minuto(s)"
            )

        else:

            tempo_texto = (
                f"{minutos} minuto(s)"
            )

    else:

        encerramento = "Em aberto"

        tempo_texto = "Em andamento"


    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.drawString(
        60,
        80,
        "ABERTURA"
    )

    pdf.drawString(
        240,
        80,
        "ENCERRAMENTO"
    )

    pdf.drawString(
        420,
        80,
        "TEMPO"
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawString(
        60,
        62,
        abertura
    )

    pdf.drawString(
        240,
        62,
        encerramento
    )

    pdf.drawString(
        420,
        62,
        tempo_texto
    )

    pdf.line(
        70,
        18,
        240,
        18
    )

    pdf.line(
        350,
        18,
        520,
        18
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawCentredString(
        155,
        2,
        "Assinatura do Técnico"
    )

    pdf.drawCentredString(
        435,
        2,
        "Assinatura do Cliente"
    )

    pdf.setFont(
        "Helvetica-Oblique",
        8
    )

    pdf.drawCentredString(
        300,
        35,
        f"Documento gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
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
