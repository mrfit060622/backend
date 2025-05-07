from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from mrfit_app import db

class RelatorioGratuito(db.Model):
    __tablename__ = "relatorio_gratis"

    id_relatorio_gratis = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
