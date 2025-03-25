import os
from dotenv import load_dotenv
from mrfit_app import create_app
from mrfit_app.db_setup import init_db  # Ajustado caminho da importação

# Carrega variáveis de ambiente do .env
load_dotenv()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db()  # Inicializa o banco dentro do contexto da aplicação
    app.run(host="0.0.0.0", port=5000, debug=True)
