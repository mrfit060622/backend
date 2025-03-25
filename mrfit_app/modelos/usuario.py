from mrfit_app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Importando Objetivo e Atividade sem criar um loop
from mrfit_app.modelos.objetivo import Objetivo
from mrfit_app.modelos.atividade import Atividade

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    idade = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)
    sexo = db.Column(db.String(10), nullable=True)
    # Chaves estrangeiras
    cd_objetivo = db.Column(db.Integer, db.ForeignKey('objetivos.cd_objetivo'), nullable=True)
    cd_atividade = db.Column(db.Integer, db.ForeignKey('atividades.cd_atividade'), nullable=True)

    # Relacionamentos
    objetivo = db.relationship("Objetivo", back_populates="usuarios")  
    atividade = db.relationship("Atividade", back_populates="usuarios")

    def set_password(self, senha):
        """Criptografa a senha antes de salvar."""
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica a senha criptografada."""
        return check_password_hash(self.senha, senha)
