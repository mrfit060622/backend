from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class PedidoRelatorio(Base):
    __tablename__ = "pedidos_relatorio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    nome = Column(String)
    idade = Column(Integer)
    peso = Column(Float)
    altura = Column(Float)
    sexo = Column(String)
    atividade = Column(String)
    objetivo = Column(String)
    calorias = Column(Integer)
    codigo_pdf = Column(String)
    pago = Column(Boolean, default=False)
    data_solicitacao = Column(DateTime, default=datetime.utcnow)
