from flask import Blueprint, request, jsonify
from mrfit_app import db

bp_notificacoes = Blueprint("notificacoes", __name__)

@bp_notificacoes.route("/mercado-pago", methods=["POST"])
def notificacao_mercado_pago():
    dados = request.get_json()

    # Validação do corpo da requisição
    if not dados:
        return jsonify({"erro": "Corpo da requisição vazio"}), 400

    tipo = dados.get("type")
    payment_id = dados.get("data", {}).get("payment_id")

    # Validação do tipo e ID de pagamento
    if tipo != "payment" or not payment_id:
        return jsonify({"erro": "Notificação inválida"}), 400

    try:
        # Consulta o pagamento atualizado no Mercado Pago
        status_atual = consultar_status_pagamento(payment_id)

        if not status_atual:
            return jsonify({"erro": "Pagamento não encontrado"}), 404

        # Atualiza o status do pagamento no banco de dados
        pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()
        if not pagamento:
            return jsonify({"erro": "Pagamento não registrado localmente"}), 404

        pagamento.status = status_atual["status"]
        db.session.commit()

        # Salva log de pagamento
        salvar_log_pagamento(
            pagamento_id=pagamento.id,
            status=status_atual["status"],
            detalhes=status_atual.get("status_detail", "")
        )

        return jsonify({"mensagem": "Notificação recebida e processada com sucesso"}), 200

    except Exception as e:
        # Tratamento genérico de erros
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500