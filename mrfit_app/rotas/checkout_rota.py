import os
from flask import Blueprint, request, jsonify, redirect
import mercadopago

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

sdk = mercadopago.SDK(ACCESS_TOKEN)

pagamento_bp = Blueprint("pagamento", __name__)

@pagamento_bp.route('/checkout', methods=['POST'])
def checkout():
    # Recebe os dados enviados pelo front-end
    payment_data = request.get_json()
    transaction_amount = payment_data.get("transactionAmount")  # Valor do pagamento
    description = payment_data.get("description")  # Descrição do pagamento
    payer_email = payment_data.get("payerEmail")  # E-mail do pagador
    payer_name = payment_data.get("payerName")  # Nome do pagador
    payment_method = payment_data.get("paymentMethod")  # Método de pagamento (ex: "pix")

    # Dados do pagamento para o Mercado Pago
    preference_data = {
        "items": [
            {
                "title": description,  # Nome do produto ou serviço
                "quantity": 1,
                "unit_price": transaction_amount,  # Preço do produto ou serviço
            }
        ],
        "payer": {
            "email": payer_email,
            "name": payer_name
        },
        "payment_methods": {
            "excluded_payment_methods": [
                {
                    "id": payment_method  # Excluir outros métodos de pagamento, se necessário
                }
            ],
            "installments": 1  # Parcelamento (se aplicável)
        },
        "back_urls": {
            "success": "http://www.seusite.com.br/sucesso",  # URL de sucesso
            "failure": "http://www.seusite.com.br/falha",  # URL de falha
            "pending": "http://www.seusite.com.br/pendente"  # URL de pendência
        },
        "auto_return": "approved"  # Retorno automático após pagamento aprovado
    }

    # Criação da preferência no Mercado Pago
    preference = sdk.preference().create(preference_data)

    # Obter a URL para redirecionamento ao Mercado Pago
    preference_url = preference["response"]["init_point"]

    # Redireciona o usuário para o Mercado Pago
    return jsonify({"status": "success", "init_point": preference_url})
