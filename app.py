import os
import openai
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_text(text):
    prompt = f"Summarize the following research paper in simple terms:\n\n{text[:3000]}"  # truncate for API limit
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
    input_text = ""
    if request.method == "POST":
        input_text = request.form.get("research_text", "")
        if input_text.strip():
            summary = summarize_text(input_text)
    return render_template("index.html", summary=summary, input_text=input_text)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)   
