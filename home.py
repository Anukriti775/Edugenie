# home.py
import streamlit as st
import json
import time
from streamlit_lottie import st_lottie
from PIL import Image
from Edugenie.pdf_summarizer import run_pdf_summarizer
from chatbot import run_chatbot
from podcast_generator import run_podcast_generator
from flashcard_generator import run_flashcard_generator

# ---------------------
# Page Config
# ---------------------
st.set_page_config(page_title="EduGenie - Learn Smarter", layout="wide")

# ---------------------
# Splash Screen (Optional)
# ---------------------
def load_lottie_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    st.markdown("<h1 style='text-align:center;'>✨ Welcome to EduGenie ✨</h1>", unsafe_allow_html=True)
    lottie_json = load_lottie_file("../transparent_loader.json")
    if lottie_json:
        st_lottie(lottie_json, height=300, key="splash")
    else:
        st.warning("⚠ Lottie animation not found!")
    st.markdown("<p style='text-align:center;'>Your AI Learning Companion is Loading...</p>", unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.splash_done = True
    st.rerun()


if "tool_selector" not in st.session_state:
    st.session_state.tool_selector = None

# ---------------------
# Styles
st.markdown("""
<style>
/* --------------------- */
/* PDF Chatbot Text & Input Styling */
/* --------------------- */

/* Chat bubbles (both user + bot) */
div[data-testid="chatMessageContent"], 
div[data-testid="stMarkdownContainer"] p {
    color: white !important;
}

/* Style the chat input box (textarea/input) */
textarea, input[type="text"] {
    background-color: #6a0dad !important;  /* Inner Purple */
    color: white !important;               /* White text inside */
    border: 1px solid #a970ff !important;  /* Optional: glowing purple border */
    border-radius: 20px !important;        /* Rounded shape */
}

/* Override outer white container (form or container) */
div:has(> input[type="text"]), 
div:has(> textarea) {
    background-color: #2A0134 !important;  /* Purple outer container */
    padding: 10px;
    border-radius: 20px;
}

/* Optional: make sure the full chat form doesn’t render white */
section[data-testid="stChatInput"] {
    background-color: #2A0134 !important;
}

/* File uploader placeholder and text */
span[data-testid="stFileUploaderDropzoneText"] {
    color: white !important;
}

/* Input box placeholder */
input::placeholder, textarea::placeholder {
    color: #d3bdf0 !important;  /* Light lavender */
    opacity: 0.9;
}

/* Text inside text input box */
input, textarea {
    color: white !important;
}

/* Global font and background */
body {
  background-color: #0f0f1c !important;
  color: #f0f0f0;
  font-family: 'Segoe UI', sans-serif;
  overflow-x: hidden;
}
.stApp {
  background: radial-gradient(circle at top, rgba(26, 26, 46, 0.95), rgba(15, 15, 28, 0.95)) !important;
}

/* --------------------- */
/* Sidebar Styling */
/* --------------------- */
[data-testid="stSidebar"] {
  background-color: #2A0134!important; /* Purple sidebar */
  color: white !important;
}
[data-testid="stSidebar"] * {
  color: white !important;
}

/* Tagline fix */
.custom-tagline {
    text-align: left;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.6;
    padding: 15px 20px;
    border-left: 5px solid #a970ff;
    border-radius: 8px;
    background: rgba(169, 112, 255, 0.07);
    color: white !important;
    box-shadow: inset 0 0 12px #a970ff44;
    margin-bottom: 20px;
    animation: glowLeft 2s infinite alternate;
}
@keyframes glowLeft {
    0%   { border-left-color: #a970ff44; }
    100% { border-left-color: #c084fc; }
}

/* --------------------- */
/* CARD Design - Tools  */
/* --------------------- */
.card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.card:hover {
  transform: scale(1.03);
  box-shadow: 0 0 25px rgba(173, 108, 255, 0.8);
}

/* Button Styles */
.stButton > button {
  background-color: #6a0dad; /* Purple */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
}
.stButton > button:hover {
  background-color: #5e0c9e; /* Darker purple */
}

/* Feature Tiles Section */
.feature {
  background: rgba(255,255,255,0.03);
  padding: 15px;
  border-radius: 16px;
  transition: 0.3s ease;
  border: 1px solid #a970ff33;
  box-shadow: 0 0 10px #a970ff22;
  color: white;
}
.feature:hover {
  box-shadow: 0 0 25px #a970ffaa;
  background: linear-gradient(135deg, #1b122a, #2b1c3e);
}

/* Sidebar Menu Pulse on Hover */
.element-container:has(label:hover) span:first-child {
  display: inline-block;
  animation: pulseIcon 0.7s infinite alternate;
}
@keyframes pulseIcon {
  0% { transform: scale(1); filter: drop-shadow(0 0 1px #a970ff); }
  100% { transform: scale(1.2); filter: drop-shadow(0 0 8px #a970ff); }
}

/* Genie animation */
@keyframes flyAcross {
  0% { transform: translateX(100vw); opacity: 0; }
  25% { opacity: 1; }
  50% { transform: translateX(50vw); }
  75% { transform: translateX(20vw); }
  100% { transform: translateX(-100vw); opacity: 0; }
}
#genie-fly {
  position: fixed;
  bottom: 160px;
  left: 0;
  width: 250px;
  z-index: 10;
  animation: flyAcross 4s ease-in-out forwards;
  pointer-events: none;
}
</style>
""", unsafe_allow_html=True)




# ---------------------
# Header
# ---------------------
def show_homepage():
    col1, col2 = st.columns([8, 1])
    with col2:
        try:
            logo = Image.open("../logo.jpg")
            st.image(logo, width=100)
        except:
            st.warning("⚠ Logo not found!")

    st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; animation: fadeIn 2s;">
            <div style="font-size:32px; font-weight:bold; color:#a970ff;">
                ✨ Welcome to EduGenie ✨...your tutor AI companion
            </div>
            <h3 style='text-align: center; color: #f0f0f0;'>Your tutor AI companion</h3>
            <p style='text-align: center; color: #aaa;'>AI-powered PDF summarizer that turns your learning into flashcards, quizzes, notes, and podcasts.</p>
        </div>
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

# Show homepage after splash screen
show_homepage()


# ---------------------
# Sidebar (Toggle Menu)
# ---------------------
with st.sidebar:
    st.markdown("""
    <style>
    .custom-tagline {
        text-align: left;
        font-size: 22px;
        font-weight: 800;
        line-height: 1.6;
        padding: 15px 20px;
        border-left: 5px solid #a970ff;
        border-radius: 8px;
        background: rgba(169, 112, 255, 0.07);
        color: #A9A9A9;
        box-shadow: inset 0 0 12px #a970ff44;
        margin-bottom: 20px;
        animation: glowLeft 2s infinite alternate;
    }

    @keyframes glowLeft {
        0%   { border-left-color: #a970ff44; }
        100% { border-left-color: #c084fc; }
    }
    </style>

    <div class='custom-tagline'>
        🚀 Revise Smart<br>
        ⚡ Learn Fast<br>
        🤖 Ask Anything.
    </div>
    """, unsafe_allow_html=True)

    tool = st.radio(" ", [
        "🏠 Home",
        "✨ Features",
        "⚙ Settings"
    ])

# ---------------------
# Tool Cards (Updated for working buttons)
# ---------------------
if tool == "🏠 Home":
    st.markdown("<h3 style='color: white;'>📚 Learn Smarter. Summarize Faster.</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='color: white;'>Choose your tool:</h5>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='card'>
            <h3 style='color:#a970ff;'>📄 PDF Summarizer</h3>
            <p style='color: white;'>Summarize long study PDFs into bite-sized notes.</p>""", unsafe_allow_html=True)
        if st.button("📄 Try Now"):
            st.session_state.tool_selector = "summarizer"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class='card'>
            <h3 style='color:#a970ff;'>🤖 PDF Chatbot</h3>
            <p style='color: white;'>Chat with your PDF like a smart tutor.</p>""", unsafe_allow_html=True)
        if st.button("🤖 Chat Now"):
            st.session_state.tool_selector = "chatbot"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""<div class='card'>
            <h3 style='color:#a970ff;'>🎙 Podcast Generator</h3>
            <p style='color: white;'>Convert PDFs into voice notes.</p>""", unsafe_allow_html=True)
        if st.button("🎧 Listen"):
            st.session_state.tool_selector = "podcast"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("""<div class='card'>
            <h3 style='color:#a970ff;'>🧠 Flashcards & Quizzes</h3>
            <p style='color: white;'>Auto-generate flashcards and quizzes.</p>""", unsafe_allow_html=True)
        if st.button("🧠 Practice"):
            st.session_state.tool_selector = "flashcards"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------
# Features Section
# ---------------------
if tool == "✨ Features":
    col1, col2 = st.columns(2)

    with col1:
        st_lottie(load_lottie_file("../Book_Spirit.json"), height=200, speed=1)
        st.markdown("""
        <div class='feature'>
            <h4>📄 Smart PDF Notes</h4>
            <p>Extract only the most important content and auto-summarize it into neat points.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st_lottie(load_lottie_file("../Mic.json"), height=200, speed=1)
        st.markdown("""
        <div class='feature'>
            <h4>🎧 Podcastify</h4>
            <p>Let AI read your notes out loud so you can learn on the go!</p>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st_lottie(load_lottie_file("../Quizes.json"), height=200, speed=1)
        st.markdown("""
        <div class='feature'>
            <h4>🧠 Flashcards & Quizzes</h4>
            <p>Convert material into quick revision cards and MCQs instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st_lottie(load_lottie_file("../Bot.json"), height=200, speed=1)
        st.markdown("""
        <div class='feature'>
            <h4>💬 Chat with Docs</h4>
            <p>Ask questions and get answers from any PDF document you upload.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------
# Footer
# ---------------------
st.markdown("""
<br><hr>
<div style='text-align:center; font-size: 13px; color: #999;'>
    Made with ❤ by <strong>EduGenie Team</strong> ©
</div>
""", unsafe_allow_html=True)

#-------------




# Zeintsi AI bot
st.markdown("""
    <style>
    @keyframes floatUpDown {
        0% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0); }
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 10px #fef08a; }
        50% { box-shadow: 0 0 30px #facc15, 0 0 60px #fcd34d; }
        100% { box-shadow: 0 0 10px #fef08a; }
    }

    @keyframes lightningStrike {
        0% {
            opacity: 0;
            transform: scale(0.5) rotate(0deg);
        }
        50% {
            opacity: 1;
            transform: scale(1.2) rotate(20deg);
        }
        100% {
            opacity: 0;
            transform: scale(1.6) rotate(-15deg);
        }
    }

    .zenitsu-wrapper {
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        animation: floatUpDown 2s ease-in-out infinite;
    }

    .zenitsu-speech {
        background: #fff8c6;
        color: #4a2d00;
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
        position: relative;
    }

    .zenitsu-speech::after {
        content: "";
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        border-width: 8px;
        border-style: solid;
        border-color: #fff8c6 transparent transparent transparent;
    }

    .zenitsu-aura-button {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid #facc15;
        background: radial-gradient(circle, #fef08a, #facc15);
        box-shadow:
            0 0 15px #fde047,
            0 0 30px #fbbf24,
            0 0 45px #facc15 inset;
        animation: pulse 2s infinite;
        cursor: pointer;
        position: relative;
    }

    .zenitsu-aura-button img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        z-index: 1;
    }

    .lightning {
        position: absolute;
        width: 40px;
        height: 80px;
        top: -15px;
        left: 20px;
        background: linear-gradient(45deg, #fff700, #facc15, #fcd34d);
        clip-path: polygon(50% 0%, 60% 30%, 40% 40%, 60% 60%, 30% 80%, 50% 100%);
        animation: lightningStrike 0.6s ease-in-out infinite;
        z-index: 2;
        opacity: 0;
        pointer-events: none;
    }

    .zenitsu-aura-button:hover .lightning {
        opacity: 1;
    }
    </style>

    <div class="zenitsu-wrapper">
        <div class="zenitsu-speech">Genie is here to help u.</div>
        <a href='?tool_selector=🤖+PDF+Chatbot'>
            <div class='zenitsu-aura-button'>
                <div class="lightning"></div>
                <img src='data:image/jpeg;base64,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' alt='Zenitsu Bot'>
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)

if st.session_state.tool_selector == "summarizer":
    run_pdf_summarizer()
elif st.session_state.tool_selector == "chatbot":
    run_chatbot()
elif st.session_state.tool_selector == "podcast":
    run_podcast_generator()
elif st.session_state.tool_selector == "flashcards":
    run_flashcard_generator()

