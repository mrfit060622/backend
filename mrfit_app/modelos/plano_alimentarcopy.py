from typing import List, Dict, Tuple
import random

def gerar_plano_alimentar(calorias: int) -> Tuple[List[Dict[str, str]], int]:
    """Gera um plano alimentar detalhado com diferentes unidades de medida."""
    alimentos = {
        "Café da Manhã": [
            ("2 ovos mexidos (100g) + 1 fatia de pão integral (30g) + 1 banana média (120g)", 400),
            ("Iogurte natural (200ml) + granola (30g) + 1 colher de mel (10g)", 350),
            ("Vitamina de aveia (250ml de leite, 40g de aveia, 1 banana)", 450)
        ],
        "Almoço": [
            ("150g de frango grelhado + 100g de arroz integral + 80g de salada variada", 600),
            ("200g de peixe assado + 150g de batata-doce + 100g de legumes cozidos", 550),
            ("120g de carne magra + 1 concha de feijão (100g) + 100g de arroz + 50g de verduras", 650)
        ],
        "Jantar": [
            ("Omelete (2 ovos) com 30g de queijo branco + 100g de legumes cozidos", 500),
            ("Salada de atum (100g) + 50g de quinoa + 1 tomate picado + 1 colher de azeite (10ml)", 450),
            ("Sopa de legumes (250ml) com 100g de frango desfiado", 400)
        ],
        "Lanche": [
            ("Iogurte natural (200ml) + 15g de castanhas", 300),
            ("Barra de proteína (40g) + 200ml de suco natural", 250),
            ("2 torradas integrais (30g) + 20g de pasta de amendoim", 350)
        ]
    }

    plano = []
    calorias_totais = 0
    for refeicao, opcoes in alimentos.items():
        escolha = random.choice(opcoes)
        plano.append({"nome": refeicao, "descricao": escolha[0], "calorias": escolha[1]})
        calorias_totais += escolha[1]

    return plano, calorias_totais


if __name__ == "__main__":
     calorias = 25000
     plano = gerar_plano_alimentar(calorias)
   
     from pprint import pprint
     pprint(plano)
