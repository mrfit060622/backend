from werkzeug.security import generate_password_hash
from mrfit_app import db
from mrfit_app.modelos.usuario import Usuario
from mrfit_app.modelos.objetivo import Objetivo
from mrfit_app.modelos.atividade import Atividade
from mrfit_app.modelos.calorias import Caloria

import requests  # Para fazer a requisição ao serviço de cálculo de calorias

def salvar_calorias(usuario_id, calorias):
    """Salva as calorias do usuário no banco de dados"""
    try:
        db.session.execute(
            Caloria.__table__.insert(),  # Use a tabela de Caloria
            {'id_usuario': usuario_id, 'valor_calorias': calorias}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar calorias: {str(e)}")

def criar_usuario_service(nome, email, senha, idade, peso, altura, sexo, objetivo_id, atividade_id):
    try:
        # Validação dos campos obrigatórios
        if not nome or not email or not senha:
            return {"error": "Nome, email e senha são obrigatórios"}, 400, None  # Retorna 3 valores

        # Verifica se o email já está registrado
        if Usuario.query.filter_by(email=email).first():
            return {"error": "Este email já está registrado"}, 400, None  # Retorna 3 valores

        # Verifica se o objetivo e a atividade existem
        objetivo = Objetivo.query.filter_by(cd_objetivo=objetivo_id).first() if objetivo_id else None
        if objetivo_id and not objetivo:
            return {"error": "Objetivo não encontrado"}, 400, None  # Retorna 3 valores

        atividade = Atividade.query.filter_by(cd_atividade=atividade_id).first() if atividade_id else None
        if atividade_id and not atividade:
            return {"error": "Atividade não encontrada"}, 400, None  # Retorna 3 valores

        # Criação do novo usuário (certificando-se de que é uma instância do modelo)
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            idade=idade,
            peso=peso,
            altura=altura,
            sexo=sexo,
            cd_objetivo=objetivo.cd_objetivo if objetivo else None,
            cd_atividade=atividade.cd_atividade if atividade else None
        )

        # Criptografando a senha antes de salvar no banco de dados
        novo_usuario.senha = generate_password_hash(senha)

        # Adicionando o novo usuário no banco
        db.session.add(novo_usuario)
        db.session.commit()

        print(f"Usuário {novo_usuario.nome} criado com sucesso!")

        # Fazer a requisição para o cálculo de calorias
        resposta_calorias = requests.post('http://DESKTOP-6J8R9MV:5000/calculo/', json={
            'idade': idade,
            'peso': peso,
            'altura': altura,
            'sexo': sexo,
            'atividade': atividade_id,
            'objetivo': objetivo_id
        })
        
        if resposta_calorias.status_code == 200:
            calorias = resposta_calorias.json().get('tmb')
            if calorias is not None:
                # Salvar calorias associadas ao usuário
                salvar_calorias(novo_usuario.id_usuario, calorias)
                print(f"Corpo da resposta: {resposta_calorias.text}")
            else:
                print("Erro: a resposta do cálculo de calorias não contém 'tmb'.")
        else:
            print(f"Erro ao chamar a API de calorias: {resposta_calorias.status_code}")
            
            
        # Retornando 3 valores (dicionário, código de status, e None)
        return {"message": "Usuário criado com sucesso!", "usuarioId": novo_usuario.id_usuario}, 201, None

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar usuário: {str(e)}")
        print(f"Dados do usuário: nome={nome}, email={email}, objetivo_id={objetivo_id}, atividade_id={atividade_id}")
        return {"error": "Erro ao criar usuário"}, 500, None  # Retorna 3 valores
