from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from mrfit_app import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)  # UUID
    payment_id = db.Column(db.String, unique=True, nullable=False)  # ID gerado pelo sistema de pagamento
    status = db.Column(db.String, nullable=True)  # Status do pagamento (ex.: aprovado, pendente)
    valor = db.Column(db.Float, nullable=False)  # Valor do pagamento
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)  # Data do pagamento
    metodo_pagamento = db.Column(db.String, nullable=False)  # Método utilizado (ex.: cartão, boleto)
 