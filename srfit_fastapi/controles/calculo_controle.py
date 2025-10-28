from flask import jsonify
from mrfit_app.servicos.calculo_calorias_servico import CalculoCalorias
from sqlalchemy.orm import Session

class CalculoControle:
    @staticmethod
    def calcular_calorias(request_data, db):
        try:
            # Obtém os dados do request
            idade = request_data.get('idade')
            peso = request_data.get('peso')
            altura = request_data.get('altura')
            sexo = request_data.get('sexo')
            atividade_texto = request_data.get('atividade')
            objetivo = request_data.get('objetivo')

            # Verifica se todos os campos obrigatórios foram fornecidos
            if not all([peso, altura, idade, sexo, objetivo, atividade_texto]):
                return {"error": "Peso, altura, idade, sexo, objetivo e atividade são obrigatórios"}, 400

            # Tenta converter idade, peso e altura para float
            try:
                idade = float(idade)
                peso = float(peso)
                altura = float(altura)
            except ValueError:
                return {"error": "Idade, peso e altura devem ser números válidos."}, 400

            # Calcula TMB
            tmb_ = CalculoCalorias.calcular_tmb(peso, altura, idade, sexo, atividade_texto, objetivo,db)
            
        except Exception as e:
            print(f"Erro: {e}")
        return {"message": "calculo realizado com sucesso!!!", "tmb" : tmb_},200
