from flask import (
    Blueprint,
    render_template
)

order_service_bp = Blueprint(
    "order_service",
    __name__,
    url_prefix="/orders"
)

@order_service_bp.route("/")
def index():

    return render_template(
        "orders/index.html"
    )
