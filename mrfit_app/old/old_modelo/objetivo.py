from mrfit_app import db

class Objetivo(db.Model):
    __tablename__ = 'objetivos'
    
    cd_objetivo = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False, unique=True)
    
    usuarios = db.relationship('Usuario', back_populates='objetivo', lazy=True)
