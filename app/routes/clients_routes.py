from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from sqlalchemy import or_

# Importando o banco de dados e o modelo de cliente
from app import db
from app.models.client_model import Client

from flask_login import login_required

# Blueprint para as rotas de clientes
client_bp = Blueprint("client", __name__, url_prefix="/clients")

# Rota para listar os clientes
@client_bp.route("/")
@login_required
def index():
    # Obtendo o parâmetro de busca da query string, removendo espaços em branco extras
    search = request.args.get("search", "").strip()

    # Obtendo o parâmetro de ordenação da query string, com valor padrão "newest"
    sort = request.args.get("sort", "newest")

    # Iniciando a consulta para obter os clientes, aplicando filtros de busca e ordenação conforme necessário
    query = Client.query
    
    # Se um termo de busca for fornecido, filtramos os clientes pelo nome ou e-mail usando o operador OR
    if search:
        # Utilizando o operador OR para filtrar clientes cujo nome ou e-mail contenha o termo de busca, ignorando maiúsculas e minúsculas
        query = query.filter(
            or_(
                Client.name.ilike(f"%{search}%"),
                Client.email.ilike(f"%{search}%")
            )
        )

    # Obtendo o número da página da query string, com valor padrão 1
    page = request.args.get(
        "page",
        1,
        type=int
    )

    # Aplicando a ordenação com base no parâmetro "sort"
    if sort == "name":

        query = query.order_by(
            Client.name.asc()
        )

    # Se o parâmetro de ordenação for "oldest", ordenamos os clientes do mais antigo para o mais recente
    elif sort == "oldest":

        query = query.order_by(
            Client.id.asc()
        )

    else:

        # Por padrão, ordenamos os clientes do mais recente para o mais antigo
        query = query.order_by(
            Client.id.desc()
        )

    # Paginação dos resultados, limitando a 5 clientes por página
    clients = query.paginate(
        page=page,
        per_page=5
    )
    
    # Renderizando o template "clients/index.html" e passando a lista de clientes para a visualização
    return render_template(
        "clients/index.html",
        clients=clients
    )

# Rota para criar um novo cliente
@client_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    # Verificando se o método da requisição é POST para processar o formulário de criação
    if request.method == "POST":
        # Obtendo os dados do formulário e removendo espaços em branco extras
        name = request.form.get("name").strip()

        phone = request.form.get("phone").strip()

        email = request.form.get("email").strip()

        # Validando os dados do formulário, garantindo que o nome seja fornecido
        if not name:

            flash(
                "Nome é obrigatório.",
                "danger"
            )

            return redirect(url_for("client.create"))
        
        # Verificando se o e-mail já está cadastrado no banco de dados
        existing_email = Client.query.filter_by(
            email=email
        ).first()

        # Se o e-mail já existir, exibe uma mensagem de erro e redireciona de volta para a página de criação
        if existing_email:

            flash(
                "Este e-mail já está cadastrado.",
                "danger"
            )

            return redirect(url_for("client.create"))
        
        # Criando um novo cliente com os dados fornecidos
        new_client = Client(
            name=name,
            phone=phone,
            email=email
        )

        # Adicionando o novo cliente à sessão do banco de dados
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
@login_required
def edit(client_id):
    # Consultando o cliente pelo ID, retornando um erro 404 se não for encontrado
    client = Client.query.get_or_404(client_id)

    # Verificando se o método da requisição é POST para processar o formulário de edição
    if request.method == "POST":

        name = request.form.get("name").strip()

        phone = request.form.get("phone").strip()

        email = request.form.get("email").strip()

        # Validando os dados do formulário, garantindo que o nome seja fornecido
        if not name:

            flash(
                "Nome é obrigatório.",
                "danger"
            )

            return redirect(
                url_for(
                    "client.edit",
                    client_id=client.id
                )
            )
        
        # Verificando se o e-mail já está cadastrado para outro cliente no banco de dados
        existing_email = Client.query.filter(
            Client.email == email,
            Client.id != client.id
        ).first()

        # Se o e-mail já existir para outro cliente, exibe uma mensagem de erro e redireciona de volta para a página de edição
        if existing_email:

            flash(
                "Este e-mail já está cadastrado.",
                "danger"
            )

            return redirect(
                url_for(
                    "client.edit",
                    client_id=client.id
                )
            )

        # Atualizando os dados do cliente com os valores fornecidos no formulário
        client.name = name
        client.phone = phone
        client.email = email

        db.session.commit()

        flash(
            "Cliente atualizado com sucesso!",
            "info"
        )

        return redirect(url_for("client.index"))

    return render_template(
        "clients/edit.html",
        client=client
    )

# Rota para deletar um cliente
@client_bp.route("/<int:client_id>/delete", methods=["POST"])
@login_required
def delete(client_id):

    client = Client.query.get_or_404(client_id)

    db.session.delete(client)
    db.session.commit()

    flash(
        "Cliente removido com sucesso!",
        "danger"
    )

    return redirect(url_for("client.index"))
