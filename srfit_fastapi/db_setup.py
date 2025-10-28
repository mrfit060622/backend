from mrfit_app import db

def init_db():
    """Inicializa o banco de dados e cria as tabelas."""
    try:
        db.create_all()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
