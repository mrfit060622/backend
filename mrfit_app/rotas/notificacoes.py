from flask import Blueprint, request, jsonify
from mrfit_app.servicos.pagamento_servico import consultar_status_pagamento, salvar_log_pagamento
from mrfit_app.modelos.pagamentos import Pagamento
from mrfit_app import db

bp_notificacoes = Blueprint("notificacoes", __name__)

@bp_notificacoes.route("/mercado-pago", methods=["POST"])
def notificacao_mercado_pago():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Corpo da requisição vazio"}), 400

    tipo = dados.get("type")
    payment_id = dados.get("data", {}).get("payment_id")

    if tipo != "payment" or not payment_id:
        return jsonify({"erro": "Notificação inválida"}), 400

    # Consulta o pagamento atualizado no Mercado Pago
    status_atual = consultar_status_pagamento(payment_id)

    if not status_atual:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    # Atualiza no banco
    pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()
    if not pagamento:
        return jsonify({"erro": "Pagamento não registrado localmente"}), 404

    pagamento.status = status_atual["status"]
    db.session.commit()

    # Salva novo log
    salvar_log_pagamento(
        pagamento_id=pagamento.id,
        status=status_atual["status"],
        detalhes=status_atual.get("status_detail", "")
    )

    return jsonify({"mensagem": "Notificação recebida e processada com sucesso"}), 200
