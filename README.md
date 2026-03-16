# LegalMind AI

A bilingual (Urdu/English) AI-powered legal assistant for Pakistan, built with FastAPI, Google Gemini, Pinecone RAG, and React.

## Features

- 🤖 **AI Legal Q&A** — Answers grounded in Pakistani law via RAG (Pinecone + SentenceTransformers + Gemini)
- 📋 **Case Intake** — Structured intake forms with AI-generated case summaries
- 📝 **Legal Draft Generation** — Generate notices, agreements, and formal letters
- ✅ **Compliance Checklists** — Step-by-step checklists by case type and jurisdiction
- 📄 **Document Upload & OCR** — Upload PDFs or images and receive an AI summary
- 🌐 **Bilingual Support** — Full Urdu ↔ English detection and translation
- 🎤 **Voice Query** — Ask by voice, receive a spoken response
- 🔐 **Secure Auth** — JWT-based signup/login

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python) |
| Authentication | JWT · python-jose · passlib/bcrypt |
| LLM | Google Gemini 2.5 Flash |
| Vector Database | Pinecone (Serverless) |
| Embeddings | SentenceTransformers — `all-MiniLM-L6-v2` |
| OCR | pytesseract · Pillow |
| PDF Parsing | PyPDF2 |
| Translation | googletrans |
| Text-to-Speech | gTTS |
| Voice Input | SpeechRecognition |
| Frontend | React |

## Getting Started

### Backend

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
npm install
npm start
```

## Sharing on LinkedIn

Ready to share this project? See **[docs/linkedin-launch-kit.md](docs/linkedin-launch-kit.md)** for:

- Three ready-to-paste LinkedIn caption options (short, medium, long)
- Suggested hashtag sets
- Call-to-action suggestions
- Exact screenshots to capture and a step-by-step screen recording guide
