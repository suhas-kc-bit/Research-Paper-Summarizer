import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_text(text):
    prompt = f"Summarize the following research paper in simple terms:\n\n{text[:3000]}"  # truncate for API limit
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error with OpenAI API: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    input_text = ""
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename.endswith((".txt", ".pdf")):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            try:
                if filename.endswith(".txt"):
                    with open(filepath, "r", encoding="utf-8") as f:
                        input_text = f.read()
                elif filename.endswith(".pdf"):
                    import PyPDF2
                    with open(filepath, "rb") as f:
                        reader = PyPDF2.PdfReader(f)
                        input_text = "".join(page.extract_text() for page in reader.pages if page.extract_text())

                if input_text.strip():
                    summary = summarize_text(input_text)
                else:
                    error = "The file appears to be empty or unreadable."

            except Exception as e:
                error = f"Could not process file: {str(e)}"
        else:
            error = "Please upload a .txt or .pdf file under 5MB."

    return render_template("index.html", summary=summary, input_text=input_text, error=error)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)

