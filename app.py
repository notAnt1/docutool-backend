# app.py
from flask import Flask, request, send_file
from flask_cors import CORS
import os
import uuid

# File conversion libraries
from pdf2docx import Converter
from docx import Document
from reportlab.pdfgen import canvas
from PIL import Image
import subprocess

app = Flask(__name__)
CORS(app, origins=["https://docutool.xyz"], supports_credentials=True)

@app.route('/convert', methods=['POST', 'OPTIONS'])
def convert_file():
    if 'file' not in request.files or 'to_format' not in request.form:
        return 'Missing file or target format', 400

    uploaded = request.files['file']
    to_format = request.form['to_format'].lower()
    original_ext = uploaded.filename.split('.')[-1].lower()

    input_filename = f"{uuid.uuid4()}.{original_ext}"
    output_filename = f"{uuid.uuid4()}.{to_format}"
    uploaded.save(input_filename)

    try:
        if original_ext == "pdf" and to_format == "docx":
            cv = Converter(input_filename)
            cv.convert(output_filename)
            cv.close()

        elif original_ext == "docx" and to_format == "pdf":
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", ".", input_filename
            ], check=True)
            output_filename = input_filename.replace('.docx', '.pdf')

        elif original_ext == "docx" and to_format == "txt":
            doc = Document(input_filename)
            with open(output_filename, 'w', encoding='utf-8') as f:
                for para in doc.paragraphs:
                    f.write(para.text + "\n")

        elif original_ext == "txt" and to_format == "pdf":
            c = canvas.Canvas(output_filename)
            with open(input_filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                y = 800
                for line in lines:
                    c.drawString(50, y, line.strip())
                    y -= 15
            c.save()

        elif original_ext in ["jpg", "jpeg", "png"] and to_format == "pdf":
            img = Image.open(input_filename).convert("RGB")
            img.save(output_filename)

        else:
            return f"Conversion from {original_ext} to {to_format} not supported.", 400

        return send_file(output_filename, as_attachment=True)

    except Exception as e:
        return str(e), 500

    finally:
        if os.path.exists(input_filename):
            os.remove(input_filename)
        if os.path.exists(output_filename):
            os.remove(output_filename)

@app.route('/')
def home():
    return "DocuTool Backend Running"
