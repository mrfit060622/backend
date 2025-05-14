from flask import Blueprint, request, jsonify, redirect
from mrfit_app.controles.pagamento_controle import checkout,consultar_status_pagamento
from mrfit_app.modelos.pagamento import Pagamento
import mercadopago
import os

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

pagamento_bp = Blueprint("pagamento", __name__)

# Definindo a rota com o método POST
pagamento_bp.route('/checkout', methods=['POST'])(checkout)


# Rota para consultar status de pagamento
@pagamento_bp.route("/status_pagamento/<payment_id>", methods=["GET"])
def status_pagamento(payment_id):
    try:
        resultado, erro = consultar_status_pagamento(payment_id)
        if erro:
            return jsonify({"erro": erro}), 404
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@pagamento_bp.route("/consulta_status_interno/<external_reference>", methods=["GET"])
def consulta_status_pagamento_interno(external_reference):
    """Consulta pagamento a partir do externa_reference."""
    print (f"📌 External Reference: {external_reference}")
    try:
        pagamento = Pagamento.query.filter_by(external_reference=external_reference).first()

        if not pagamento:
            return jsonify({"erro": "Pagamento não identificado"}), 404

        return jsonify({"status": pagamento.status}), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao consultar UUID: {str(e)}"}), 500

#novo metodo
@pagamento_bp.route('/intent', methods=['POST'])
def criar_preferencia():
    sdk = mercadopago.SDK(ACCESS_TOKEN)

    data = request.get_json()
    preference_data = {
        "items": [
            {
                "title": data.get("description"),
                "quantity": 1,
                "unit_price": float(data.get("transactionAmount")),
            }
        ],
        "payer": {
            "email": data.get("payerEmail"),
            "name": data.get("payerName"),
        },
        "back_urls": {
            "success": "https://seusite.com/sucesso",
            "failure": "https://seusite.com/falha",
            "pending": "https://seusite.com/pendente",
        },
        "auto_return": "approved",
        "external_reference": data.get("external_reference")
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        print (f"📌 Preference ID: {preference_response}")
        return jsonify({"id": preference["id"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500