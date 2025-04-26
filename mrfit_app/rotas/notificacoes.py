from flask import Blueprint, request, jsonify
from mrfit_app.controles.pagamento_controle import verificar_pagamento
from mrfit_app.modelos.pagamento import Pagamento
from mrfit_app import db

bp_notificacoes = Blueprint("notificacoes", __name__)

@bp_notificacoes.route("/mercado-pago", methods=["POST"])
def notificacao_mercado_pago():
    dados = request.get_json()

    # Validação do corpo da requisição
    if not dados:
        return jsonify({"erro": "Corpo da requisição vazio"}), 400

    tipo = dados.get("type")
    payment_id = dados.get("data", {}).get("id")  # ID enviado pela notificação
    acao_recebida = dados.get("action")  # Exemplo: "payment.updated"

    # Validação do tipo e ID de pagamento
    if tipo != "payment" or not payment_id:
        return jsonify({"erro": "Notificação inválida"}), 400

    try:
        # Buscar pagamento pelo payment_id
        pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()

        if not pagamento:
            return jsonify({"erro": "Pagamento não encontrado"}), 404

        # Verificar o status real do pagamento via API (se necessário)
        status_real = verificar_pagamento(payment_id)  # Função para buscar o status real
        if status_real:
            pagamento.status = status_real
        else:
            pagamento.status = "Desconhecido"  # Default caso não consiga buscar o status

        db.session.commit()

        return jsonify({"mensagem": "Pagamento atualizado com sucesso"}), 200

    except Exception as e:
        # Tratamento genérico de erros
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500