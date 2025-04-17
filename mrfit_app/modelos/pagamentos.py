import uuid
from datetime import datetime
from mrfit_app import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)
    uuid_requisicao = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(100), nullable=True)
    payment_id = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pagamento = db.Column(db.String(50), nullable=False)
    parcelamento = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default="pendente")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    logs = db.relationship("LogPagamento", backref="pagamento", lazy=True)

    def __repr__(self):
        return f"<Pagamento {self.payment_id} - {self.status}>"


class LogPagamento(db.Model):
    __tablename__ = "logs_pagamento"

    id = db.Column(db.Integer, primary_key=True)
    uuid_requisicao = db.Column(db.String(36), nullable=False)
    pagamento_id = db.Column(db.Integer, db.ForeignKey("pagamentos.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    detalhes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LogPagamento {self.pagamento_id} - {self.status}>"
