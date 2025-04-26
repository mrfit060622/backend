import mercadopago

def criar_preferencia(access_token, transaction_amount, description, payer_email, payer_name):
    sdk = mercadopago.SDK(access_token)
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
    return sdk.preference().create(preference_data)