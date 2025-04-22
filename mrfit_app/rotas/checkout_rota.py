import os
from flask import Blueprint, request, jsonify, redirect
import mercadopago

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

mp = mercadopago.MP(ACCESS_TOKEN)

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
        'items': [
            {
                'title': description,
                'quantity': 1,
                'unit_price': transaction_amount,
            }
        ],
        'payer': {
            'email': payer_email,
            'name': payer_name,
        },
        'payment_methods': {
            'excluded_payment_types': [{'id': 'atm'}],
            'installments': 1,
        },
        'back_urls': {
            'success': 'https://seusite.com/pagamento/sucesso',
            'failure': 'https://seusite.com/pagamento/erro',
            'pending': 'https://seusite.com/pagamento/pendente',
        },
        'auto_return': 'approved',
    }

    # Criação da preferência no Mercado Pago
    preference = mp.create_preference(preference_data)

    # Obter a URL para redirecionamento ao Mercado Pago
     if preference['status'] == '200':
        init_point = preference['response']['init_point']
        return jsonify({'status': 'success', 'init_point': init_point})
    else:
        return jsonify({'status': 'error', 'message': 'Erro ao criar preferência de pagamento'})
