import os
import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

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


if __name__ == "__main__":
    pdf_path = "taj-mahal-history-architectural-features-143.pdf"
    if not os.path.exists(pdf_path):
        print("PDF file not found.")
    else:
        extracted_text = extract_text_from_pdf(pdf_path)
        summary = summarize_text(extracted_text)
        print("\n📄 Summary:\n")
        print(summary)
