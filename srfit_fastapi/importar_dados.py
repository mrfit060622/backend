import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações do aplicativo Flask e do banco de dados
app = Flask(__name__)

# Configurações manuais do banco de dados
DB_HOST = 'DESKTOP-6J8R9MV'
DB_PORT = '3306'
DB_USER = 'app_mrfit'
DB_PASSWORD = '1234'
DB_NAME = 'mrfit'

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{3306}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua-chave-secreta-aqui'  # Defina uma chave secreta adequada

# Inicializar a extensão SQLAlchemy
db = SQLAlchemy(app)

# Importar o modelo Alimento após a inicialização do db
from mrfit_app.modelos import Alimento

# Regex para capturar os dados
regex = r"^(\d+)\s+([\w\s,]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)\s+([\d,NA]+)"

# Função para ler os dados do arquivo
def ler_dados_do_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        return file.readlines()

# Função para inserir dados
def inserir_dados(dados):
    for linha in dados:
        match = re.match(regex, linha)
        if match:
            valores = match.groups()
            
            # Convertendo 'NA' para None (NULL no SQL)
            valores = [None if v == "NA" else v.replace(",", ".") for v in valores]
            
            # Criar uma instância da classe Alimento
            try:
                alimento = Alimento(
                    id=int(valores[0]) if valores[0] is not None else None,
                    descricao=valores[1],
                    umidade=float(valores[2]) if valores[2] else None,
                    energia_kcal=int(valores[3]) if valores[3] else None,
                    energia_kj=int(valores[4]) if valores[4] else None,
                    proteina=float(valores[5]) if valores[5] else None,
                    lipideos=float(valores[6]) if valores[6] else None,
                    colesterol=valores[7],
                    carboidratos=float(valores[8]) if valores[8] else None,
                    fibra=float(valores[9]) if valores[9] else None,
                    cinzas=float(valores[10]) if valores[10] else None,
                    calcio=int(valores[11]) if valores[11] else None,
                    magnesio=int(valores[12]) if valores[12] else None
                )

                # Adicionar ao banco de dados
                db.session.add(alimento)
            except Exception as e:
                print(f"Erro ao criar Alimento: {e}")
    
    db.session.commit()
# Executar a inserção
if __name__ == "__main__":
    try:
        dados = ler_dados_do_arquivo('dadoss.txt')
        inserir_dados(dados)
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
