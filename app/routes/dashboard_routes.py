from flask import (
    Blueprint,
    render_template
)

from app.models.client_model import Client

from app.models.order_service_model import (
    OrderService
)

from flask_login import login_required

# Blueprint para o dashboard
dashboard_bp = Blueprint("dashboard", __name__)

# Rota para a página inicial do dashboard
@dashboard_bp.route("/")
@login_required
def home():
    # Consulta para obter o total de clientes
    total_clients = Client.query.count()

    # Consulta para obter o total de ordens de serviço
    total_orders = OrderService.query.count()

    # Consulta para obter o total de ordens de serviço abertas
    open_orders = OrderService.query.filter_by(
        status="Aberto"
    ).count()

    # Consulta para obter o total de ordens de serviço finalizadas
    completed_orders = OrderService.query.filter_by(
        status="Finalizado"
    ).count()

    # Consulta para obter as 5 últimas ordens de serviço
    latest_orders = OrderService.query.order_by(
        OrderService.id.desc()
    ).limit(5).all()

    # Renderiza o template do dashboard, passando os dados obtidos
    return render_template(
        "dashboard/home.html",
        total_clients=total_clients,
        total_orders=total_orders,
        open_orders=open_orders,
        completed_orders=completed_orders,
        latest_orders=latest_orders
    )
