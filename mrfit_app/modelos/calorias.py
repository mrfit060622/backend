from datetime import datetime
from mrfit_app import db

class Caloria(db.Model):
    __tablename__ = 'calorias'

    # Campos da tabela
    id_calorias = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)  # Relacionamento com a tabela usuarios
    valor_calorias = db.Column(db.Float, nullable=False)
    data_calculo = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    id_calorias_novo = db.Column(db.Integer, nullable=False)

    # Relacionamento com a tabela de usuarios
    usuario = db.relationship('Usuario', backref='calorias_usuario', lazy=True)

    def __init__(self, id_usuario, valor_calorias):
        self.id_usuario = id_usuario
        self.valor_calorias = valor_calorias
        self.data_calculo = datetime.utcnow()
    
    def __repr__(self):
        return f"<Caloria(id_calorias={self.id_calorias}, valor_calorias={self.valor_calorias}, data_calculo={self.data_calculo})>"
