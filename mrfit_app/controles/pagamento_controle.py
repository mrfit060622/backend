from flask import request, jsonify
import os
import mercadopago
from mrfit_app.servicos.mercado_pago_servico import criar_preferencia

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


def consultar_status_pagamento(payment_id):
    """Consulta o status do pagamento e do último log no banco de dados."""
    if not payment_id:
        return None, "ID de pagamento obrigatório"

    pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()
    if not pagamento:
        return None, "Pagamento não encontrado"

    log = LogPagamento.query.filter_by(pagamento_id=pagamento.id)\
        .order_by(LogPagamento.criado_em.desc()).first()

    if not log:
        return None, "Log de pagamento não encontrado"

    return {
        "status": log.status,
        "data_log": log.criado_em
    }, None
