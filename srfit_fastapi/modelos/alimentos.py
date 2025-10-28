from mrfit_app import db

class TipoAlimento(db.Model):
    __tablename__ = "tipos_"  # Nome da tabela para tipos de 
    
    id_tp_alimento = db.Column(db.Integer, primary_key=True)  # Identificador único para o tipo de alimento
    tp_alimento = db.Column(db.String(100), nullable=False, unique=True)  # Nome do tipo de alimento
    
    # Relacionamento com 
     = db.relationship("Alimento", back_populates="tipo_alimento", lazy=True)  # Ajustado para 'tipo_alimento'
    
    def __repr__(self):
        return f"<TipoAlimento {self.tp_alimento}>"

class Alimento(db.Model):
    __tablename__ = ""  # Nome da tabela para 
    
    id_alimento = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Identificador único para o alimento
    descricao = db.Column(db.String(255), nullable=False, unique=True)  # Descrição do alimento
    energia_kcal = db.Column(db.Float, nullable=True)  # Energia em kcal
    proteina_g = db.Column(db.Float, nullable=True)  # Proteínas em gramas
    lipideos_g = db.Column(db.Float, nullable=True)  # Lipídios em gramas
    colesterol_mg = db.Column(db.Float, nullable=True)  # Colesterol em mg
    carboidratos_g = db.Column(db.Float, nullable=True)  # Carboidratos em gramas
    fibra_g = db.Column(db.Float, nullable=True)  # Fibras em gramas
    calcio_mg = db.Column(db.Float, nullable=True)  # Cálcio em mg
    fosforo_mg = db.Column(db.Float, nullable=True)  # Fósforo em mg
    ferro_mg = db.Column(db.Float, nullable=True)  # Ferro em mg
    sodio_mg = db.Column(db.Float, nullable=True)  # Sódio em mg
    potassio_mg = db.Column(db.Float, nullable=True)  # Potássio em mg
    vitamina_c_mg = db.Column(db.Float, nullable=True)  # Vitamina C em mg
    
    # Chave estrangeira para tipos_
    tipo_alimento_id = db.Column(db.Integer, db.ForeignKey("tipos_.id_tp_alimento"), nullable=False)
    
    # Relacionamento com TipoAlimento
    tipo_alimento = db.relationship("TipoAlimento", back_populates="")  # Correto
