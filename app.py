from flask import Flask, render_template, request, send_file
import os
from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "image" not in request.files:
            return "No image uploaded"

        file = request.files["image"]

        if file.filename == "":
            return "No file selected"

        # Save image
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # OCR
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Create PDF
        pdf_path = os.path.join(OUTPUT_FOLDER, "EasyPDF_Output.pdf")
        c = canvas.Canvas(pdf_path, pagesize=A4)

        width, height = A4
        x, y = 40, height - 40

        for line in text.split("\n"):
            c.drawString(x, y, line)
            y -= 15
            if y < 40:
                c.showPage()
                y = height - 40

        c.save()

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="EasyPDF_Output.pdf"
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

