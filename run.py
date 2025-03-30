import os
from dotenv import load_dotenv
from mrfit_app import create_app
from mrfit_app.db_setup import init_db  # Ajustado caminho da importação

# Carrega variáveis de ambiente do .env
load_dotenv()

# Criação da aplicação
app = create_app()

# Inicializa o banco de dados apenas uma vez ao iniciar
with app.app_context():
    init_db()

# Verifica se estamos executando diretamente ou se o ambiente é de produção
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
