from mrfit_app import db

class MedidasPorcao(db.Model):
    __tablename__ = "medidas_porcao"  

    id_medida = db.Column(db.Integer, primary_key=True)
    descricao_medida = db.Column(db.String(100), nullable=False, unique=True)
    kcal = db.Column(db.Float, nullable=True)


class Alimento(db.Model):
    __tablename__ = "alimentos"  # Nome da tabela corrigido

    id_alimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False, unique=True)
    energia_kcal = db.Column(db.Float, nullable=True)
    proteina_g = db.Column(db.Float, nullable=True)
    lipideos_g = db.Column(db.Float, nullable=True)
    colesterol_mg = db.Column(db.Float, nullable=True)
    carboidratos_g = db.Column(db.Float, nullable=True)
    fibra_g = db.Column(db.Float, nullable=True)
    calcio_mg = db.Column(db.Float, nullable=True)
    fosforo_mg = db.Column(db.Float, nullable=True)
    ferro_mg = db.Column(db.Float, nullable=True)
    sodio_mg = db.Column(db.Float, nullable=True)
    potassio_mg = db.Column(db.Float, nullable=True)
    vitamina_c_mg = db.Column(db.Float, nullable=True)

    # Chave estrangeira para GrupoAlimento
    tipo_alimento_id = db.Column(db.Integer, db.ForeignKey("alimentos_grupos.id_grp_alimento"), nullable=False)

    # Relacionamento com GrupoAlimento
    tipo_alimento = db.relationship("GrupoAlimento", back_populates="alimentos")

    def __repr__(self):
        return f"<Alimento {self.descricao}>"
