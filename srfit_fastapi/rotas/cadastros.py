from flask import Blueprint, request, jsonify
from flask_cors import CORS
import requests
from mrfit_app.modelos.usuario import Usuario  # Certifique-se de que o modelo está correto
from mrfit_app.servicos.usuario_servico import criar_usuario_service
from mrfit_app.servicos.calculo_calorias_servico import CalculoCalorias
from mrfit_app import db

bp_usuario = Blueprint('usuario', __name__)
CORS(bp_usuario)  # Permite requisições de origens diferentes

# Endpoint para verificar se o e-mail já existe antes de avançar no cadastro
@bp_usuario.route('/verificar-email', methods=['POST'])
def verificar_email():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email não fornecido"}), 400
    
    usuario_existente = Usuario.query.filter_by(email=email).first()
    
    if usuario_existente:
        return jsonify({"error": "Este email já está registrado"}), 400
    
    return jsonify({"message": "Email disponível"}), 200

# Endpoint para cadastrar um novo usuário
@bp_usuario.route('/cadastro', methods=['POST'])
def criar_usuario():
    dados = request.json
    print("Dados recebidos:", dados)
    
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    idade = dados.get('idade')
    peso = dados.get('peso')
    altura = dados.get('altura')
    sexo = dados.get('sexo')
    objetivo_id = dados.get('objetivo')
    atividade_id = dados.get('atividade')

    # Verifica novamente se o e-mail já está cadastrado
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({"error": "Este email já está registrado"}), 400

    # Chama o serviço de criação do usuário
    resposta, status_code, novo_usuario = criar_usuario_service(
        nome=nome,
        email=email,
        senha=senha,
        idade=idade,
        peso=peso,
        altura=altura,
        sexo=sexo,
        objetivo_id=objetivo_id,
        atividade_id=atividade_id
    )

    if status_code != 201 or novo_usuario is None:
        return jsonify(resposta), status_code

    try:
        # Calcula a TMB (Taxa de Metabolismo Basal)
        tmb = CalculoCalorias.calcular_tmb(peso, altura, idade, sexo, atividade_id, objetivo_id)

        # Adicionando o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        db.session.refresh(novo_usuario)

        # Chamada para API externa de cálculo de calorias
        resposta_calorias = requests.post('http://DESKTOP-6J8R9MV/calculo/', json={
            'peso': peso,
            'altura': altura,
            'idade': idade,
            'sexo': sexo,
            'atividade': atividade_id,
            'objetivo': objetivo_id
        })

        if resposta_calorias.status_code != 200:
            print(f"Erro ao calcular calorias na API externa: {resposta_calorias.status_code}")
            print(f"Resposta da API: {resposta_calorias.text}")

        print(f"Calorias calculadas: {tmb}")
        resposta['calorias'] = tmb  # Inclui a informação de calorias no retorno

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(resposta), status_code
