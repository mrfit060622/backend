from datetime import datetime
from mrfit_app import db

class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)  # Usando Numeric para precisão
    metodo_pagamento = db.Column(db.String(50), nullable=False)  # Ex: "pix", "visa", "mastercard"
    parcelamento = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default="pendente")  # Ex: "aprovado", "pendente", "rejeitado"
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    logs = db.relationship("LogPagamento", backref="pagamento", lazy=True)  # Relacionamento

    def __repr__(self):
        return f"<Pagamento {self.payment_id} - {self.status}>"
    
class LogPagamento(db.Model):
    __tablename__ = "logs_pagamento"

    id = db.Column(db.Integer, primary_key=True)
    pagamento_id = db.Column(db.Integer, db.ForeignKey("pagamentos.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # "pendente", "aprovado", "rejeitado"
    detalhes = db.Column(db.Text, nullable=True)  # Motivo da rejeição, erros, etc.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<LogPagamento {self.pagamento_id} - {self.status}>"
