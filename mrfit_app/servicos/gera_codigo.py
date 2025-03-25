import uuid
import logging

def gerar_codigo_unico():
    """Gera um código único para identificar o arquivo PDF."""
    return str(uuid.uuid4())  # Gera um UUID aleatório

def verificar_codigo(codigo, codigos_validos):
    """
    Verifica se o código existe na lista de códigos válidos.
    
    :param codigo: Código a ser verificado.
    :param codigos_validos: Conjunto ou lista de códigos previamente gerados.
    :return: True se for válido, False caso contrário.
    """
    if codigo in codigos_validos:
        return True
    else:
        logging.error(f"Código inválido ou expirado: {codigo}")
        return False
