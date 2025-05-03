import mercadopago
import os
from mrfit_app.modelos.pagamento import Pagamento
from mrfit_app import db
from datetime import datetime

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

def criar_preferencia(access_token, transaction_amount, description, payer_email, payer_name):
    sdk = mercadopago.SDK(ACCESS_TOKEN)
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
    response = sdk.preference().create(preference_data)

    if response['status'] == 201:
        # Salvar no banco de dados
        id_preferencia = response['response']['id']
        external_reference = response['response'].get('external_reference')
        init_point = response['response']['init_point']
        
        pagamento = Pagamento(
            id_preferencia=id_preferencia,
            status='Aguardando pagamento', 
            data_pagamento=datetime.now()
        )
        db.session.add(pagamento)
        db.session.commit()
        
        return response  # Retorna os dados para o controle e a rota
    return response