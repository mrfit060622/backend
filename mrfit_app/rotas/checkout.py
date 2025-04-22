from flask import Blueprint, request, jsonify

pagamento_bp = Blueprint("pagamento", __name__)
@app.route('/checkout', methods=['GET'])
def checkout():
    # Dados do pagamento
    preference_data = {
        "items": [
            {
                "title": "Nome do produto ou serviço",
                "quantity": 1,
                "unit_price": 100.00,  # Preço do produto ou serviço
            }
        ],
        "back_urls": {
            "success": "http://www.seusite.com.br/sucesso",
            "failure": "http://www.seusite.com.br/falha",
            "pending": "http://www.seusite.com.br/pendente"
        },
        "auto_return": "approved"
    }

    preference = sdk.preference().create(preference_data)
    preference_url = preference["response"]["init_point"]  # URL para redirecionamento

    return redirect(preference_url)  # Redireciona o usuário para o Mercado Pago
