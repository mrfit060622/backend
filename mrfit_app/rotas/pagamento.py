from flask import Blueprint, request, jsonify
from mrfit_app.controles.pagamento_controle import processar_pagamento, processar_consulta, consultar_status_pagamento

pagamento_bp = Blueprint("pagamento", __name__)

@pagamento_bp.route("/criar_pagamento", methods=["POST"])
def criar_pagamento():
    dados = request.json
    resposta = processar_pagamento(dados)
    return jsonify(resposta)

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
