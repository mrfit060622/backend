from mrfit_app.modelos.pedido_relatorio import PedidoRelatorio
from sqlalchemy.orm import Session

def registrar_pedido_relatorio(db: Session, data: dict, codigo_pdf: str, pago=False):
    try:
        pedido = PedidoRelatorio(
            email=data.get('email'),
            nome=data.get('nome'),
            idade=int(data.get('idade')) if data.get('idade') else None,
            peso=float(data.get('peso')) if data.get('peso') else None,
            altura=float(data.get('altura')) if data.get('altura') else None,
            sexo=data.get('sexo'),
            atividade=data.get('atividade'),
            objetivo=data.get('objetivo'),
            calorias=int(data.get('calorias')) if data.get('calorias') else None,
            codigo_pdf=codigo_pdf,
            pago=pago
        )

        db.add(pedido)
        db.commit()
        return None

    except Exception as e:
        db.rollback()
        return str(e)
