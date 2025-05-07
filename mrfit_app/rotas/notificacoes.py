from flask import Blueprint, request, jsonify
from mrfit_app.controles.pagamento_controle import verificar_pagamento
from mrfit_app.modelos.pagamento import Pagamento
from datetime import datetime
from mrfit_app import db

bp_notificacoes = Blueprint("notificacoes", __name__)
@bp_notificacoes.route("/mercado-pago", methods=["POST"])
def notificacao_mercado_pago():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Corpo da requisição vazio"}), 400

    tipo = dados.get("type")
    payment_id = dados.get("data", {}).get("id")
    action = dados.get("action")

    print(f"[Webhook] Tipo: {tipo}, Payment ID: {payment_id}, Action: {action}")

    if tipo != "payment" or not payment_id:
        return jsonify({"erro": "Notificação inválida"}), 400

    try:
        # Consulta o Mercado Pago com o ID do pagamento
        dados_pagamento = verificar_pagamento(payment_id)

        if not dados_pagamento:
            print("[Webhook] Pagamento não encontrado na API do MP")
            return jsonify({"erro": "Pagamento não encontrado"}), 404

        external_reference = dados_pagamento.get("external_reference")

        if not external_reference:
            print("[Webhook] external_reference ausente")
            return jsonify({"erro": "external_reference ausente"}), 400

        # Agora busca o pagamento pela referência externa
        print (f"[Webhook] Buscando pagamento com external_reference={external_reference}")
        pagamento = Pagamento.query.filter_by(external_reference=external_reference).first()

        if not pagamento:
            print(f"[Webhook] Nenhum pagamento encontrado para external_reference={external_reference}")
            return jsonify({"erro": "Pagamento não encontrado no banco"}), 404

        # Atualiza o registro existente
        pagamento.payment_id = payment_id
        pagamento.metodo_pagamento = dados_pagamento.get("payment_method_id")
        pagamento.valor = dados_pagamento.get("transaction_amount")
        pagamento.parcelamento = dados_pagamento.get("installments")
        pagamento.status = dados_pagamento.get("status")
        pagamento.data_pagamento = datetime.utcnow()
        pagamento.tipo = tipo

        db.session.commit()

        print(f"[Webhook] Pagamento atualizado com sucesso para external_reference={external_reference}")
        return jsonify({"mensagem": "Notificação processada com sucesso"}), 200

    except Exception as e:
        print(f"[Webhook] Erro inesperado: {str(e)}")
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500



def completa_pagamento(payment_id, tipo):
    try:
        dados_pagamento = verificar_pagamento(payment_id)

        if not dados_pagamento:
            print("Pagamento não encontrado no Mercado Pago")
            return

        # Extrai os dados
        email = dados_pagamento.get("payer", {}).get("email")
        metodo_pagamento = dados_pagamento.get("payment_method_id")
        valor = dados_pagamento.get("transaction_amount")
        parcelamento = dados_pagamento.get("installments")
        status = dados_pagamento.get("status")

        print(f"Detalhes: {email}, {metodo_pagamento}, {valor}, {parcelamento}, {status}, {tipo}")

        pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()

        if pagamento:
            pagamento.email_pago = email
            pagamento.metodo_pagamento = metodo_pagamento
            pagamento.valor = valor
            pagamento.parcelamento = parcelamento
            pagamento.status = status
            pagamento.data_pagamento = datetime.utcnow()
            pagamento.tipo = tipo
            db.session.commit()
        else:
            print(f"Nenhum registro encontrado no banco para payment_id={payment_id}")
    except Exception as e:
        print(f"Erro ao completar pagamento: {e}")
