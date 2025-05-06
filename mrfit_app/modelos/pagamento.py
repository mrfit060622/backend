from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from mrfit_app import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String, nullable=True)
    tipo = db.Column(db.String, nullable=True)
    payment_id = db.Column(db.BigInteger, nullable=True, unique=True)
    external_reference = db.Column(db.String, nullable=False, unique=True)
    valor = db.Column(db.Float, nullable=True)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pagamento = db.Column(db.String, nullable=True)
    parcelamento = db.Column(db.Integer, nullable=True)
    email_pago = db.Column(db.String, nullable=True)
 