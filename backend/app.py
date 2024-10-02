from flask import Flask, request, jsonify
from flask_cors import CORS
from helpers import extract_entities, extract_text_from_docx, extract_text_from_pdf

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename.endswith('.pdf'):
        text_content = extract_text_from_pdf(file)
    elif file.filename.endswith('.docx'):
        text_content = extract_text_from_docx(file)
    else:
        return jsonify({"error": "Unsupported file format. Please upload a PDF or DOCX file."}), 400

    entities = extract_entities(text_content)
    return jsonify({"extracted_entities": entities})

if __name__ == '__main__':
    app.run(debug=True)