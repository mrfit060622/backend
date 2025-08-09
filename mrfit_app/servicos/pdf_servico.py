import os
import logging
import uuid
from flask import render_template
from weasyprint import HTML
from mrfit_app.servicos.plano_alimentar_servico import validar_dados_essenciais
from mrfit_app.modelos.plano_alimentar import gerar_plano_alimentar
from mrfit_app.servicos.relatorio_ia import gerar_pdf_pg_ia
from typing import Dict, Tuple

UPLOAD_FOLDER = os.path.join(os.getcwd(), "pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def gerar_pdf(data: Dict[str, str]) -> Tuple[str, str]:
    """Gera um PDF com os dados fornecidos e salva localmente."""
    email = data.get("email")

    if not email:
        return None, "E-mail é obrigatório!"

    pdf_filename = f"relatorio_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    missing_fields = validar_dados_essenciais(data)
    if missing_fields:
        return None, f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"

    plano_alimentar, calorias_totais = gerar_pdf_pg_ia(data)
    
    if not plano_alimentar:
        return None, "Falha ao gerar plano alimentar."

    # Atualiza todo o data com o plano retornado
    data.update(plano_alimentar)
    print (f"data: {data}")
    data['calorias_totais'] = calorias_totais

    # Renderiza o HTML
    html = render_template('pdf_template.html', **data)

    try:
        pdf = HTML(string=html).write_pdf()
        with open(pdf_path, "wb") as f:
            f.write(pdf)
    except Exception as e:
        logging.error(f"Erro ao salvar o PDF: {e}")
        return None, f"Erro ao salvar o PDF: {e}"

    return pdf_path, None