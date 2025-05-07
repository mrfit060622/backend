from mrfit_app.modelos.relatorio import Relatorio
from mrfit_app.modelos.relatorio_gratis import RelatorioGratuito
from sqlalchemy.orm import Session
from datetime import datetime
def registrar_pedido_relatorio(db: Session, data: dict, external_reference: str, pagamento_id: str):
    try:
        relatorio = Relatorio(
            email=data.get('email'),
            nome=data.get('nome'),
            idade=int(data.get('idade')) if data.get('idade') else None,
            peso=float(data.get('peso')) if data.get('peso') else None,
            altura=float(data.get('altura')) if data.get('altura') else None,
            sexo=data.get('sexo'),
            atividade=data.get('atividade'),
            objetivo=data.get('objetivo'),
            calorias=int(data.get('calorias')) if data.get('calorias') else None,
            data_pagamento=datetime.utcnow(),
            data_solicitacao=datetime.utcnow(),
            external_reference=external_reference  # Referência ao pagamento
        )

        db.add(relatorio)
        db.commit()
        return None  # Sucesso

    except Exception as e:
        db.rollback()
        return str(e)  # Retorna o erro como string
def registrar_pedido_relatorio_gratis(db: Session, data: dict):
    try:
        relatorio_gratis = RelatorioGratuito(
            email=data.get('email'),
            nome=data.get('nome'),
            idade=int(data.get('idade')) if data.get('idade') else None,
            peso=float(data.get('peso')) if data.get('peso') else None,
            altura=float(data.get('altura')) if data.get('altura') else None,
            sexo=data.get('sexo'),
            atividade=data.get('atividade'),
            objetivo=data.get('objetivo'),
            calorias=int(data.get('calorias')) if data.get('calorias') else None
        )

        db.add(relatorio_gratis)
        db.commit()
        return None  # Sucesso

    except Exception as e:
        db.rollback()
        return str(e)  # Retorna o erro como string