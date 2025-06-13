from flask import Flask, request, send_file
from flask_cors import CORS  # ✅ Add this
import os
from pdf2docx import Converter
import uuid

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS globally

@app.route('/pdf-to-word', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf' not in request.files:
        return 'No file uploaded', 400

    pdf_file = request.files['pdf']
    pdf_filename = f"{uuid.uuid4()}.pdf"
    docx_filename = pdf_filename.replace('.pdf', '.docx')

    pdf_file.save(pdf_filename)
    cv = Converter(pdf_filename)
    cv.convert(docx_filename)
    cv.close()

    response = send_file(docx_filename, as_attachment=True)

    os.remove(pdf_filename)
    os.remove(docx_filename)

    return response