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
    transaction_amount = data.get("transactionAmount")
    description = data.get("description")
    payer_email = data.get("payerEmail")
    payer_name = data.get("payerName")
    payment_method = data.get("paymentMethod")

    # Cria preferência no Mercado Pago
    preference = criar_preferencia(
        ACCESS_TOKEN,
        transaction_amount,
        description,
        payer_email,
        payer_name
    )

    if preference['status'] == 201:
        response = preference['response']
        init_point = response.get('init_point')
        id_preferencia = response.get('id')

        # Salva o relatório com base nos dados recebidos
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
            id_preferencia=id_preferencia,
            pagamento_id=None
        )

        if erro:
            return jsonify({'status': 'error', 'message': 'Erro ao registrar relatório', 'detail': erro}), 500

        return jsonify({'status': 'success', 'init_point': init_point})

    return jsonify({
        'status': 'error',
        'message': 'Erro ao criar preferência de pagamento',
        'error_detail': preference
    })

def consultar_status_pagamento(payment_id):
    """Consulta o status do pagamento na API externa."""
    if not payment_id:
        return {"erro": "ID de pagamento obrigatório"}, 400

    return verificar_pagamento(payment_id)


def verificar_pagamento(payment_id):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            pagamento_detalhes = response.json()
            return pagamento_detalhes  # <- Retornar o JSON para usar na outra função
            pagamento_detalhes
        else:
            print(f"Erro na consulta: Status {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Erro ao verificar pagamento: {str(e)}")
        return None

