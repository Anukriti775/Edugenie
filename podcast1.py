import streamlit as st #podcast_generator.py
from PyPDF2 import PdfReader
from gtts import gTTS
import tempfile

import streamlit as st

def run_podcast_generator():
    st.title("🎙 Podcast Generator")
    st.markdown("Turn your study material into voice podcasts.")

    if st.button("🔙 Back to Home"):
        st.session_state.tool_selector = None
        st.rerun()

    uploaded_file = st.file_uploader("Upload PDF or Notes", type=["pdf", "txt"])
    if uploaded_file:
        st.success("📚 Content loaded.")
        st.markdown("🔊 Generating podcast...")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")


def extract_pdf_text(uploaded_file, selected_pages):
    reader = PdfReader(uploaded_file)
    text = ""
    for i in selected_pages:
        if 0 <= i < len(reader.pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def generate_audio(text, lang='en', speed=1.0):
    tts = gTTS(text, lang=lang, slow=False)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

def run_podcast_generator():
    st.markdown("""
    <h1 style='color: #a970ff; font-family: "Segoe UI", sans-serif;'>Podcast Generator</h1>
    <p style='color: #a970ff; font-size: 1.1rem; font-family: "Segoe UI", sans-serif;'>Convert summaries into AI-narrated podcasts for quick listening.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📄Upload your PDF here!", type=["pdf"])
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)

        # Select pages to read
        st.markdown(f"🧾 This PDF has {total_pages} pages")
        page_range = st.text_input("Enter page numbers (e.g., 1-3, 2, or all):", value="all")

        # Select speed
        speed_option = st.select_slider("🎚 Select Playback Speed", options=["1x", "1.5x", "2x"], value="1x")
        speed_map = {"1x": 1.0, "1.5x": 1.2, "2x": 1.4}

        if page_range.lower() == "all":
            selected_pages = list(range(total_pages))
        elif "-" in page_range:
            try:
                start, end = map(int, page_range.split("-"))
                selected_pages = list(range(start - 1, end))
            except:
                st.error("❌ Invalid page range.")
                return
        else:
            try:
                selected_pages = [int(page_range) - 1]
            except:
                st.error("❌ Invalid input.")
                return

        # Extract and display text
        full_text = extract_pdf_text(uploaded_file, selected_pages)
        if not full_text:
            st.error("❌ Could not extract any text.")
            return

        st.markdown("<h3 style='color: white;'>📜 Subtitles (Transcript)</h3>", unsafe_allow_html=True)

        st.text_area("Subtitle Preview", full_text, height=250)

        if st.button("🎧 Generate & Play Podcast"):
            with st.spinner("Generating podcast..."):
                audio_file = generate_audio(full_text, speed=speed_map[speed_option])
                st.success("✅ Podcast ready!")

                # Audio Player with Controls
                st.markdown("### ▶ Audio Player")
                st.audio(audio_file, format="audio/mp3")

                st.info("You can use the built-in audio controls (Pause, Resume, Restart) below the player.")