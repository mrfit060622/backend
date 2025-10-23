import os
from mrfit_app.servicos.pdf_servico import gerar_pdf
from mrfit_app.servicos.pdf_servico_pg import gerar_pdf_pg
from mrfit_app.servicos.email_servico import enviar_email
from mrfit_app.servicos.gera_codigo import gerar_codigo_unico  
from mrfit_app.servicos.registro_pedido_servico import registrar_pedido_relatorio, registrar_pedido_relatorio_gratis
from mrfit_app import db
from typing import Tuple
from mrfit_app.rotas.n8n import n8n

def processar_pedido_pdf(data, mail):
    """Processa a solicitação de geração do PDF e envio por e-mail."""
    pdf_path, plano_alimentar, error = gerar_pdf(data)
    if error:
        return None, error
    # print (plano_alimentar)
    erro_n8n = n8n(data)
    if erro_n8n:
        return None, erro_n8n
    print(erro_n8n)

    # 🔹 Usa variável de ambiente para definir a URL do webhook
    


    pdf_filename = os.path.basename(pdf_path)
    codigo = gerar_codigo_unico()
    referencia = data.get("referencia")

    erro = registrar_pedido_relatorio_gratis(db.session, data,  referencia,plano_alimentar )
    if erro:
        return None, str(erro)

    email_error = enviar_email(mail, data["email"], pdf_filename, codigo)
    if email_error:
        return None, email_error

    return pdf_path, codigo


def processar_pedido_pdf_pg(data, mail) -> Tuple[str, str]:
    email = data.get("email")
    pdf_path, error = gerar_pdf_pg(data)

    if error:
        return None, error

    pdf_filename = os.path.basename(pdf_path)
    codigo = gerar_codigo_unico()

    email_error = enviar_email(mail, data["email"], pdf_filename, codigo)
    if email_error:
        return None, email_error

    return pdf_path, codigo
