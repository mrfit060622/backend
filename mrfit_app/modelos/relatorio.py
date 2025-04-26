from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from mrfit_app import db

class Relatorio(db.Model):
    __tablename__ = "relatorios"

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)  # UUID
    email = db.Column(db.String, nullable=False)
    nome = db.Column(db.String)
    idade = db.Column(db.Integer)
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    sexo = db.Column(db.String)
    atividade = db.Column(db.String)
    objetivo = db.Column(db.String)
    calorias = db.Column(db.Integer)
    codigo_pdf = db.Column(db.String)  # Código do relatório em PDF
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)  # Data da solicitação
    pagamento_id = db.Column(db.Integer, db.ForeignKey('pagamentos.id'), nullable=False)  # Referência ao pagamento