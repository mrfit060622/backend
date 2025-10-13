from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from mrfit_app import db

class Relatorio(db.Model):
    __tablename__ = "relatorios"

    id_relatorio_pg = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    nome = db.Column(db.String)
    idade = db.Column(db.Integer)
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    sexo = db.Column(db.String)
    atividade = db.Column(db.String)
    objetivo = db.Column(db.String)
    calorias = db.Column(db.Integer)
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_pagamento = db.Column(db.DateTime, nullable=False)
    external_reference = db.Column(db.String, db.ForeignKey('pagamentos.external_reference'), nullable=False)
    pagamento = db.relationship('Pagamento', backref='relatorios', lazy=True)
    