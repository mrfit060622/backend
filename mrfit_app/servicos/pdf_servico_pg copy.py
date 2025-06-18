import os
import logging
import uuid
from flask import render_template
from weasyprint import HTML
from mrfit_app.servicos.plano_alimentar_servico import validar_dados_essenciais, ajustar_calorias
from mrfit_app.modelos.plano_alimentar import gerar_plano_alimentar
from typing import Dict, Tuple

UPLOAD_FOLDER = os.path.join(os.getcwd(), "pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def gerar_pdf_pg(data: Dict[str, str]) -> Tuple[str, str]:
    """Gera um PDF com os dados fornecidos e salva localmente."""
    email = data.get("email")

    if not email:
        return None, "E-mail é obrigatório!"

    pdf_filename = f"relatorio_{uuid.uuid4().hex}.pdf"  # Apenas nome aleatório para o arquivo
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    missing_fields = validar_dados_essenciais(data)
    if missing_fields:
        return None, f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"

    plano_alimentar, calorias_totais = gerar_plano_alimentar(data['calorias'])
    data['refeicoes'] = ajustar_calorias(plano_alimentar, data['calorias'])
    data['calorias_totais'] = calorias_totais

    html = render_template('pdf_template_pg.html', **data)

    pdf = HTML(string=html).write_pdf()

    try:
        with open(pdf_path, "wb") as f:
            f.write(pdf)
    except Exception as e:
        logging.error(f"Erro ao salvar o PDF: {e}")
        return None, f"Erro ao salvar o PDF: {e}"

    return pdf_path, None 