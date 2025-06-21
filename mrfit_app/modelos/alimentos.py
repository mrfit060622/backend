from mrfit_app import db
import enum
from sqlalchemy import Enum


# ---------------------------
# GRUPO DE ALIMENTO
# ---------------------------
class GrupoAlimento(db.Model):
    __tablename__ = "alimentos_grupos"

    id_grp_alimento = db.Column(db.Integer, primary_key=True)
    nm_grp_alimento = db.Column(db.String(100), nullable=False, unique=True)

    # Um grupo tem vários alimentos
    alimentos = db.relationship("Alimento", back_populates="tipo_alimento", lazy="select")

    def __repr__(self):
        return f"<GrupoAlimento {self.nm_grp_alimento}>"

# ---------------------------
# ALIMENTO
# ---------------------------
class Alimento(db.Model):
    __tablename__ = "alimentos"

    id_alimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False, unique=True)
    energia_kcal = db.Column(db.Float, nullable=True)  # kcal por 100g
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

    tipo_alimento_id = db.Column(db.Integer, db.ForeignKey("alimentos_grupos.id_grp_alimento"), nullable=False)
    tipo_alimento = db.relationship("GrupoAlimento", back_populates="alimentos")

    medidas_por_alimento = db.relationship("AlimentoMedida", back_populates="alimento", lazy="select")

    def __repr__(self):
        return f"<Alimento {self.descricao}>"

# ---------------------------
# MEDIDAS PORÇÃO
# ---------------------------
class TipoMedidaEnum(enum.Enum):
    peso = "peso"
    volume = "volume"
    unidade = "unidade"

class MedidasPorcao(db.Model):
    __tablename__ = "medidas_porcao"

    id_medida = db.Column(db.Integer, primary_key=True)
    descricao_medida = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(Enum(TipoMedidaEnum), nullable=False)  # ✅ substituído aqui

    alimentos_medidas = db.relationship("AlimentoMedida", back_populates="medida", lazy="select")

    def __repr__(self):
        return f"<Medida {self.descricao_medida}>"

# ---------------------------
# RELAÇÃO ALIMENTO x MEDIDA
# ---------------------------
class AlimentoMedida(db.Model):
    __tablename__ = "alimento_medida"

    id = db.Column(db.Integer, primary_key=True)
    alimento_id = db.Column(db.Integer, db.ForeignKey("alimentos.id_alimento"), nullable=False)
    medida_id = db.Column(db.Integer, db.ForeignKey("medidas_porcao.id_medida"), nullable=False)
    peso_em_gramas = db.Column(db.Float, nullable=False)

    alimento = db.relationship("Alimento", back_populates="medidas_por_alimento")
    medida = db.relationship("MedidasPorcao", back_populates="alimentos_medidas")

    def __repr__(self):
        return (
            f"<AlimentoMedida {self.alimento.descricao} - "
            f"{self.medida.descricao_medida}: {self.peso_em_gramas}g>"
        )
