# LinkedIn Launch Kit — LegalMind AI

> Copy-paste ready assets for announcing LegalMind AI on LinkedIn as a Final Year Project.

---

## 1. Primary Caption (copy-paste ready)

```
🎓 We're excited to share our Final Year Project — LegalMind AI!

As students of the Software Engineering department at Mirpur University of Science and Technology (MUST), we set out to solve a real problem: legal knowledge and assistance is often inaccessible, expensive, and available only in English — leaving millions of people behind.

LegalMind AI is an intelligent legal assistant that bridges that gap. Here's what it can do:

✅ Secure authentication & user management
✅ Case management — create, track, and organise your legal cases
✅ RAG-powered Q&A with cited sources — ask any legal question and get answers backed by real documents
✅ Intake summary generator — fill in your case details and get a structured summary instantly
✅ Legal draft generator — generate formal legal documents (applications, notices, contracts) in seconds
✅ Compliance & risk checklist generator — never miss a critical step in your case
✅ Document upload with OCR — upload PDFs or images (scanned documents, photos) and extract text automatically
✅ Bilingual support — fully functional in both Urdu 🇵🇰 and English 🌐

We built LegalMind AI using a modern, production-grade stack:
🔧 FastAPI · SQLAlchemy · JWT authentication
🧠 Pinecone (vector search) · SentenceTransformers · Gemini (LLM)
📄 PyPDF2 · pytesseract (OCR)

This project is the result of months of research, late nights, and a genuine desire to make legal assistance accessible to everyone — regardless of their background or budget.

We'd love to hear your thoughts! 💬 Feel free to reach out, leave a comment, or share this with anyone who might benefit.

#LegalMindAI #FinalYearProject #FYP #SoftwareEngineering #MUST #MirpurUniversity #ArtificialIntelligence #LegalTech #NLP #RAG #Pakistan #MachineLearning #FastAPI #Pinecone #Gemini #OpenSource #StudentProject #AI #BuildInPublic #TechForGood
```

---

## 2. Hashtag Sets

### Broad (reach & discovery)
```
#LegalTech #AI #ArtificialIntelligence #MachineLearning #NLP #BuildInPublic #TechForGood #OpenSource #StudentProject #FinalYearProject #FYP #Pakistan
```

### Niche (technical & domain)
```
#RAG #RetrievalAugmentedGeneration #FastAPI #Pinecone #SentenceTransformers #Gemini #PyPDF2 #pytesseract #OCR #LegalAI #SoftwareEngineering #MUST #MirpurUniversity
```

---

## 3. Call-to-Action Lines

Choose one or combine:

- 💬 **"Drop a comment — what legal feature would you want to see next?"**
- 🔗 **"Check out the full project on GitHub → [link]"**
- 🤝 **"If you know anyone who needs affordable legal assistance, share this post."**
- 📩 **"DM us if you'd like a live demo or want to collaborate."**
- 🌟 **"Give the repo a ⭐ if you think accessible legal tech matters."**

---

## 4. Screenshots to Take (6–8 images)

Capture these screens for the LinkedIn carousel or image gallery:

| # | Screen | What to show |
|---|--------|-------------|
| 1 | **Login / Sign-up page** | Clean auth UI; obscure any test credentials |
| 2 | **Dashboard / Case list** | Several sample cases listed with titles and dates |
| 3 | **RAG Q&A — English** | A legal question typed in English with an answer and source citations visible |
| 4 | **RAG Q&A — Urdu** | Same Q&A interface with Urdu text to highlight bilingual support |
| 5 | **Intake Summary result** | Filled intake form on one side, generated summary on the other |
| 6 | **Legal Draft output** | Generated formal document (e.g., an application or notice) displayed in the UI |
| 7 | **Checklist output** | A numbered compliance/risk checklist for a sample case type |
| 8 | **Document Upload + OCR** | File upload panel with a PDF or image uploaded and extracted text shown |

> **Tip:** Use realistic-looking dummy data (e.g., "Muhammad Ali vs. XYZ Corporation") instead of real client names. Blur or crop any field that reveals personal or sensitive test data.

---

## 5. Screen Recording Flow (45–75 seconds)

Record in one continuous take at 1080p. Follow this script:

```
00:00 – 00:05  Open the app; show the landing / login page for a moment.
00:05 – 00:12  Log in with a demo account; land on the dashboard showing 2–3 sample cases.
00:12 – 00:22  Click into a case → open the Q&A tab → type a legal question in English → show the
               answer appearing with source citations highlighted.
00:22 – 00:30  Switch the language to Urdu → type the same question → show the Urdu response.
00:30 – 00:40  Navigate to the Draft Generator → fill in a "Notice to Vacate" → click Generate →
               show the formatted draft appearing on screen.
00:40 – 00:50  Navigate to Document Upload → upload a sample PDF → show the extracted text /
               summary result.
00:50 – 00:60  Navigate to the Checklist tab → select a case type (e.g., Tenancy Dispute) →
               click Generate → show the checklist items appearing.
00:60 – 00:75  Zoom out to the dashboard; end on the app logo / branding for a clean finish.
```

> **Audio:** Add a short background track (royalty-free) or record a 1–2 sentence voice-over introducing the project. Keep it under 75 seconds for LinkedIn's auto-play sweet spot.

---

## 6. Repo Files to Show / Highlight

### ✅ Safe to show publicly

**Backend**
- `backend/main.py` — FastAPI routes and app structure
- `backend/rag_engine.py` — RAG pipeline (Pinecone + SentenceTransformers + Gemini)
- `backend/auth.py` — JWT authentication logic
- `backend/config.py` — Configuration (settings class, not values)
- `requirements.txt` — Full tech stack at a glance

**Frontend**
- `App.js` — Main React app entry point
- `ChatInterface.js` — Q&A / chat interface component
- `Auth.css`, `ChatInterface.css`, `App.css` — UI styling

### ❌ Never share / always keep private

| File / Pattern | Reason |
|---------------|--------|
| `.env` | Contains `SECRET_KEY`, API keys (Pinecone, Gemini) |
| `users.json` | Contains user data |
| `processing_summary.json` | Internal processing metadata |
| Any `*.db` or `*.sqlite` file | Contains database records |
| `page_dump.html` | Internal debug artifact |

> **Rule of thumb:** If a file contains a key, token, password, or personal data — never show it, even partially, in screenshots or recordings.

---

## 7. Post Checklist (before you hit "Post")

- [ ] Caption copied and personalised (add your name / team names at the end)
- [ ] GitHub repo link added to the CTA
- [ ] 6–8 screenshots ready (no real personal data visible)
- [ ] Screen recording trimmed to 45–75 seconds
- [ ] `.env` and secrets **not** visible in any media
- [ ] Hashtags pasted at the end of the caption
- [ ] Tag your university page: search "Mirpur University of Science and Technology" on LinkedIn
- [ ] Tag your teammates and supervisor in the post
