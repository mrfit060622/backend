from mrfit_app import db

class TipoAlimento(db.Model):
    __tablename__ = "tipos_alimento"  # Nome da tabela corrigido

    id_tp_alimento = db.Column(db.Integer, primary_key=True)  # ID do tipo de alimento
    tp_alimento = db.Column(db.String(100), nullable=False, unique=True)  # Nome do tipo (Ex: Proteínas, Carboidratos)

    # Relacionamento com Alimento
    alimentos = db.relationship("Alimento", back_populates="tipo_alimento", lazy=True)

    def __repr__(self):
        return f"<TipoAlimento {self.tp_alimento}>"


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

    # Chave estrangeira para TipoAlimento
    tipo_alimento_id = db.Column(db.Integer, db.ForeignKey("tipos_alimento.id_tp_alimento"), nullable=False)

    # Relacionamento com TipoAlimento
    tipo_alimento = db.relationship("TipoAlimento", back_populates="alimentos")

    def __repr__(self):
        return f"<Alimento {self.descricao}>"
