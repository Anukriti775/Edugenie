import fitz  # PyMuPDF #pdf_summarizer.py
from transformers import pipeline
import streamlit as st
import textwrap
import re

import streamlit as st

def run_pdf_summarizer():
    st.title("📄 PDF Summarizer")
    st.markdown("Upload a PDF file to summarize your study material into crisp notes.")

    if st.button("🔙 Back to Home"):
        st.session_state.tool_selector = None
        st.rerun()

    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded_file:
        st.success("✅ File uploaded successfully.")
        st.write("📝 *Summary Preview:*")
        st.info("This is where the summarized content will appear.")



# 💜 Apply purple theme & hide uploader label
st.markdown("""
<style>
/* Hide the file uploader label */
div[data-testid="stFileUploader"] label {
    display: none !important;
}

/* File uploader container style */
div[data-testid="stFileUploader"] {
    background-color: #f1e6ff !important;
    border: 2px solid #5e1f8c !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-bottom: 25px !important;
}

/* Inner dropzone */
div[data-testid="stFileDropzone"] {
    background-color: #f1e6ff !important;
    color: #5e1f8c !important;
    border: 1px dashed #b57cff !important;
    border-radius: 10px !important;
}

/* Notification text */
[data-testid="stNotificationContentInfo"],
[data-testid="stNotificationContentSuccess"],
[data-testid="stNotificationContentError"] {
    color: #5e1f8c !important;
    font-family: 'Segoe UI', sans-serif' !important;
}

/* Headings and summaries */
h1, h2, h3, h4, h5, h6, .stMarkdown p {
    color: #5e1f8c !important;
    font-family: 'Segoe UI', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


def clean_text(text):
    text = text.replace('\u00a0', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def summarize_text_to_bullets(text, max_chunk_size=1024):
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    bullet_points = []

    for chunk in chunks:
        result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        sentences = result.split('. ')
        for sentence in sentences:
            cleaned = clean_text(sentence.strip())
            if cleaned:
                bullet_points.append(f"• {textwrap.fill(cleaned, width=100)}")
    return "\n\n".join(bullet_points)


def run_pdf_summarizer():
    st.markdown("""
    <h1 style='color: #a970ff; font-family: "Segoe UI", sans-serif;'>AI-Powered PDF Summarizer</h1>
    <p style='color: #a970ff; font-size: 1.1rem; font-family: "Segoe UI", sans-serif;'>Upload a PDF and get a bullet-point summary!</p>
    """, unsafe_allow_html=True)

    # 🟣 Hidden label by setting to empty string
    uploaded_file = st.file_uploader("📄Upload your PDF here!", type="pdf")

    if uploaded_file:
        st.info("⏳ Extracting and summarizing text...")

        try:
            raw_text = extract_text_from_pdf(uploaded_file)

            if not raw_text.strip():
                st.error("❌ No text found in the PDF!")
            else:
                cleaned_text = clean_text(raw_text)
                summary = summarize_text_to_bullets(cleaned_text)

                st.success("✅ Summary Generated!")
                st.markdown("<h3 style='color: white;'>📌 Summary:</h3>", unsafe_allow_html=True)

                st.markdown(f"<div style='color: #5e1f8c; white-space: pre-wrap; font-family: Segoe UI;'>{summary}</div>", unsafe_allow_html=True)

                st.download_button(
                    label="📥 Download Summary (.txt)",
                    data=summary,
                    file_name="../summary_output.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")