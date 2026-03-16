# LegalMind AI

An intelligent legal assistant built as a Final Year Project by students of the **Software Engineering** department at **Mirpur University of Science and Technology (MUST)**.

LegalMind AI makes legal knowledge accessible to everyone — regardless of background or budget — with bilingual support (Urdu & English), AI-powered Q&A, document analysis, and legal document generation.

---

## Features

- 🔐 Secure authentication & user management (JWT)
- 📁 Case management — create, track, and organise legal cases
- 🤖 RAG-powered Q&A with cited sources (Pinecone + SentenceTransformers + Gemini)
- 📋 Intake summary generator
- 📝 Legal draft generator (applications, notices, contracts)
- ✅ Compliance & risk checklist generator
- 📄 Document upload with OCR (PDF & images via PyPDF2 + pytesseract)
- 🌐 Bilingual — Urdu 🇵🇰 and English

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI |
| Database ORM | SQLAlchemy |
| Authentication | JWT (python-jose) |
| Vector Search | Pinecone |
| Embeddings | SentenceTransformers |
| LLM | Google Gemini |
| PDF Parsing | PyPDF2 |
| OCR | pytesseract |
| Frontend | React |

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Tesseract OCR installed on the system

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (copy .env.example and fill in your keys)
cp .env.example .env

# Start the API server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
npm install
npm start
```

---

## Sharing on LinkedIn

Planning to share LegalMind AI on LinkedIn? We've put together a ready-to-use launch kit with copy-paste captions, hashtag sets, screenshot guides, and a screen-recording script:

👉 **[docs/linkedin-launch-kit.md](docs/linkedin-launch-kit.md)**

---

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── auth.py          # JWT authentication
│   ├── rag_engine.py    # RAG pipeline
│   └── config.py        # App configuration
├── docs/
│   └── linkedin-launch-kit.md
├── App.js               # React entry point
├── ChatInterface.js     # Q&A interface
├── requirements.txt
└── README.md
```

---

## License

This project was developed for academic purposes as a Final Year Project at Mirpur University of Science and Technology.
