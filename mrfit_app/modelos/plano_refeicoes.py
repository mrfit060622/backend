from mrfit_app import db

class PlanoRefeicaoAlimento(db.Model):
    __tablename__ = "plano_refeicao_alimento"

    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos_caloricos.id"), nullable=False)
    refeicao_id = db.Column(db.Integer, db.ForeignKey("refeicoes.id"), nullable=False)
    alimento_id = db.Column(db.Integer, db.ForeignKey("alimentos.id_alimento"), nullable=False)
    medida_id = db.Column(db.Integer, db.ForeignKey("medidas_porcao.id_medida"), nullable=False)
    quantidade = db.Column(db.Float, nullable=False, default=1.0)

    __table_args__ = (
        db.Index("ix_plano_refeicao", "plano_id", "refeicao_id"),
    )

    plano = db.relationship("PlanoCalorico", back_populates="refeicoes_alimentos")
    refeicao = db.relationship("Refeicao", back_populates="alimentos_plano")
    alimento = db.relationship("Alimento", lazy="joined")
    medida = db.relationship("MedidasPorcao", lazy="joined")

    def __repr__(self):
        return f"<PlanoRefeicaoAlimento plano_id={self.plano_id}, refeicao_id={self.refeicao_id}, alimento_id={self.alimento_id}, medida_id={self.medida_id}, qtd={self.quantidade}>"


class PlanoCalorico(db.Model):
    __tablename__ = "planos_caloricos"

    id = db.Column(db.Integer, primary_key=True)
    kcal_total = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(100), nullable=True)


    refeicoes_alimentos = db.relationship("PlanoRefeicaoAlimento", back_populates="plano", lazy=True)

    def __repr__(self):
        return f"<PlanoCalorico {self.kcal_total} kcal>"


class Refeicao(db.Model):
    __tablename__ = "refeicoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)  # Ex: café da manhã, almoço
    ordem = db.Column(db.Integer, nullable=True)  # Ex: 1 = café da manhã, 5 = ceia

    alimentos_plano = db.relationship("PlanoRefeicaoAlimento", back_populates="refeicao", lazy=True)

    def __repr__(self):
        return f"<Refeicao {self.nome}>"
