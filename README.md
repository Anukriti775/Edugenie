📘 EduGenie — Your one step away study partner

(PDF Summarizer • Quiz Generator • Podcast Converter • Chat with PDF)

PDF Genie is an AI-powered Flask application that lets users upload any PDF and instantly perform multiple intelligent tasks:

📄 Summarize long PDF documents

🎧 Convert summary to Podcast (Text-to-Speech)

📝 Generate Quizzes (MCQs) from PDF content

💬 Chat with your PDF — ask questions and get intelligent answers

This project was developed using Python 3.11, Flask, Transformers, Sentence Transformers, and gTTS, and built using PyCharm.

🚀 Features
🔹 1. PDF Summarizer

Extracts text from the uploaded PDF and generates concise summaries using modern transformer models.

🔹 2. Podcast Generator

Converts the generated summary into natural speech using gTTS and produces downloadable MP3 files.

🔹 3. Quiz Generator (MCQs)

Creates automatic quizzes based on the document content — useful for study, revision, and interactive learning.

🔹 4. Chat with your PDF

Uses embeddings + FAISS vector search to retrieve relevant sections of the PDF and gives intelligent answers.
Supports OpenAI API for high-quality answers (optional).

🔹 5. Modular Architecture

Codebase is split into multiple files:

app.py                → Main Flask application  
utils.py              → File management + PDF extraction  
summarizer.py         → AI summarization logic  
podcast.py            → Text-to-speech generation  
quizzes.py            → Quiz generator  
chat_pdf.py           → Embeddings + FAISS + Chat logic  
uploads/              → Uploaded PDFs  
outputs/              → Generated files (mp3/json/txt)

🛠️ Technologies Used
Category	Technologies
Backend	Python 3.11, Flask
AI Models	Hugging Face Transformers, Sentence Transformers
Embeddings	all-MiniLM-L6-v2
Vector Search	FAISS CPU
NLP	Transformers library, PDFPlumber
Speech	Google gTTS
UI	HTML (Flask Templates)
Tools & IDE	PyCharm, VS Code
📁 Project Structure
pdf-genie/
│── app.py
│── utils.py
│── summarizer.py
│── podcast.py
│── quizzes.py
│── chat_pdf.py
│── requirements.txt
│── .env          # (optional for OpenAI key)
│── uploads/
│── outputs/

⚙️ Installation & Setup (PyCharm)
1️⃣ Clone the project
git clone https://github.com/your-username/pdf-genie.git
cd pdf-genie

2️⃣ Create a Python 3.11 virtual environment

In PyCharm:
File → Settings → Project → Python Interpreter → Add Interpreter → Python 3.11

Or using terminal:

py -3.11 -m venv venv
venv\Scripts\activate

3️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ (Optional) Add OpenAI API key

Create a .env file:

OPENAI_API_KEY=your_api_key_here

5️⃣ Run the Flask app
python app.py


Open in browser:
👉 http://127.0.0.1:5000

🖼️ Screenshots

(Add these once you take them)

📤 PDF Upload Page

📄 Summary Download

🎧 Podcast (MP3) Output

📝 Quiz JSON File

💬 Chat with PDF

🧠 How It Works (Architecture)
🔹 1. PDF → Text

pdfplumber extracts raw text.

🔹 2. Text → Summary

transformers summarization pipeline.

🔹 3. Summary → Speech

gTTS converts text into MP3.

🔹 4. Text → Quiz

Custom logic extracts sentences → key terms → MCQs.

🔹 5. Text → Embeddings → FAISS

SentenceTransformer converts text chunks into embeddings.
FAISS performs semantic search to answer user questions.

📦 Requirements

See: requirements.txt

Includes:

Flask

Transformers

Sentence-Transformers

FAISS-CPU

pdfplumber

gTTS

OpenAI (optional)

🏆 Why This Project Matters

This project demonstrates strong skills in:

✔ AI/ML model integration
✔ Backend development with Flask
✔ Natural Language Processing
✔ Vector search (FAISS)
✔ Full-stack problem solving
✔ Clean modular code architecture
✔ Deployable, real-world application
