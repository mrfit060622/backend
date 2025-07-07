from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, Any,Text
import json

load_dotenv()

CHAVE_IA = os.getenv("CHAVE_IA")

client = OpenAI(api_key=CHAVE_IA)

def carregar_prompt() -> Text:
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_prompt = os.path.abspath(os.path.join(diretorio_atual, "..", "templates", "prompt.txt"))
    with open(caminho_prompt, "r", encoding="utf-8") as f:
        prompt =f.read()
    return prompt

def gerar_pdf_pg_ia(dados_usuario: Dict[str, Any]):
    if not dados_usuario:
        return None, "Dados obrigatórios"
    
    prompt_pesquisa = carregar_prompt()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"""
              Você é um nutricionista com ampla experiência prática em nutrição esportiva, emagrecimento, hipertrofia e reeducação alimentar.
              
              Com base no seguinte perfil do paciente:
              
              - Nome: {dados_usuario["nome"]}
              - Sexo: {dados_usuario["sexo"]}
              - Idade: {dados_usuario["idade"]}
              - Altura: {dados_usuario["altura"]}m
              - Peso: {dados_usuario["peso"]}kg
              - Nível de atividade física: {dados_usuario["atividade"]}
              - Objetivo: {dados_usuario["objetivo"]}
              - Necessidade calórica diária estimada: {dados_usuario["calorias"]} kcal
              
              {prompt_pesquisa}
            """}
        ]
    )
    
    conteudo = response.choices[0].message.content
    
    try:
        plano_json = json.loads(conteudo)
        json_data = (preparar_dados(dados_usuario,plano_json))
        return json_data
         
    except json.JSONDecodeError as e:
        print("Erro ao decodificar JSON:", e)
        print("Conteúdo retornado:", conteudo)
        return None


def preparar_dados(dados_usuario,json_data):
    refeicoes = []
    for nome_refeicao, alimentos in json_data["plano_alimentar"].items():
        itens_refeicao = []
        for alimento in alimentos:
            # Achar substituições
            subs_refeicao = json_data["substituicoes"].get(nome_refeicao, [])
            sub_item = next((s for s in subs_refeicao if s["original"] == alimento["alimento"]), None)
            substituicoes = sub_item["substituicoes"] if sub_item else []
            
            itens_refeicao.append({
                "nome": alimento["alimento"],
                "quantidade": alimento["quantidade"],
                "kcal": alimento["calorias"],
                "justificativa": f"Este alimento fornece {alimento['calorias']} kcal",
                "substituicoes": substituicoes
            })

        refeicoes.append({
            "nome": nome_refeicao.replace("_", " ").title(),
            "alimentos": itens_refeicao
        })

    email=dados_usuario.get('email')
    nome=dados_usuario.get('nome')
    data=dados_usuario.get('data')
    calorias=dados_usuario.get('calorias')
    idade=dados_usuario.get('idade')
    peso=dados_usuario.get('peso')
    altura=dados_usuario.get('altura')
    sexo=dados_usuario.get('sexo')
    atividade=dados_usuario.get('atividade')
    objetivo=dados_usuario.get('objetivo')

    dados = {
        "email": email,
        "nome": nome,
        "data": data,
        "calorias": calorias,
        "objetivo": objetivo,
        "idade": idade,
        "peso": peso,
        "altura": altura,
        "sexo": sexo,
        "atividade": atividade,
        "refeicoes": refeicoes,
        "macronutrientes": json_data["macronutrientes"],
        "recomendacoes": json_data["recomendacoes"],
        "observacoes": json_data["observacoes"]
    }
    return dados,calorias
    

# if __name__ == "__main__":
#     # nome_arquivo = "planos_alimentares.json"
#     # dados = carregar_planos(nome_arquivo)
#     dados = {
#     "email": "duduhvs@gmail.com",
#     "nome": "Eduardo Silva",
#     "data": "2025-06-18",
#     "idade": 27,
#     "peso": 100,
#     "altura": 1.79,
#     "sexo": "Masculino",
#     "atividade": "Moderado",
#     "objetivo": "Perda de peso",
#     "calorias": 2930
#     }
#     plano = gerar_pdf_pg_ia(dados)
    
#     # from pprint import pprint
#     # pprint(plano)
#     import json
#     print(json.dumps(plano, indent=2, ensure_ascii=False))