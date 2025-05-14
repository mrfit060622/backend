import mercadopago
from mercadopago.config import RequestOptions
import os
from mrfit_app import db
from datetime import datetime
from mrfit_app.modelos.pagamento import Pagamento

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
sdk = mercadopago.SDK(ACCESS_TOKEN)


def criar_pagamento_transparente(email, valor, nome, sobrenome, nr_cpf, metodo_pagamento,
                                  parcelamento, issuer_id, token, tp_doc, uuid_requisicao):
    """Cria um pagamento via Pix, Cartão de Crédito ou Débito"""
    metodo_pagamento = metodo_pagamento.lower()
    request_options = RequestOptions()
    request_options.custom_headers = {
        'x-idempotency-key': uuid_requisicao
    }

    if metodo_pagamento == "pix":
        pagamento_dados = {
            "transaction_amount": float(valor),
            "description": f"Pagamento - {nome}",
            "payment_method_id": "pix",
            "payer": {
                "email": email
            },
            "external_reference": uuid_requisicao
        }
    else:
        if not token:
            return {"erro": "Token de cartão obrigatório para pagamento com cartão"}, 400

        pagamento_dados = {
            "transaction_amount": float(valor),
            "token": token,
            "payment_method_id": metodo_pagamento,
            "description": f"Pagamento - {nome}",
            "installments": int(parcelamento),
            "external_reference": uuid_requisicao,
            "issuer_id": issuer_id,
            "payer": {
                "email": email,
                "first_name": nome,
                "last_name": sobrenome,
                "identification": {
                    "type": tp_doc,
                    "number": nr_cpf
                }
            }
        }

    try:
        resultado = sdk.payment().create(pagamento_dados, request_options)
    except Exception as e:
        return {"erro": "Erro ao conectar com a API do Mercado Pago", "detalhes": str(e)}, 500
##Saida
    if resultado.get("status") == 201:
                response_data = resultado["response"]
                init_point = response_data.get("init_point")
    
                pagamento = Pagamento(
                    external_reference=uuid_requisicao,
                    status='Aguardando pagamento',
                    data_pagamento=datetime.utcnow(),
                    email_pago=email
                )
                db.session.add(pagamento)
                db.session.commit()
                print("💾 Pagamento salvo com sucesso.")
                print ("🔑 ID da preferência:", response_data.get ("id"))
                return {
                    "status": "success",
                    "init_point": init_point,
                    "external_reference": uuid_requisicao
                }
    else:
        return {
            "status": "error",
            "message": "Erro na resposta do Mercado Pago",
            "error_detail": resultado
        }
            
    
##Chegada
    # if resultado.get("status") != 201:
    #     return {
    #         "erro": resultado.get("message", "Erro ao processar pagamento"),
    #         "detalhes": resultado
    #     }, resultado.get("status", 400)

    # response = resultado["response"]
    # external_reference = response.get("external_reference")

    # pagamento_db = Pagamento(
    #     uuid_requisicao=external_reference,
    #     status=response.get("status", "Aguardando pagamento"),
    #     data_pagamento=datetime.utcnow(),
    #     email_pago=email,
    #     valor=valor,
    #     metodo_pagamento=metodo_pagamento,
    #     payment_id=response.get("id")
    # )
    # db.session.add(pagamento_db)
    # db.session.commit()

    # print("💾 Pagamento salvo com sucesso.")
    # print("🔑 ID do pagamento:", response.get("id"))

    # retorno = {
    #     "status": "success",
    #     "payment_id": response.get("id"),
    #     "external_reference": external_reference,
    #     "status_pagamento": response.get("status"),
    # }

    # # Se for PIX, incluir dados adicionais
    # poi = response.get("point_of_interaction", {})
    # tx_data = poi.get("transaction_data", {})

    # if metodo_pagamento == "pix":
    #     retorno["qr_code"] = tx_data.get("qr_code")
    #     retorno["ticket_url"] = tx_data.get("ticket_url")
    # elif tx_data.get("ticket_url"):
    #     retorno["ticket_url"] = tx_data["ticket_url"]

    # return retorno
