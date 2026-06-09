from app import db
from datetime import datetime

# Modelo de Ordem de Serviço
class OrderService(db.Model):
    # Definindo o nome da tabela no banco de dados
    __tablename__ = "order_services"

    # Definindo as colunas da tabela OrderService
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # O título da ordem de serviço, que é um campo obrigatório (nullable=False)
    title = db.Column(
        db.String(150),
        nullable=False
    )

    # O equipamento relacionado à ordem de serviço, que é um campo obrigatório (nullable=False)
    equipment = db.Column(
        db.String(150),
        nullable=False
    )

    # A descrição da ordem de serviço, que é um campo obrigatório (nullable=False)
    description = db.Column(
        db.Text,
        nullable=False
    )

    # As notas técnicas da ordem de serviço, que é um campo opcional (nullable=True)
    technical_notes = db.Column(
        db.Text
    )

    # O status da ordem de serviço, que é um campo obrigatório (nullable=False) com valor padrão "Aberto"       
    status = db.Column(
        db.String(30),
        nullable=False,
        default="Aberto"
    )

    # A data e hora de criação da ordem de serviço, com valor padrão para o momento atual
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # A data e hora da última atualização da ordem de serviço, que é atualizada automaticamente sempre que o registro é modificado
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # A chave estrangeira para o cliente associado à ordem de serviço, que é um campo obrigatório (nullable=False) e referencia a tabela "clients"
    client_id = db.Column(
        db.Integer,
        db.ForeignKey("clients.id"),
        nullable=False
    )
