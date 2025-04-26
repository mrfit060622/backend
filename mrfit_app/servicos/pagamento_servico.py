
from sqlalchemy.exc import SQLAlchemyError
from modelos.pedido_relatorio import PedidoRelatorio
from mrfit_app import db

def registrar_pagamento(email, codigo_pagamento):
    """Registra um pagamento no banco de dados."""
    session = SessionLocal()
    try:
        pagamento_existente = session.query(Pagamento).filter_by(email=email).first()
        if pagamento_existente:
            pagamento_existente.codigo_pagamento = codigo_pagamento
        else:
            novo_pagamento = Pagamento(email=email, codigo_pagamento=codigo_pagamento)
            session.add(novo_pagamento)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erro ao registrar pagamento: {e}")
    finally:
        session.close()

def verificar_pagamento(email):
    """Verifica se o pagamento do usuário já foi registrado."""
    session = SessionLocal()
    try:
        return session.query(Pagamento).filter_by(email=email).first() is not None
    except SQLAlchemyError as e:
        print(f"Erro ao verificar pagamento: {e}")
        return False
    finally:
        session.close()
