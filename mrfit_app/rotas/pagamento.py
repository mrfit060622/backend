from flask import Blueprint, request, jsonify, redirect
import mercadopago
from mrfit_app.controles.pagamento_controle import checkout

pagamento_bp = Blueprint("pagamento", __name__)

# Definindo a rota com o método POST
pagamento_bp.route('/checkout', methods=['POST'])(checkout)

@pagamento_bp.route("/status_pagamento/<payment_id>", methods=["GET"])
def status_pagamento(payment_id):
    """Consulta o status do pagamento pelo ID no banco de dados."""
    try:
        resultado, erro = consultar_status_pagamento(payment_id)
        if erro:
            return jsonify({"erro": erro}), 404
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@pagamento_bp.route("/consulta_uuid/<uuid_requisicao>", methods=["GET"])
def consulta_por_uuid(uuid_requisicao):
    """Consulta pagamento e logs a partir do UUID de requisição."""
    try:
        pagamento = Pagamento.query.filter_by(uuid_requisicao=uuid_requisicao).first()

        if not pagamento:
            return jsonify({"erro": "Pagamento com esse UUID não encontrado"}), 404

        logs = LogPagamento.query.filter_by(uuid_requisicao=uuid_requisicao).all()

        return jsonify({
            "pagamento": {
                "id": pagamento.id,
                "email": pagamento.email,
                "nome": pagamento.nome,
                "payment_id": pagamento.payment_id,
                "valor": float(pagamento.valor),
                "metodo_pagamento": pagamento.metodo_pagamento,
                "parcelamento": pagamento.parcelamento,
                "status": pagamento.status,
                "criado_em": pagamento.criado_em.isoformat(),
            },
            "logs": [
                {
                    "status": log.status,
                    "detalhes": log.detalhes,
                    "criado_em": log.criado_em.isoformat()
                } for log in logs
            ]
        }), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao consultar UUID: {str(e)}"}), 500

