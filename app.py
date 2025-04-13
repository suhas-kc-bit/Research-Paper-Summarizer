import os
import fitz  # PyMuPDF
import openai
import streamlit as st
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📄 Research Paper Summarizer")

uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def summarize_text(text):
    prompt = f"Summarize the following research paper in simple terms:\n\n{text[:3000]}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

if uploaded_file:
    with st.spinner("Extracting and summarizing..."):
        text = extract_text_from_pdf(uploaded_file)
        summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)
