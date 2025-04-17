from mrfit_app.servicos.pagamento_servico import criar_pagamento_transparente, consultar_status_pagamento
from mrfit_app.modelos.pagamentos import db, Pagamento, LogPagamento
import uuid

def processar_pagamento(dados):
    """Processa o pagamento com os dados recebidos."""
    uuid_requisicao = str(uuid.uuid4())

    valor = dados.get("valor")
    token = dados.get("token")
    metodo_pagamento = dados.get("metodo_pagamento", "").lower()
    parcelamento = dados.get("parcelamento", 1)

    payer = dados.get("payer", {})
    email = payer.get("email")
    nome = payer.get("nome")
    sobrenome = payer.get("sobrenome")
    identification = payer.get("identification", {})
    tp_doc = identification.get("tp_doc")
    nr_cpf = identification.get("nr_cpf")

    if not all([email, valor, metodo_pagamento]):
        return {"erro": "Nome, email, valor e método de pagamento são obrigatórios"}, 400

    try:
        valor = float(valor)
        if valor <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return {"erro": "Valor do pagamento inválido"}, 400

    if metodo_pagamento != "pix" and not token:
        return {"erro": "Token do cartão é obrigatório para pagamentos com cartão"}, 400

    resultado = pagamento_mp(
        valor=valor,
        email=email,
        nome=nome,
        sobrenome=sobrenome,
        metodo_pagamento=metodo_pagamento,
        parcelamento=parcelamento,
        token=token,
        nr_cpf=nr_cpf,
        tp_doc=tp_doc
    )

    # Em caso de falha no pagamento
    if isinstance(resultado, tuple):
        status = resultado[0].get("erro", "erro")
        detalhes = resultado[0]
        log = LogPagamento(
            uuid_requisicao=uuid_requisicao,
            pagamento_id=None,
            status="falha",
            detalhes=str(detalhes)
        )
        db.session.add(log)
        db.session.commit()
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
        status=resultado.get("status")
    )
    db.session.add(pagamento)
    db.session.commit()

    log = LogPagamento(
        uuid_requisicao=uuid_requisicao,
        pagamento_id=pagamento.id,
        status=resultado.get("status"),
        detalhes=str(resultado)
    )
    db.session.add(log)
    db.session.commit()

    return {
        "mensagem": "Pagamento registrado com sucesso",
        "uuid_requisicao": uuid_requisicao,
        "status": resultado.get("status"),
        "payment_id": resultado.get("id")
    }


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