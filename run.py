import os
from dotenv import load_dotenv
from mrfit_app import create_app,db
from flask_migrate import Migrate

# Carrega variáveis de ambiente do .env
load_dotenv()

# Criação da aplicação
app = create_app()


migrate = Migrate(app, db)

# Inicializa o banco de dados apenas uma vez ao iniciar

with app.app_context():
    try:
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar as tabelas: {e}")

# Verifica se estamos executando diretamente ou se o ambiente é de produção
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
