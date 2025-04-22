import os
from flask import Blueprint, request, jsonify, redirect
import mercadopago

@app.route('/pagamento/checkout', methods=['POST'])
def checkout():
    # Configurar o Mercado Pago com o Access Token
    MP = mercadopago.MP(ACCESS_TOKEN)
    data = request.json
    transaction_amount = data['transactionAmount']
    description = data['description']
    payer_email = data['payerEmail']
    payer_name = data['payerName']

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

    # Cria a preferência de pagamento
    preference = mp.create_preference(preference_data)

    if preference['status'] == '200':
        init_point = preference['response']['init_point']
        return jsonify({'status': 'success', 'init_point': init_point})
    else:
        return jsonify({'status': 'error', 'message': 'Erro ao criar preferência de pagamento'})
