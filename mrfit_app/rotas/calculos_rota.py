from flask import Blueprint, request, jsonify
from mrfit_app.config import SessionLocal  # 🔹 Importa a sessão do banco
from mrfit_app.controles.calculo_controle import CalculoControle

bp_calculo = Blueprint('calculo', __name__)

@bp_calculo.route('/', methods=['POST'])
def calcular():
    db = SessionLocal()  # 🔹 Criar sessão do banco de dados
    try:
        # Chama o método de controle para calcular as calorias
        response, status_code = CalculoControle.calcular_calorias(request.json, db)  # 🔹 Passa `db` corretamente
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()  # 🔹 Fecha a sessão do banco

