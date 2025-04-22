from mrfit_app.servicos.pagamento_servico import criar_pagamento_transparente, consultar_status_pagamento
from mrfit_app.modelos.pagamentos import db, Pagamento, LogPagamento
import uuid

def processar_pagamento(dados):
    """Processa o pagamento com os dados recebidos."""

    uuid_requisicao = str(uuid.uuid4())
    print(f"[DEBUG] UUID da requisição gerado: {uuid_requisicao}")

    valor = dados.get("valor")
    token = dados.get("token")
    metodo_pagamento = dados.get("metodo_pagamento", "").lower()
    parcelamento = dados.get("parcelamento", 1)
    issuer_id = dados.get("issuer_id", None)
    payer = dados.get("payer", {})
    email = payer.get("email")
    nome = payer.get("nome")
    sobrenome = payer.get("sobrenome")
    identification = payer.get("identification", {})
    tp_doc = identification.get("tp_doc")
    nr_cpf = identification.get("nr_cpf")

    if not all([email, valor, metodo_pagamento]):
        _registrar_log(uuid_requisicao, None, "falha", "Campos obrigatórios ausentes")
        return {"erro": "Nome, email, valor e método de pagamento são obrigatórios"}, 400

    try:
        valor = float(valor)
        if valor <= 0:
            raise ValueError
    except (ValueError, TypeError):
        _registrar_log(uuid_requisicao, None, "falha", "Valor inválido")
        return {"erro": "Valor do pagamento inválido"}, 400

    if metodo_pagamento != "pix" and not token:
        _registrar_log(uuid_requisicao, None, "falha", "Token ausente em pagamento com cartão")
        return {"erro": "Token do cartão é obrigatório para pagamentos com cartão"}, 400

    resultado = criar_pagamento_transparente(
        valor=valor,
        email=email,
        nome=nome,
        sobrenome=sobrenome,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        issuer_id = issuer_id,
        token=token,
        nr_cpf=nr_cpf,
        tp_doc=tp_doc,
        uuid_requisicao = uuid_requisicao
    )

    if isinstance(resultado, tuple):
        _registrar_log(uuid_requisicao, None, "falha", str(resultado[0]))
        return resultado

    # Registro no banco
    pagamento = Pagamento(
        uuid_requisicao=uuid_requisicao,
        email=email,
        nome=nome,
        payment_id=resultado.get("id"),
        valor=valor,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        issuer_id = issuer_id,
        status=resultado.get("status")
    )
    db.session.add(pagamento)
    db.session.commit()

    _registrar_log(uuid_requisicao, pagamento.id, resultado.get("status"), str(resultado))

    return {
        "mensagem": "Pagamento registrado com sucesso",
        "uuid_requisicao": uuid_requisicao,
        "status": resultado.get("status"),
        "payment_id": resultado.get("id"),
        "qr_code": resultado.get("qr_code", None),
        "ticket_url": resultado.get("ticket_url", None)
    }

def _registrar_log(uuid_requisicao, pagamento_id, status, detalhes):
    log = LogPagamento(
        uuid_requisicao=uuid_requisicao,
        pagamento_id=pagamento_id,
        status=status,
        detalhes=detalhes
    )
    db.session.add(log)
    db.session.commit()


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
