import os
import logging
from flask import Blueprint, jsonify, request, send_from_directory,current_app
from flask_mail import Mail
from mrfit_app.controles.pdf_controle import processar_pedido_pdf, processar_pedido_pdf_pg
from mrfit_app.servicos.email_servico import enviar_email
from mrfit_app.servicos.gera_codigo import gerar_codigo_unico  # Alterado para gerar código único

# Criar Blueprint
pdf_bp = Blueprint("pdf", __name__)

# Configurar e-mail
mail = Mail()

# Configurar a pasta de armazenamento dos PDFs
UPLOAD_FOLDER = os.path.join(os.getcwd(), "pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  

# Dicionário para mapear códigos únicos para nomes de arquivos
codigos_arquivos = {}

@pdf_bp.route("/gerar_pdf", methods=["POST"])
def gerar_pdf():
    """ Rota para gerar um PDF e enviar por e-mail. """
    try:
        api_host = current_app.config['API_HOST']
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "E-mail é obrigatório!"}), 400

        # Gera o PDF e recebe o código único
        pdf_path, codigo = processar_pedido_pdf(data, mail)
        if not pdf_path:
            return jsonify({"error": codigo}), 400  # Aqui, codigo é a mensagem de erro

        pdf_filename = os.path.basename(pdf_path)

        # Salva a relação código -> arquivo
        codigos_arquivos[codigo] = pdf_filename  

        return jsonify({
            "message": "PDF gerado e enviado por e-mail!",
            "download_url": f"{api_host}/pdf/download/{codigo}"  
        })
    except Exception as e:
        logging.error(f"Erro ao processar requisição: {e}")
        return jsonify({"error": "Erro interno no servidor."}), 500

@pdf_bp.route("/gerar_pdf_pg", methods=["POST"])
def gerar_pdf_pg():
    """ Rota para gerar um PDF e enviar por e-mail. """
    try:
        api_host = current_app.config['API_HOST']
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "E-mail é obrigatório!"}), 400

        # Gera o PDF e recebe o código único
        pdf_path, codigo = processar_pedido_pdf_pg(data, mail)
        if not pdf_path:
            return jsonify({"error": codigo}), 400  # Aqui, codigo é a mensagem de erro

        pdf_filename = os.path.basename(pdf_path)

        # Salva a relação código -> arquivo
        codigos_arquivos[codigo] = pdf_filename  

        return jsonify({
            "message": "PDF gerado e enviado por e-mail!",
            "download_url": f"{api_host}/pdf/download/{codigo}"
        })
    except Exception as e:
        logging.error(f"Erro ao processar requisição: {e}")
        return jsonify({"error": "Erro interno no servidor."}), 500

@pdf_bp.route('/download/<codigo>', methods=['GET'])
def download_pdf(codigo):
    """ Permite o download do PDF usando apenas o código único. """
    try:
        if codigo not in codigos_arquivos:
            return jsonify({"error": "Código inválido ou expirado."}), 404

        filename = codigos_arquivos[codigo]  
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Erro ao fazer download do PDF: {e}")
        return jsonify({"error": "Erro ao processar o download."}), 500
