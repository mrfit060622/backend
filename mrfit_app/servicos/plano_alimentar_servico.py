from typing import List, Dict

def validar_dados_essenciais(data: Dict[str, str]) -> List[str]:
    """Valida se todos os campos obrigatórios estão presentes nos dados do usuário."""
    required_fields = ['nome', 'idade', 'peso', 'altura', 'sexo', 'atividade', 'objetivo', 'calorias', 'email']
    return [field for field in required_fields if not data.get(field)]

def ajustar_calorias(plano_alimentar: List[Dict[str, str]], calorias_sugeridas: int) -> List[Dict[str, str]]:
    """Ajusta as quantidades dos alimentos para que a soma das calorias atinja a meta sugerida."""
    total_calorias = sum(item['calorias'] for item in plano_alimentar)

    if total_calorias > 0:  # Evitar divisão por zero
        fator_ajuste = calorias_sugeridas / total_calorias
        for item in plano_alimentar:
            item['calorias'] = int(item['calorias'] * fator_ajuste)

    return plano_alimentar
