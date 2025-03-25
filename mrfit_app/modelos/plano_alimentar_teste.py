from typing import List, Dict, Tuple
import random

def gerar_plano_alimentar(calorias: int) -> Tuple[List[Dict[str, str]], int]:
    """Gera um plano alimentar detalhado com diferentes unidades de medida e macronutrientes."""
    
    # Tabela de alimentos com suas calorias aproximadas e informações de macronutrientes (em gramas)
    alimentos = {
        "Café da Manhã": [
            ("2 ovos mexidos (100g) + 1 fatia de pão integral (30g) + 1 banana média (120g)", 400, {"carboidratos": 40, "proteínas": 20, "gorduras": 18}),
            ("Iogurte natural (200ml) + granola (30g) + 1 colher de mel (10g)", 350, {"carboidratos": 45, "proteínas": 12, "gorduras": 10}),
            ("Vitamina de aveia (250ml de leite, 40g de aveia, 1 banana)", 450, {"carboidratos": 60, "proteínas": 12, "gorduras": 8})
        ],
        "Almoço": [
            ("150g de frango grelhado + 100g de arroz integral + 80g de salada variada", 600, {"carboidratos": 75, "proteínas": 40, "gorduras": 12}),
            ("200g de peixe assado + 150g de batata-doce + 100g de legumes cozidos", 550, {"carboidratos": 60, "proteínas": 35, "gorduras": 10}),
            ("120g de carne magra + 1 concha de feijão (100g) + 100g de arroz + 50g de verduras", 650, {"carboidratos": 80, "proteínas": 38, "gorduras": 15})
        ],
        "Jantar": [
            ("Omelete (2 ovos) com 30g de queijo branco + 100g de legumes cozidos", 500, {"carboidratos": 20, "proteínas": 30, "gorduras": 35}),
            ("Salada de atum (100g) + 50g de quinoa + 1 tomate picado + 1 colher de azeite (10ml)", 450, {"carboidratos": 40, "proteínas": 25, "gorduras": 20}),
            ("Sopa de legumes (250ml) com 100g de frango desfiado", 400, {"carboidratos": 30, "proteínas": 30, "gorduras": 12})
        ],
        "Lanche": [
            ("Iogurte natural (200ml) + 15g de castanhas", 300, {"carboidratos": 25, "proteínas": 12, "gorduras": 18}),
            ("Barra de proteína (40g) + 200ml de suco natural", 250, {"carboidratos": 30, "proteínas": 15, "gorduras": 5}),
            ("2 torradas integrais (30g) + 20g de pasta de amendoim", 350, {"carboidratos": 40, "proteínas": 10, "gorduras": 15})
        ]
    }

    plano = []
    calorias_totais = 0
    macronutrientes_totais = {"carboidratos": 0, "proteínas": 0, "gorduras": 0}
    
    for refeicao, opcoes in alimentos.items():
        escolha = random.choice(opcoes)
        descricao, calorias, macronutrientes = escolha
        plano.append({
            "nome": refeicao,
            "descricao": descricao,
            "calorias": calorias,
            "macronutrientes": macronutrientes
        })
        calorias_totais += calorias
        
        # Acumulando os macronutrientes totais
        for chave, valor in macronutrientes.items():
            macronutrientes_totais[chave] += valor

    # Ajustando o plano se as calorias totais estiverem muito abaixo ou acima do desejado
    if calorias_totais < calorias:
        # Se as calorias totais estiverem abaixo do objetivo, ajustamos as refeições
        diferenca = calorias - calorias_totais
        for refeicao in plano:
            if diferenca > 0:
                refeicao["calorias"] += diferenca // len(plano)  # Aumenta as calorias proporcionalmente
                calorias_totais += diferenca // len(plano)
                break

    return plano, calorias_totais, macronutrientes_totais

# Testando a função
calorias_desejadas = 2000
plano, calorias_totais, macronutrientes_totais = gerar_plano_alimentar(calorias_desejadas)

# Exibindo o resultado
for refeicao in plano:
    print(f"{refeicao['nome']}: {refeicao['descricao']} - {refeicao['calorias']} kcal")
    
print(f"Total de calorias: {calorias_totais} kcal")
print(f"Macronutrientes totais: {macronutrientes_totais}")
