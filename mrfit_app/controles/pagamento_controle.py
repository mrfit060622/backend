from flask import request, jsonify
import os
import mercadopago
from mrfit_app.servicos.mercado_pago_servico import criar_preferencia
from mrfit_app.modelos.pagamento import Pagamento
from mrfit_app.modelos.relatorio import Relatorio
from datetime import datetime
from mrfit_app import db
import requests

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

def checkout():
    # Recebe os dados enviados pelo front-end
    payment_data = request.get_json()
    transaction_amount = payment_data.get("transactionAmount")
    description = payment_data.get("description")
    payer_email = payment_data.get("payerEmail")
    payer_name = payment_data.get("payerName")
    payment_method = payment_data.get("paymentMethod")

    # Cria preferência de pagamento usando o serviço
    preference = criar_preferencia(ACCESS_TOKEN, transaction_amount, description, payer_email, payer_name)

    # Retorna a resposta
    if preference['status'] == 201:
        init_point = preference['response']['init_point']
        payment_id = preference['response']['id']  # ID único do pagamento

        # Insere na tabela de pagamentos
        novo_pagamento = Pagamento(
            payment_id=payment_id,
            valor=transaction_amount,
            metodo_pagamento=payment_method,
            status="Pendente",
            data_pagamento=datetime.utcnow(),
        )
        db.session.add(novo_pagamento)
        db.session.commit()

        # Insere na tabela de relatórios
        novo_relatorio = Relatorio(
            pagamento_id=novo_pagamento.id,  # Referência ao pagamento
            email=payer_email,
            nome=payer_name,
            data_solicitacao=datetime.utcnow(),
        )
        db.session.add(novo_relatorio)
        db.session.commit()

        return jsonify({'status': 'success', 'init_point': init_point})
    else:
        return jsonify({
            'status': 'error',
            'message': 'Erro ao criar preferência de pagamento',
            'error_detail': preference
        })

def processar_consulta(payment_id):
    """Consulta o status do pagamento na API externa."""
    if not payment_id:
        return {"erro": "ID de pagamento obrigatório"}, 400

    return verificar_pagamento(payment_id)

def verificar_pagamento(payment_id):
    ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            return dados.get("status")  # Status: "approved", "pending", "rejected", etc.
        else:
            return None
    except Exception as e:
        print(f"Erro ao verificar pagamento: {str(e)}")
        return None