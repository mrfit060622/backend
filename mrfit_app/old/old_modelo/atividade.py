from mrfit_app import db

class Atividade(db.Model):
    __tablename__ = 'atividades'
    
    cd_atividade = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False, unique=True)
    
    usuarios = db.relationship('Usuario', back_populates='atividade', lazy=True)
