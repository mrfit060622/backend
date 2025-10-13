import logging
from urllib.parse import urlparse
from flask import current_app
import requests
import os

def enviar_email(email: str, codigo: str,pdf_filename: str) -> str:
    """Envia um e-mail com o link para download do PDF via API do Brevo."""

    api_host = current_app.config['API_HOST']
    base_url = f"{api_host}/pdf/download/"
    pdf_url = f"{base_url}{codigo}"

    # Verificar se a URL está correta
    parsed_url = urlparse(pdf_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        logging.error(f"URL inválida: {pdf_url}")
        return "Erro ao gerar URL do PDF."

    # Corpo do e-mail em HTML
    html_content = f"""
    <p>Olá,</p>
    <p>Seu relatório de cálculo nutricional está pronto! Você pode baixá-lo no link abaixo:</p>
    <p><a href="{pdf_url}" style="color: blue; font-weight: bold;">Baixar Relatório</a></p>
    <p><small>O link expira em 1 hora.</small></p>
    <hr>
    <p>Atenciosamente,</p>
    <p><strong>Equipe MrFit</strong></p>
    <p><small>Este é um e-mail automático. Por favor, não responda.</small></p>
    """

    # Chave de API do Brevo armazenada em variável de ambiente
    api_key = os.getenv('BREVO_API_KEY')
    if not api_key:
        logging.error("Chave de API do Brevo não encontrada.")
        return "Erro: chave de API não configurada."

    payload = {
        "sender": {
            "name": "MrFit",
            "email": "992008001@smtp-brevo.com"  # Remetente verificado no Brevo
        },
        "to": [{"email": email}],
        "subject": "📄 Seu Relatório de Cálculo Nutricional",
        "htmlContent": html_content
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    try:
        logging.info(f"📨 Enviando e-mail para {email} via API Brevo...")
        response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
        response.raise_for_status()
        logging.info("✅ E-mail enviado com sucesso via Brevo API.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erro ao enviar e-mail via Brevo API: {e}")
        return f"Erro ao enviar o e-mail: {str(e)}"

