import os
import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# Initialize OpenAI client securely
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OpenAI API key not found. Please set it in .env or Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Streamlit UI
st.title("📄 Research Paper Summarizer")
uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

# PDF text extractor
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# OpenAI summarizer
def summarize_text(text):
    prompt = f"Summarize the following research paper in simple terms:\n\n{text[:3000]}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenAI Error: {str(e)}"

# App workflow
if uploaded_file:
    with st.spinner("⏳ Extracting and summarizing..."):
        try:
            text = extract_text_from_pdf(uploaded_file)
            if text.strip() == "":
                st.error("The uploaded PDF doesn't contain readable text.")
            else:
                summary = summarize_text(text)
                st.subheader("📚 Summary")
                st.write(summary)
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
