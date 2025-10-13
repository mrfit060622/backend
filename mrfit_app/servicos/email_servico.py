# import logging
# from urllib.parse import urlparse
# from flask import current_app
# import requests
# import os

# def enviar_email(mail, email: str, pdf_filename: str, codigo: str) -> str:
#     """Envia um e-mail com o link para download do PDF via API do Brevo."""

#     api_host = current_app.config['API_HOST']
#     base_url = f"{api_host}/pdf/download/"
#     pdf_url = f"{base_url}{codigo}"
    
#     # Verificar se a URL está correta
#     parsed_url = urlparse(pdf_url)
#     if not parsed_url.scheme or not parsed_url.netloc:
#         logging.error(f"URL inválida: {pdf_url}")
#         return "Erro ao gerar URL do PDF."
    
#     # Corpo do e-mail em HTML
#     html_content = f"""
#     <p>Olá,</p>
#     <p>Seu relatório de cálculo nutricional está pronto! Você pode baixá-lo no link abaixo:</p>
#     <p><a href="{pdf_url}" style="color: blue; font-weight: bold;">Baixar Relatório</a></p>
#     <p><small>O link expira em 1 hora.</small></p>
#     <hr>
#     <p>Atenciosamente,</p>
#     <p><strong>Equipe MrFit</strong></p>
#     <p><small>Este é um e-mail automático. Por favor, não responda.</small></p>
#     """

#     # Chave de API do Brevo armazenada em variável de ambiente
#     api_key = os.getenv('BREVO_API_KEY')
#     if not api_key:
#         logging.error("Chave de API do Brevo não encontrada.")
#         return "Erro: chave de API não configurada."

#     payload = {
#         "sender": {
#             "name": "MrFit",
#             "email": "suporte@srfit.com.br"  # Remetente verificado no Brevo
#         },
#         "to": [{"email": email}],
#         "subject": "📄 Seu Relatório de Cálculo Nutricional",
#         "htmlContent": html_content
#     }

#     headers = {
#         "accept": "application/json",
#         "api-key": api_key,
#         "content-type": "application/json"
#     }

#     try:
#         logging.info(f"📨 Enviando e-mail para {email} via API Brevo...")
#         response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
#         response.raise_for_status()
#         logging.info("✅ E-mail enviado com sucesso via Brevo API.")
#         return None
#     except requests.exceptions.RequestException as e:
#         logging.error(f"❌ Erro ao enviar e-mail via Brevo API: {e}")
#         return f"Erro ao enviar o e-mail: {str(e)}"

import os
import logging
import base64
import requests
from urllib.parse import urlparse
from flask import current_app

def enviar_email(mail, email: str, pdf_filename: str, codigo: str) -> str:
    """
    Envia um e-mail com o PDF em anexo e link para download via Brevo.
    Retorna None se sucesso, ou mensagem de erro se falhar.
    """
    api_host = current_app.config.get('API_HOST')
    upload_folder = os.path.join(os.getcwd(), "pdfs")
    pdf_path = os.path.join(upload_folder, pdf_filename)

    # Verifica se o arquivo existe
    if not os.path.exists(pdf_path):
        logging.error(f"Arquivo PDF não encontrado: {pdf_path}")
        return "Erro: arquivo PDF não encontrado."

    # Monta URL de fallback (link de download)
    base_url = f"{api_host}/pdf/download/"
    pdf_url = f"{base_url}{codigo}"

    parsed_url = urlparse(pdf_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        logging.error(f"URL inválida: {pdf_url}")
        return "Erro ao gerar URL do PDF."

    # Converte o PDF para Base64
    try:
        with open(pdf_path, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode()
    except Exception as e:
        logging.error(f"Erro ao ler o PDF para anexo: {e}")
        return f"Erro ao anexar o PDF: {e}"

    # Corpo do e-mail em HTML
    html_content = f"""
    <p>Olá,</p>
    <p>Seu relatório de cálculo nutricional está pronto! 🎯</p>
    <p>Ele está anexado a este e-mail.</p>
    <p>Caso prefira, você também pode baixá-lo clicando no link abaixo:</p>
    <p><a href="{pdf_url}" style="color: #007bff; font-weight: bold;">📥 Baixar Relatório</a></p>
    <hr>
    <p>Atenciosamente,</p>
    <p><strong>Equipe MrFit</strong></p>
    <p><small>Este é um e-mail automático. Por favor, não responda.</small></p>
    """

    # Chave da API
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        logging.error("Chave de API Brevo não configurada.")
        return "Erro: chave de API não configurada."

    # Payload da API Brevo
    payload = {
        "sender": {
            "name": "MrFit",
            "email": "suporte@srfit.com.br"  # remetente verificado no Brevo
        },
        "to": [{"email": email}],
        "subject": "📄 Seu Relatório de Cálculo Nutricional",
        "htmlContent": html_content,
        "attachment": [
            {
                "content": pdf_base64,
                "name": pdf_filename
            }
        ]
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    try:
        logging.info(f"📨 Enviando e-mail para {email} com anexo via Brevo...")
        response = requests.post("https://api.brevo.com/v3/smtp/email", json=payload, headers=headers)
        response.raise_for_status()
        logging.info("✅ E-mail com anexo enviado com sucesso via Brevo.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erro ao enviar e-mail via Brevo API: {e}")
        return f"Erro ao enviar o e-mail: {str(e)}"
