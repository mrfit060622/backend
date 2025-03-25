from sqlalchemy.orm import Session

atividade_map = {
    '1': 1.2,    # Sedentário
    '2': 1.375,  # Levemente ativo
    '3': 1.55,   # Moderadamente ativo
    '4': 1.725,  # Altamente ativo
    '5': 1.9     # Extremamente ativo
}

objetivos_validos = {
    "1": "manutenção",
    "2": "ganho de peso",
    "3": "perda de peso"
}

class CalculoCalorias:
    @staticmethod
    def calcular_tmb(peso, altura, idade, sexo, atividade_texto, objetivo, db):
        if objetivo not in objetivos_validos:
            raise ValueError("Objetivo inválido. Os objetivos válidos são: '1' (manutenção), '2' (ganho de peso) ou '3' (perda de peso).")

        if atividade_texto not in atividade_map:
            raise ValueError("Atividade inválida. Use '1', '2', '3', '4' ou '5' para as opções de atividade.")

        atividade = atividade_map[atividade_texto]

        if sexo == "m":
            tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
        elif sexo == "f":
            tmb = (10 * peso) + (6.25 * altura) - (5 * idade) - 161
        else:
            raise ValueError("Sexo inválido. Use 'm' para masculino ou 'f' para feminino.")

        # Ajusta o TMB com base na atividade
        tmb *= atividade

        # Ajuste de calorias com base no objetivo
        if objetivo == "3":  # Perda de peso
            tmb -= 500
        elif objetivo == "2":  # Ganho de peso
            tmb += 500

        return round(tmb, 2)

