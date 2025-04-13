from flask import jsonify
from mrfit_app.servicos.calculo_calorias_servico import CalculoCalorias
from sqlalchemy.orm import Session

class CalculoControle:
    @staticmethod
    def calcular_calorias(request_data, db: Session):
        try:
            # Obtém os dados do request
            idade, peso, altura, sexo, atividade_texto, objetivo = (
                request_data.get('idade'),
                request_data.get('peso'),
                request_data.get('altura'),
                request_data.get('sexo'),
                request_data.get('atividade'),
                request_data.get('objetivo')
            )

            # Verifica se todos os campos obrigatórios foram fornecidos
            if not all([idade, peso, altura, sexo, objetivo, atividade_texto]):
                return {"error": "Peso, altura, idade, sexo, objetivo e atividade são obrigatórios"}, 400

            # Tenta converter idade, peso e altura para float
            try:
                idade, peso, altura = map(float, (idade, peso, altura))
            except ValueError:
                return {"error": "Idade, peso e altura devem ser números válidos."}, 400

            # Calcula TMB
            tmb_ = CalculoCalorias.calcular_tmb(peso, altura, idade, sexo, atividade_texto, objetivo, db)
            
        except Exception as e:
            print(f"Erro: {e}")
        return {"message": "calculo realizado com sucesso!!!", "tmb" : tmb_},200
