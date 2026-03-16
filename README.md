# LegalMind AI

An AI-powered Pakistani legal assistant that supports end-to-end case workflows — from intake and document analysis to legal drafts, compliance checklists, and RAG-based Q&A.

## Features

- **Case management** — create and organise cases with full message history
- **Legal Q&A (RAG)** — ask questions and get answers backed by retrieved legal sources
- **Case intake** — submit facts and receive a structured case summary
- **Legal draft generator** — generate notices, agreements, and other documents
- **Compliance checklist** — risk and compliance checklist for a given case type
- **Document upload** — PDF parsing and image OCR with automatic summarisation
- **Urdu / English support** — responses in the language of your choice

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, JWT (python-jose) |
| AI / RAG | Google Gemini, SentenceTransformers, Pinecone |
| Document processing | PyPDF2, Tesseract OCR (Pillow) |
| Auth | bcrypt, OAuth2 password flow |

## Getting Started

### Prerequisites

- Python 3.10+
- A [Pinecone](https://www.pinecone.io/) account and index
- A [Google AI Studio](https://aistudio.google.com/) API key (Gemini)
- Tesseract OCR installed on your system

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mominmasood39/LegalMind-AI.git
cd LegalMind-AI

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Copy and fill in environment variables
cp .env.example .env   # edit .env with your keys

# 4. Start the backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy connection string (e.g. `sqlite:///./legalmind.db`) |
| `SECRET_KEY` | Secret key for JWT signing |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX` | Name of your Pinecone index |
| `GEMINI_API_KEY` | Google Gemini API key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes (default: `60`) |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/signup` | Register a new user |
| `POST` | `/login` | Obtain a JWT access token |
| `GET` | `/me` | Current user details |
| `POST` | `/cases` | Create a new case |
| `GET` | `/cases` | List all cases for the current user |
| `POST` | `/query` | Ask a legal question (RAG) |
| `POST` | `/cases/{id}/intake` | Submit intake form |
| `POST` | `/cases/{id}/draft` | Generate a legal draft |
| `POST` | `/cases/{id}/checklist` | Generate a compliance checklist |
| `POST` | `/cases/{id}/documents` | Upload a PDF or image document |
| `GET` | `/admin/summary` | Admin statistics (admin role required) |

## Getting Help / Sharing Recordings

If you run into a bug or unexpected behaviour, please open an [issue](../../issues) and attach a screen recording or screenshots to help us diagnose the problem quickly.

Read **[docs/support-media.md](docs/support-media.md)** for:

- Preferred recording formats (MP4, WebM) and maximum size guidance
- How to share large files via YouTube Unlisted or Google Drive
- Privacy guidance — how to blur PII, tokens, and email addresses before sharing
- What to capture in your recording for UI issues (Network tab, Console, backend logs)

## Contributing

Pull requests are welcome. For major changes please open an issue first to discuss what you would like to change.

## License

This project is released under the [MIT License](LICENSE).
