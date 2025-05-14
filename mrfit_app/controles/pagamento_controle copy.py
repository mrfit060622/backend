from flask import request, jsonify
import os
import mercadopago
from mrfit_app.servicos.mercado_pago_servico import criar_preferencia
from mrfit_app.servicos.registro_pedido_servico import registrar_pedido_relatorio
from mrfit_app.modelos.pagamento import Pagamento
from mrfit_app.modelos.relatorio import Relatorio
from mrfit_app import db
from datetime import datetime
import requests

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

def checkout():
    data = request.get_json()

    try:
        transaction_amount = data["transactionAmount"]
        description = data["description"]
        payer_email = data["payerEmail"]
        payer_name = data["payerName"]
        # pagamento_id será gerado após o pagamento, não agora

        # Criar preferência
        resultado = criar_preferencia(
            transaction_amount,
            description,
            payer_email,
            payer_name
        )

        if resultado["status"] != "success":
            return jsonify({
                "status": "error",
                "message": resultado.get("message"),
                "detail": resultado.get("error_detail")
            }), 400

        init_point = resultado.get("init_point")
        external_reference = resultado.get("external_reference")

        # Salvar relatório
        erro = registrar_pedido_relatorio(
            db.session,
            data={
                'email': payer_email,
                'nome': payer_name,
                'idade': data.get('idade'),
                'peso': data.get('peso'),
                'altura': data.get('altura'),
                'sexo': data.get('sexo'),
                'atividade': data.get('atividade'),
                'objetivo': data.get('objetivo'),
                'calorias': data.get('calorias')
            },
            external_reference=external_reference,
            pagamento_id=None
        )

        if erro:
            return jsonify({
                "status": "error",
                "message": "Erro ao registrar relatório",
                "detail": erro
            }), 500

        return jsonify({
            "status": "success",
            "init_point": init_point,
            "external_reference": external_reference,
            "preference_id": resultado.get("preference_id")
        }), 200

    except KeyError as ke:
        return jsonify({
            "status": "error",
            "message": f"Campo obrigatório ausente: {str(ke)}"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Erro inesperado ao processar o checkout",
            "detail": str(e)
        }), 500

def consultar_status_pagamento(payment_id):
    """Consulta o status do pagamento na API externa."""
    if not payment_id:
        return {"erro": "ID de pagamento obrigatório"}, 400

    pagamento_detalhes = verificar_pagamento(payment_id)

    if pagamento_detalhes is None:
        return {"erro": "Erro ao consultar status do pagamento"}, 500

    return jsonify(pagamento_detalhes), 200

def verificar_pagamento(payment_id):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # Retorna o JSON com os detalhes do pagamento
        else:
            print(f"Erro na consulta: Status {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Erro ao verificar pagamento: {str(e)}")
        return None

   