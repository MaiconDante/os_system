from flask import (
    Blueprint,
    render_template
)

from app.models.client_model import Client

from app.models.order_service_model import (
    OrderService
)

from flask_login import login_required


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def home():

    total_clients = Client.query.count()


    total_orders = OrderService.query.count()


    open_orders = OrderService.query.filter_by(
        status="Aberto"
    ).count()


    completed_orders = OrderService.query.filter_by(
        status="Finalizado"
    ).count()


    latest_orders = OrderService.query.order_by(
        OrderService.id.desc()
    ).limit(5).all()


    return render_template(
        "dashboard/home.html",
        total_clients=total_clients,
        total_orders=total_orders,
        open_orders=open_orders,
        completed_orders=completed_orders,
        latest_orders=latest_orders
    )
