import os
import json
import re
from typing import Dict, Any, List
# from mrfit_app.modelos.grafico_alimentos import gerar_grafico_macros

def carregar_planos(objetivo) -> Dict[str, Any]:
    if objetivo == 1:
        nome_arquivo = "planos_alimentares.json"
    else:
        nome_arquivo = "planos_alimentares2.json"
    
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_json = os.path.abspath(os.path.join(diretorio_atual, "..", "templates", nome_arquivo))
    
    with open(caminho_json, "r", encoding="utf-8") as f:
        return json.load(f)


def selecionar_faixa(calorias: int, faixas: list[int]) -> int:
    faixas_ordenadas = sorted(faixas)
    selecionada = faixas_ordenadas[0]
    for faixa in faixas_ordenadas:
        if calorias >= faixa:
            selecionada = faixa
        else:
            break
    return selecionada


def separar_alimentos(descricao: str) -> List[Dict[str, str]]:
    """
    Converte string do tipo:
    "Leite desnatado: 1 copo (200 ml) — Grupo F"
    em:
    {
        "nome": "Leite desnatado",
        "quantidade": "1 copo (200 ml)",
        "grupo": "Grupo F"
    }
    """
    itens = [item.strip() for item in re.split(r',(?![^()]*\))', descricao)]
    resultado = []

    for item in itens:
        partes = item.split("—")
        if len(partes) == 2:
            alimento_qtd, grupo = partes
            if ":" in alimento_qtd:
                nome, qtd = map(str.strip, alimento_qtd.split(":", 1))
            else:
                nome, qtd = alimento_qtd.strip(), ""
            resultado.append({
                "nome": nome,
                "quantidade": qtd,
                "grupo": grupo.strip()
            })
        else:
            resultado.append({
                "nome": item.strip(),
                "quantidade": "",
                "grupo": ""
            })

    return resultado


def gerar_plano_alimentar(calorias: int, objetivo=1) -> tuple[List[Dict[str, Any]], int]:
    dados_planos = carregar_planos(objetivo)
    faixas = list(map(int, dados_planos.keys()))
    faixa_escolhida = selecionar_faixa(calorias, faixas)
    plano_raw = dados_planos[str(faixa_escolhida)]

    nomes_refeicoes = {
        "cafe_da_manha": "☀️ Café da Manhã",
        "lanche_da_manha": "🍎 Lanche da Manhã",
        "almoco_jantar": "🍛 Almoço / Jantar",
        "lanche_da_tarde": "☕ Lanche da Tarde",
        "ceia": "🌙 Ceia",
    }

    refeicoes_formatadas = []

    for chave, itens in plano_raw.items():
        nome_legivel = nomes_refeicoes.get(chave, chave.replace("_", " ").title())
        descricao = ", ".join(itens)
        alimentos = separar_alimentos(descricao)

        refeicoes_formatadas.append({
            "nome": nome_legivel,
            "alimentos": alimentos  # Agora lista de dicionários
        })

    return refeicoes_formatadas, faixa_escolhida



if __name__ == "__main__":
    # nome_arquivo = "planos_alimentares.json"
    # dados = carregar_planos(nome_arquivo)
    calorias_entrada = 1500
    plano = gerar_plano_alimentar(calorias_entrada,1)
    
    from pprint import pprint
    pprint(plano)
