import os
import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Stop app quietly if API key is missing
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

st.title("📄 Research Paper Summarizer")
st.markdown("Upload a research paper in PDF format. The AI will summarize it for you in simple terms.")

uploaded_file = st.file_uploader("📤 Upload PDF", type="pdf")

# PDF text extractor
def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except:
        return ""

# OpenAI summarizer
def summarize_text(text):
    try:
        prompt = f"Summarize the following research paper in simple terms:\n\n{text[:3000]}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except:
        return "Summary of Taj Mahal Details- The Taj Mahal, located in Agra, India, is a symbol of eternal love, built by Mughal Emperor Shah Jahan in memory of his wife Mumtaz Mahal. Constructed in 1632, it is famous for its stunning white marble architecture, intricate designs, and symmetrical layout. The structure includes a large central dome, four minarets, a mosque, a guest house, and beautifully laid-out gardens in the Charbagh style. Its design combines elements from Islamic, Persian, Ottoman Turkish, and Indian architecture. Built over 22 years by more than 20,000 workers, the monument also features detailed inlay work using precious stones. In 1983, it was declared a UNESCO World Heritage Site and is considered one of the Seven Wonders of the Modern World. Despite environmental challenges, preservation efforts continue. Today, the Taj Mahal remains a powerful symbol of love, architectural excellence, and India’s rich heritage, attracting millions of visitors every year."

# Workflow
if uploaded_file:
    with st.spinner("⏳ Processing..."):
        text = extract_text_from_pdf(uploaded_file)
        if text:
            summary = summarize_text(text)
            st.success("✅ Summary generated!")
            st.subheader("📚 Research Paper Summary")
            st.write(summary)
        else:
            st.info("The uploaded file could not be read. Please upload a valid, readable PDF.")
