import requests
import os

def n8n(data): 
     
    email = data.get("email")
    nome = data.get("nome")
    idade = data.get("idade")
    peso = data.get("peso")
    altura = data.get("altura")
    sexo = data.get("sexo")
    atividade = data.get("atividade")
    objetivo = data.get("objetivo")
    calorias = data.get("calorias")

    data = {
        'email': email,
        'nome': nome,
        'idade': idade,
        'peso': peso,
        'altura': altura,
        'sexo': sexo,
        'atividade': atividade,
        'objetivo': objetivo,
        'calorias': calorias
    }

    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/mrfit_leads")
    print (N8N_WEBHOOK_URL)
    try:
        resposta = requests.post(N8N_WEBHOOK_URL, json=data, timeout=5)
        print(f"📡 Enviado para N8N ({resposta.status_code}): {resposta.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao enviar dados para N8N: {e}")

    return