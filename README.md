# LegalMind AI

An intelligent, bilingual legal assistant for Pakistani law — built as a Final Year Project (FYP).

LegalMind AI helps users navigate the legal system by providing contextual, source-cited answers to legal questions in both **Urdu and English**, alongside tools for case management, document analysis, and legal document generation.

---

## ✨ Features

- 🔐 **Secure Authentication** — JWT-based sign-up and login
- 📂 **Case Management** — Create and organise legal cases
- 🤖 **RAG-Powered Legal Chat** — Answers grounded in real legal sources with citations, supporting Urdu and English
- 📋 **Intake Summary Generator** — Structured intake form → professional case summary
- 📝 **Legal Draft Generator** — Auto-generate notices, complaints, and agreements
- ✅ **Compliance & Risk Checklist Generator** — Step-by-step preparation checklist per case type
- 📄 **Document Upload with OCR** — Upload PDFs or images (JPG/PNG) and extract text automatically
- 🌐 **Urdu & English Support** — Full bilingual experience throughout the platform

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, PassLib / bcrypt, PyPDF2, Pytesseract |
| AI / ML | Google Gemini, Sentence Transformers (`all-MiniLM-L6-v2`), Pinecone |
| Frontend | React, React Router |
| Auth | JWT (python-jose) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- A `.env` file with your API keys (see `config.py` for required variable names — **never commit real keys**)

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# Install dependencies
npm install

# Start the dev server
npm start
```

The app will be available at `http://localhost:3000` (frontend) and `http://localhost:8000` (API).

---

## 📁 Project Structure

```
├── main.py                  # FastAPI app — all API endpoints
├── rag_engine.py            # RAG pipeline (Gemini + Pinecone + SentenceTransformers)
├── auth.py                  # JWT authentication helpers
├── config.py                # App settings (reads from .env)
├── document_processor.py   # PDF/image ingestion and OCR
├── conversation_handler.py  # Multi-turn conversation logic
├── practical_guidance.py    # Practical legal guidance helpers
├── App.js                   # React app entry point and routing
├── ChatInterface.js         # Main chat UI component
├── Signup.js                # Sign-up form component
├── login.js                 # Login form component
├── requirements.txt         # Python dependencies
└── docs/
    └── linkedin-launch-kit.md  # LinkedIn FYP announcement guide
```

---

## 📣 Sharing on LinkedIn

We prepared a complete LinkedIn launch kit for announcing this project as a Final Year Project.

👉 **[docs/linkedin-launch-kit.md](docs/linkedin-launch-kit.md)**

It includes:
- A ready-to-post LinkedIn caption (first-person, FYP-focused)
- Shorter caption variants and hashtag sets
- Step-by-step instructions on which app screens to screenshot
- A recommended 45–75 second screen recording flow
- Guidance on which code files/modules to highlight — and what to blur/avoid

---

## 🔒 Security Notes

- Never commit `.env` files or expose API keys in screenshots or posts.
- Use demo accounts (not real personal data) when recording demos.
- Refer to the "What to blur / avoid" section in the LinkedIn launch kit before posting.

---

## 📄 License

This project was developed as an academic Final Year Project. Please contact the authors before reusing or adapting the code.
