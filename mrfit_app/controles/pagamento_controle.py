from mrfit_app.servicos.pagamento_servico import criar_pagamento_transparente, consultar_status_pagamento
from mrfit_app.modelos.pagamentos import db, Pagamento, LogPagamento

def processar_pagamento(dados):
    """Processa o pagamento com os dados recebidos."""

    valor = dados.get("valor")
    parcelamento = dados.get("parcelamento", 1)
    token = dados.get("token")
    metodo_pagamento = dados.get("payment_method_id", "").lower()
    
    # Extrai dados do payer
    payer = dados.get("payer", {})
    nome = payer.get("first_name")
    email = payer.get("email")
    cpf = payer.get("identification", {}).get("number")

    # Validação básica
    if not all([nome, email, valor, metodo_pagamento]):
        return {"erro": "Nome, email, valor e método de pagamento são obrigatórios"}, 400

    try:
        valor = float(valor)
        if valor <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return {"erro": "Valor do pagamento inválido"}, 400

    # Token é obrigatório para cartão de crédito/débito
    if metodo_pagamento not in ["pix", "boleto", "bolbradesco", "pec"] and not token:
        return {"erro": "Token do cartão é obrigatório para pagamentos com cartão"}, 400

    # Chama o serviço de pagamento
    resultado = criar_pagamento_transparente(
        nome=nome,
        email=email,
        valor=valor,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        token=token
    )

    # Se houve erro com código de status
    if isinstance(resultado, tuple):
        return resultado

    return resultado



def processar_consulta(payment_id):
    """Consulta o status do pagamento na API externa."""
    if not payment_id:
        return {"erro": "ID de pagamento obrigatório"}, 400

    return verificar_pagamento(payment_id)


def consultar_status_pagamento(payment_id):
    """Consulta o status do pagamento e do último log no banco de dados."""
    if not payment_id:
        return None, "ID de pagamento obrigatório"

    pagamento = Pagamento.query.filter_by(payment_id=payment_id).first()
    if not pagamento:
        return None, "Pagamento não encontrado"

    log = LogPagamento.query.filter_by(pagamento_id=pagamento.id)\
        .order_by(LogPagamento.criado_em.desc()).first()

    if not log:
        return None, "Log de pagamento não encontrado"

    return {
        "status": log.status,
        "data_log": log.criado_em
    }, None