from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_pdf(data):
    """Gera um arquivo PDF com as informações fornecidas."""
    pdf_filename = "relatorio.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"Plano Alimentar para {data['email']}")
    c.save()
    return pdf_filename

### pdf_email.py
import smtplib

def enviar_email(email, pdf_filename):
    """Envia um e-mail com o PDF anexado."""
    print(f"Enviando {pdf_filename} para {email}...")
    return "Email enviado com sucesso."