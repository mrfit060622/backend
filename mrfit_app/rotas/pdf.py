import os
import logging
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, request, send_from_directory, current_app
from flask_mail import Mail
from mrfit_app.controles.pdf_controle import processar_pedido_pdf, processar_pedido_pdf_pg
from mrfit_app.modelos.relatorio import Relatorio

# Criar Blueprint
pdf_bp = Blueprint("pdf", __name__)

# Configurar e-mail
mail = Mail()

# Configurar a pasta de armazenamento dos PDFs
UPLOAD_FOLDER = os.path.join(os.getcwd(), "pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ThreadPool para controlar tarefas simultâneas
executor = ThreadPoolExecutor(max_workers=5)

# Dicionário para mapear códigos únicos para nomes de arquivos
codigos_arquivos = {}

# Função que roda em background COM CONTEXTO
def gerar_pdf_thread(func, data, mail, app):
    try:
        with app.app_context():  # garante que a thread tenha contexto do Flask
            pdf_path, codigo = func(data, mail)
            if pdf_path:
                pdf_filename = os.path.basename(pdf_path)
                codigos_arquivos[codigo] = pdf_filename
                logging.info(f"✅ PDF gerado e armazenado: {pdf_filename}")
            else:
                logging.error(f"❌ Erro ao gerar PDF: {codigo}")  # aqui codigo é msg de erro
    except Exception as e:
        logging.error(f"Erro ao processar PDF em background: {e}")

def disparar_pdf(func, data):
    app = current_app._get_current_object()  # pega a instância real da app
    executor.submit(gerar_pdf_thread, func, data, mail, app)

# -------- ROTAS -------- #

@pdf_bp.route("/gerar_pdf", methods=["POST"])
def gerar_pdf():
    """ Rota para gerar um PDF e enviar por e-mail em background. """
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "E-mail é obrigatório!"}), 400

        # dispara a tarefa em background
        disparar_pdf(processar_pedido_pdf, data)

        return jsonify({
            "message": "Sua solicitação foi recebida! O PDF será enviado por e-mail.",
            "info": "Pode levar alguns segundos para o e-mail chegar."
        })

    except Exception as e:
        logging.error(f"Erro ao processar requisição: {e}")
        return jsonify({"error": "Erro interno no servidor."}), 500


@pdf_bp.route("/gerar_pdf_pg", methods=["POST"])
def gerar_pdf_pg():
    """ Rota para gerar um PDF pago e enviar por e-mail em background. """
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"error": "E-mail é obrigatório!"}), 400

        # dispara a tarefa em background
        disparar_pdf(processar_pedido_pdf_pg, data)

        return jsonify({
            "message": "Sua solicitação foi recebida! O PDF será enviado por e-mail.",
            "info": "Pode levar alguns segundos para o e-mail chegar."
        })

    except Exception as e:
        logging.error(f"Erro ao processar requisição: {e}")
        return jsonify({"error": "Erro interno no servidor."}), 500


@pdf_bp.route("/consulta_pdf/<external_reference>", methods=["GET"])
def buscar_relatorio_por_referencia(external_reference):
    """ Consulta dados do relatório pelo external_reference. """
    relatorio = Relatorio.query.filter_by(external_reference=external_reference).first()

    if not relatorio:
        return jsonify({'erro': 'Relatório não encontrado'}), 404

    return jsonify({
        'nome': relatorio.nome,
        'idade': relatorio.idade,
        'peso': relatorio.peso,
        'altura': relatorio.altura,
        'sexo': relatorio.sexo,
        'atividade': relatorio.atividade,
        'objetivo': relatorio.objetivo,
        'calorias': relatorio.calorias
    })


@pdf_bp.route("/download/<codigo>", methods=["GET"])
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
