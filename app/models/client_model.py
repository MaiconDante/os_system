from app import db

class Client(db.Model):
    # Define the table name for the Client model
    __tablename__ = "clients"

    # Define the columns for the Client model
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # The name of the client, which is a required field (nullable=False)
    name = db.Column(db.String(100), nullable=False)

    # The phone number of the client, which is an optional field (nullable=True)
    phone = db.Column(db.String(20))

    # The email address of the client, which is an optional field (nullable=True)
    email = db.Column(db.String(120))

    # The date and time when the client record was created, with a default value of the current time
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Client {self.name}>"
    