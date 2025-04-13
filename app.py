import os
import fitz  # PyMuPDF
import openai
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB upload

openai.api_key = os.getenv("OPENAI_API_KEY")

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def summarize_text(text):
    prompt = f"Summarize the following research paper in simple terms:\n\n{text[:3000]}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error with OpenAI API: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file part"
        file = request.files["pdf"]
        if file.filename == "":
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            extracted_text = extract_text_from_pdf(filepath)
            summary = summarize_text(extracted_text)
            os.remove(filepath)  # Clean up uploaded file

    return render_template("index.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)

