import os
from mrfit_app.servicos.pdf_servico import gerar_pdf
from mrfit_app.servicos.pdf_servico_pg import gerar_pdf_pg
from mrfit_app.servicos.email_servico import enviar_email
from mrfit_app.servicos.gera_codigo import gerar_codigo_unico  # Alterado para gerar código único

from typing import Tuple

def processar_pedido_pdf(data, mail) -> Tuple[str, str]:
    """Processa a solicitação de geração do PDF e envio por e-mail."""
    pdf_path, error = gerar_pdf(data)
    
    if error:
        return None, error

    pdf_filename = os.path.basename(pdf_path)
    codigo = gerar_codigo_unico()  # Código gerado apenas aqui!

    email_error = enviar_email(mail, data["email"], pdf_filename, codigo)
    if email_error:
        return None, email_error

    return pdf_path, codigo

def processar_pedido_pdf_pg(data, mail) -> Tuple[str, str]:
    """Processa a solicitação de geração do PDF e envio por e-mail."""
    pdf_path, error = gerar_pdf_pg(data)
    
    if error:
        return None, error

    pdf_filename = os.path.basename(pdf_path)
    codigo = gerar_codigo_unico()  # Código gerado apenas aqui!

    email_error = enviar_email(mail, data["email"], pdf_filename, codigo)
    if email_error:
        return None, email_error

    return pdf_path, codigo
