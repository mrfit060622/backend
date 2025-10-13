
from typing import List, Dict


def validar_dados_essenciais(data: Dict[str, str]) -> List[str]:
    """Valida os campos obrigatórios do formulário."""
    required_fields = ['nome', 'idade', 'peso', 'altura', 'sexo', 'atividade', 'objetivo', 'calorias', 'email']
    return [campo for campo in required_fields if not data.get(campo)]

def ajustar_calorias(plano: List[Dict[str, str]], calorias_sugeridas: int) -> List[Dict[str, str]]:
    """Ajusta as calorias do plano conforme a meta calórica."""
    total = sum(item['calorias'] for item in plano)
    if total == 0:
        return plano

    fator = calorias_sugeridas / total
    for item in plano:
        item['calorias'] = int(item['calorias'] * fator)

    return plano


# if __name__ == "__main__":
#     # nome_arquivo = "planos_alimentares.json"
#     # dados = carregar_planos(nome_arquivo)
#     calorias = 25000
#     plano1,calorias = gerar_plano_alimentar(calorias)
#     result = ajustar_calorias(plano1,calorias)
#     from pprint import pprint
#     pprint(result)
