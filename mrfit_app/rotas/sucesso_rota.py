# rotas/pagamento.py

from flask import Blueprint, request, render_template

pagamento_bp = Blueprint('pagamento', __name__)

@pagamento_bp.route('/pagamento/sucesso')
def pagamento_sucesso():
    status = request.args.get('status')
    payment_id = request.args.get('payment_id')
    external_reference = request.args.get('external_reference')
    
    return render_template('pagamento_sucesso.html', status=status, payment_id=payment_id, reference=external_reference)
