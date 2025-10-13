from flask import request, jsonify
import os
import mercadopago
from mrfit_app.servicos.registro_pedido_servico import registrar_pedido_relatorio
from mrfit_app.servicos.pagamento_servico import criar_pagamento_transparente
from mrfit_app.modelos.pagamento import Pagamento
from mrfit_app.modelos.relatorio import Relatorio
from mrfit_app import db
from datetime import datetime
import requests
import uuid
ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

def checkout():
    data = request.get_json()
    try:
        transaction_amount = data["transactionAmount"]
        description = data["description"]
        payer_email = data["payerEmail"]
        payer_name = data["payerName"]
        # pagamento_id será gerado após o pagamento, não agora

        # Criar preferência
        resultado = criar_preferencia(
            transaction_amount,
            description,
            payer_email,
            payer_name
        )

        if resultado["status"] != "success":
            return jsonify({
                "status": "error",
                "message": resultado.get("message"),
                "detail": resultado.get("error_detail")
            }), 400

        init_point = resultado.get("init_point")
        external_reference = resultado.get("external_reference")

        # Salvar relatório
        erro = registrar_pedido_relatorio(
            db.session,
            data={
                'email': payer_email,
                'nome': payer_name,
                'idade': data.get('idade'),
                'peso': data.get('peso'),
                'altura': data.get('altura'),
                'sexo': data.get('sexo'),
                'atividade': data.get('atividade'),
                'objetivo': data.get('objetivo'),
                'calorias': data.get('calorias')
            },
            external_reference=external_reference,
            pagamento_id=None
        )

        if erro:
            return jsonify({
                "status": "error",
                "message": "Erro ao registrar relatório",
                "detail": erro
            }), 500

        return jsonify({
            "status": "success",
            "init_point": init_point,
            "external_reference": external_reference,
            "preference_id": resultado.get("preference_id")
        }), 200

    except KeyError as ke:
        return jsonify({
            "status": "error",
            "message": f"Campo obrigatório ausente: {str(ke)}"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Erro inesperado ao processar o checkout",
            "detail": str(e)
        }), 500


def consultar_status_pagamento(payment_id):
    """Consulta o status do pagamento na API externa."""
    if not payment_id:
        return {"erro": "ID de pagamento obrigatório"}, 400

    pagamento_detalhes = verificar_pagamento(payment_id)

    if pagamento_detalhes is None:
        return {"erro": "Erro ao consultar status do pagamento"}, 500

    return jsonify(pagamento_detalhes), 200

def verificar_pagamento(payment_id):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # Retorna o JSON com os detalhes do pagamento
        else:
            print(f"Erro na consulta: Status {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Erro ao verificar pagamento: {str(e)}")
        return None


def processar_pagamento(dados):
    """Processa o pagamento com os dados recebidos."""
    uuid_requisicao = str(uuid.uuid4())
    print(f"[DEBUG] UUID da requisição gerado: {uuid_requisicao}")
    valor = dados.get("valor")
    token = dados.get("token")
    metodo_pagamento = dados.get("metodo_pagamento", "").lower()
    parcelamento = dados.get("parcelamento", 1)
    issuer_id = dados.get("issuer_id", None)
    payer = dados.get("payer", {})
    email = payer.get("email")
    nome = payer.get("nome")
    sobrenome = payer.get("sobrenome")
    identification = payer.get("identification", {})
    tp_doc = identification.get("tp_doc")
    nr_cpf = identification.get("nr_cpf")
    relatorio = dados.get("relatorio", {})
    idade = relatorio.get("idade")
    peso = relatorio.get("peso")
    altura = relatorio.get("altura")
    sexo = relatorio.get("sexo")
    atividade = relatorio.get("atividade")
    objetivo = relatorio.get("objetivo")
    calorias = relatorio.get("calorias")

    ######

    if not all([email, valor, metodo_pagamento]):
        return {"erro": "Nome, email, valor e método de pagamento são obrigatórios"}, 400

    try:
        valor = float(valor)
        if valor <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return {"erro": "Valor do pagamento inválido"}, 400

    if metodo_pagamento != "pix" and not token:
        return {"erro": "Token do cartão é obrigatório para pagamentos com cartão"}, 400

    resultado = criar_pagamento_transparente(
        valor=valor,
        email=email,
        nome=nome,
        sobrenome=sobrenome,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        issuer_id = issuer_id,
        token=token,
        nr_cpf=nr_cpf,
        tp_doc=tp_doc,
        uuid_requisicao = uuid_requisicao
    )

    print (f"[DEBUG] Resultado da criação do pagamento: {resultado}")
    erro = registrar_pedido_relatorio(
            db.session,
            data={
                'email': email,
                'nome': nome,
                'idade': idade,
                'peso': peso,
                'altura': altura,
                'sexo': sexo,
                'atividade': atividade,
                'objetivo': objetivo,
                'calorias': calorias
            },
            external_reference=uuid_requisicao,
            pagamento_id=None
    )
    print (f"[DEBUG] Resultado da criação do pedido: {erro}")
    
    return resultado

