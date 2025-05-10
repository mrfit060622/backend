import mercadopago
import os
from mrfit_app.modelos.pagamento import Pagamento
from mrfit_app import db
from datetime import datetime
import uuid

ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

def criar_preferencia(transaction_amount, description, payer_email, payer_name):
    try:
        print("🔄 Iniciando criação da preferência...")

        external_reference = str(uuid.uuid4())
        print(f"📌 External Reference: {external_reference}")

        sdk = mercadopago.SDK(ACCESS_TOKEN)

        preference_data = {
            'items': [{
                'title': description,
                'quantity': 1,
                'unit_price': float(transaction_amount),
            }],
            'payer': {
                'email': payer_email,
                'name': payer_name,
            },
            'payment_methods': {
                'excluded_payment_types': [{'id': 'atm'}],  # Exclui boleto bancário
                'installments': 1,
            },
            'back_urls': {
                'success': f'https://front-mu-one.vercel.app/detalhes?ref={external_reference}',
                'failure': f'https://front-mu-one.vercel.app/detalhes?ref={external_reference}',
                'pending': f'https://front-mu-one.vercel.app/detalhes?ref={external_reference}',
            },
            'auto_return': 'approved',
            'external_reference': external_reference
        }

        print("📤 Enviando dados para Mercado Pago...")
        response = sdk.preference().create(preference_data)
        print(f"✅ Resposta da API: {response}")

        if response.get("status") == 201:
            response_data = response["response"]
            init_point = response_data.get("init_point")

            pagamento = Pagamento(
                external_reference=external_reference,
                status='Aguardando pagamento',
                data_pagamento=datetime.utcnow(),
                email_pago=payer_email
            )
            db.session.add(pagamento)
            db.session.commit()
            print("💾 Pagamento salvo com sucesso.")

            return {
                "status": "success",
                "init_point": init_point,
                "external_reference": external_reference
            }

        else:
            return {
                "status": "error",
                "message": "Erro na resposta do Mercado Pago",
                "error_detail": response
            }

    except Exception as e:
        print("❗ Exceção:", str(e))
        return {
            "status": "error",
            "message": "Erro ao criar preferência",
            "error_detail": str(e)
        }
