import mercadopago
import os
from mrfit_app import db
from mrfit_app.modelos.pagamentos import Pagamento, LogPagamento
from datetime import datetime
import logging


ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
sdk = mercadopago.SDK(ACCESS_TOKEN)

def criar_pagamento_transparente(nome, email, valor, metodo_pagamento, parcelamento=1, token=None):
    """Cria um pagamento via Pix, Cartão de Crédito ou Débito"""

    if metodo_pagamento.lower() == "pix":
        pagamento_dados = {
            "transaction_amount": float(valor),
            "description": f"Pagamento - {nome}",
            "payment_method_id": "pix",
            "payer": {
                "email": email,
                "first_name": nome
            }
        }
    else:
        if not token:
            return {"erro": "Token de cartão obrigatório para pagamento com cartão"}, 400

        pagamento_dados = {
            "transaction_amount": float(valor),
            "description": f"Pagamento - {nome}",
            "installments": int(parcelamento),
            "token": token,
            "payer": {
                "email": email,
                "first_name": nome,
                "identification": {
                    "type": "CPF",
                    "number": "40841868808"
                }
            }
        }

    logging.info(f"Dados do pagamento enviados: {pagamento_dados}")
    
    pagamento = sdk.payment().create(pagamento_dados)
    logging.info(f"Resposta da API do MercadoPago: {pagamento}")
    
    resposta = pagamento.get("response", {})

    if "id" not in resposta:
        erro_msg = resposta.get("message", "Erro ao processar pagamento")
        logging.error(f"Erro ao processar pagamento. Mensagem: {erro_msg}, Detalhes: {resposta}")
        return {"erro": erro_msg, "detalhes": resposta}, 400

    retorno = {
        "payment_id": resposta["id"],
        "status": resposta["status"],
        "status_detail": resposta.get("status_detail")
    }

    # Dados adicionais (Pix ou boleto)
    poi = resposta.get("point_of_interaction", {})
    tx_data = poi.get("transaction_data", {})

    if metodo_pagamento.lower() == "pix":
        retorno["qr_code"] = tx_data.get("qr_code")
        retorno["ticket_url"] = tx_data.get("ticket_url")
    elif tx_data.get("ticket_url"):
        retorno["ticket_url"] = tx_data["ticket_url"]

    # Salvar no banco
    salvar_pagamento_no_banco(
        payment_id=resposta["id"],
        nome=nome,
        email=email,
        valor=valor,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        status=resposta["status"],
        status_detail=resposta.get("status_detail")
    )

    return retorno


def consultar_status_pagamento(payment_id):
    """Consulta o status do pagamento pelo ID"""
    pagamento = sdk.payment().get(payment_id)
    resposta = pagamento["response"]
    return {
        "payment_id": resposta["id"],
        "status": resposta["status"],
        "status_detail": resposta["status_detail"]
    }

def salvar_pagamento_no_banco(payment_id, nome, email, valor, metodo_pagamento, parcelamento, status, status_detail):
    """Salva o pagamento e seu log no banco de dados."""
    
    # Criação do pagamento
    pagamento = Pagamento(
        payment_id=payment_id,
        nome=nome,
        email=email,
        valor=valor,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        status=status,
    )
    db.session.add(pagamento)
    db.session.flush()  # Garante que o pagamento.id esteja disponível para o LogPagamento

    # Criação do log
    log = LogPagamento(
        pagamento_id=pagamento.id,
        status=status,
        detalhes=status_detail
    )
    db.session.add(log)
    db.session.commit()

def salvar_log_pagamento(pagamento_id, status, detalhes):
    log = LogPagamento(
        pagamento_id=pagamento_id,
        status=status,
        detalhes=detalhes,
        criado_em=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()