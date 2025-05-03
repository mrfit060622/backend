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

    print(f"Tipo: {tipo}, Payment ID: {payment_id}, Action: {action}")

    if tipo != "payment" or not payment_id:
        return jsonify({"erro": "Notificação inválida"}), 400

    try:
        # Primeiro: verifica se já existe no banco
        pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()

        if not pagamento:
            # Cria um novo objeto Pagamento com status inicial
            pagamento = Pagamento(payment_id=payment_id, status=action)
            db.session.add(pagamento)
            db.session.commit()  # <- IMPORTANTE: garantir que o registro existe no banco

        else:
            # Atualiza o status se já existe
            pagamento.status = action
            db.session.commit()

        # Agora o pagamento existe -> podemos completar os dados
        completa_pagamento(payment_id, tipo)

        return jsonify({"mensagem": "Notificação processada e pagamento atualizado"}), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao processar notificação: {str(e)}"}), 500


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
