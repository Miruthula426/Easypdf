from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def text_to_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 40

    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()

