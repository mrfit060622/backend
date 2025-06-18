
import matplotlib.pyplot as plt
from io import BytesIO

def gerar_grafico_macros_bytes(calorias: int) -> bytes:
    carbo = calorias * 0.45 / 4
    proteina = calorias * 0.35 / 4
    gordura = calorias * 0.20 / 9

    labels = ['Carboidratos', 'Proteínas', 'Gorduras']
    valores = [carbo, proteina, gordura]
    cores = ['#f1c40f', '#3498db', '#e67e22']

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90, colors=cores)
    ax.set_title('Distribuição de Macronutrientes')
    ax.axis('equal')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)  # Voltar para o início do buffer

    return buf.getvalue()  # retorna bytes da imagem PNG
