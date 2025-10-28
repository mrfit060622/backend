import logging
from flask_mail import Message
from urllib.parse import urlparse
from flask import current_app

def enviar_email(mail, email: str, codigo: str,pdf_filename: str = None ) -> str:
    """Envia um e-mail com o link para download do PDF."""
    
    api_host = current_app.config['API_HOST']
    # Definir a base da URL, corrigindo a formatação e usando http://
    base_url = f"{api_host}/pdf/download/"
    pdf_url = f"{base_url}{codigo}"

    # Verificar se a URL está correta
    parsed_url = urlparse(pdf_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        logging.error(f"URL inválida: {pdf_url}")
        return "Erro ao gerar URL do PDF."

    # Criar o objeto da mensagem
    msg = Message(
        subject="📄 Seu Relatório de Cálculo Nutricional",
        sender=("MrFit", "mrftig@gmail.com"),  # Nome + e-mail
        recipients=[email]
    )

    # Corpo do e-mail em HTML para melhorar a entrega
    msg.html = f"""
    <p>Olá,</p>
    <p>Seu relatório de cálculo nutricional está pronto! Você pode baixá-lo no link abaixo:</p>
    <p><a href="{pdf_url}" style="color: blue; font-weight: bold;">Baixar Relatório</a></p>
    <p><small>O link expira em 1 hora.</small></p>
    <hr>
    <p>Atenciosamente,</p>
    <p><strong>Equipe MrFit</strong></p>
    <p><small>Este é um e-mail automático. Por favor, não responda.</small></p>
    """

    # Tentar enviar o e-mail
    try:
        logging.debug(f"Enviando e-mail para: {email}")
        mail.send(msg)
        logging.debug("E-mail enviado com sucesso.")
        return None  # Caso não ocorra erro
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {e}")
        return f"Erro ao enviar o e-mail: {str(e)}"
