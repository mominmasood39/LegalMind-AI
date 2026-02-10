import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from backend.config import settings
from backend.conversation_handler import ConversationHandler
from backend.practical_guidance import PracticalGuidance
from googletrans import Translator
import re

class RAGEngine:
    def __init__(self):
        # Initialize Gemini (for chat)
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize local embedding model (FREE)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Pinecone
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = pc.Index(settings.PINECONE_INDEX_NAME)
        
        self.translator = Translator()
        self.conversation = ConversationHandler()
        self.guidance = PracticalGuidance()
        print("✓ RAG Engine initialized")
    
    def detect_language(self, text):
        urdu_pattern = re.compile(r'[\u0600-\u06FF]')
        if urdu_pattern.search(text):
            return 'urdu'
        return 'english'
    
    def translate_text(self, text, target_lang='en'):
        try:
            if target_lang == 'en':
                result = self.translator.translate(text, src='ur', dest='en')
                return result.text
            else:
                result = self.translator.translate(text, src='en', dest='ur')
                return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
    
    def is_non_legal_query(self, text: str):
        """Detect clearly non-legal or gibberish inputs"""
        text = text.lower().strip()
        if len(text.split()) < 3:
            return True
        
        legal_keywords = [
            # General legal terms
            "law", "legal", "section", "punishment", "fir", "police",
            "court", "bail", "case", "rights", "ppc", "crpc",
            "constitution", "crime", "complaint", "harassment",
            "notice", "summons", "warrant", "hearing", "trial",
            "advocate", "lawyer", "judge", "magistrate",
            
            # Common incidents and offenses
            "theft", "stolen", "steal", "robbery", "burglary",
            "assault", "fight", "kidnap", "abduction", "fraud",
            "forgery", "cheque", "cyber", "blackmail", "extortion",
            "rape", "molestation", "domestic", "violence",
            "property", "tenant", "rent", "landlord", "eviction",
            "divorce", "khula", "maintenance", "custody", "nikah",
            "inheritance", "will", "contract", "agreement", "salary",
            "termination", "work", "employer", "employee"
        ]
        
        return not any(word in text for word in legal_keywords)
    
    def retrieve_relevant_chunks(self, query, top_k=5):
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        retrieved_chunks = []
        for match in results['matches']:
            retrieved_chunks.append({
                'text': match['metadata'].get('text', ''),
                'document': match['metadata'].get('document', ''),
                'section': match['metadata'].get('section', ''),
                'score': match['score']
            })
        return retrieved_chunks
    
    def generate_response(self, query, language='english'):
        original_query = query
        if language == 'urdu':
            query = self.translate_text(query, target_lang='en')
            print(f"Translated query: {query}")
        
        print("Retrieving relevant legal documents...")
        chunks = self.retrieve_relevant_chunks(query, top_k=5)
        
        if not chunks or (chunks and chunks[0]['score'] < 0.3):
            if self.is_non_legal_query(original_query):
                non_legal_msg = "Please ask a relevant legal question so I can assist you properly."
                if language == 'urdu':
                    non_legal_msg = self.translate_text(non_legal_msg, target_lang='ur')
                return {'answer': non_legal_msg, 'sources': [], 'language': language}
            
            low_conf_msg = (
                "I want to answer accurately, but I need a bit more context. Please tell me:\n"
                "1. Your province/city\n"
                "2. What exactly happened\n"
                "3. Whether there is any FIR, notice, contract, or court case number\n\n"
                "Then I'll guide you with the most relevant steps."
            )
            if language == 'urdu':
                low_conf_msg = self.translate_text(low_conf_msg, target_lang='ur')
            return {'answer': low_conf_msg, 'sources': [], 'language': language}
        
        context = "\n\n".join([chunk['text'] for chunk in chunks])
        
        prompt = f"""You are LegalMind AI, a friendly and supportive Pakistani legal assistant.
Always be polite, empathetic, and user-friendly.

You must follow user instructions about answer length and style:
- If the user asks for "brief", "short", "2 lines", "3 lines", or "4 lines", respond concisely in that length.
- If the user asks for "detailed" or "in detail", respond with a full explanation.
- If the user asks for "points" or "list", answer in numbered points.
- If the user greets (hi/hello/assalam), respond with a greeting and offer help.

Use ONLY the legal context provided below. Do NOT invent facts.

LEGAL CONTEXT:
{context}

QUESTION: {query}

INSTRUCTIONS:
1. Answer based ONLY on the provided context.
2. Cite specific sections when available, but do NOT mention document names or filenames.
3. Be clear, conversational, and helpful.
4. If the question asks "what should I do" or involves a victim, ALSO explain:
   - Immediate steps
   - Evidence to preserve
   - How to report (FIR/complaint)
   - Documents needed
5. If the context is insufficient, politely ask for more details instead of refusing.
6. Use plain text only. NO markdown, NO **, NO *.

ANSWER:"""
        
        print("Generating response...")
        try:
            response = self.model.generate_content(prompt)
            answer = response.text
            answer = answer.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
        except Exception as e:
            print(f"Generation error: {e}")
            answer = "I encountered an error generating the response. Please try again."
        
        practical_steps = ""
        if self.guidance.should_add_guidance(original_query):
            print("Adding practical guidance...")
            practical_steps = self.guidance.get_guidance(original_query)
            if practical_steps and "GENERAL LEGAL GUIDANCE" not in practical_steps:
                answer += "\n" + "="*60 + practical_steps
        
        if language == 'urdu':
            print("Translating response to Urdu...")
            answer = self.translate_text(answer, target_lang='ur')
        
        sources = [
            {'document': chunk['document'], 'section': chunk['section'], 'relevance_score': round(chunk['score'], 3)}
            for chunk in chunks[:3]
        ]
        
        return {'answer': answer, 'sources': sources, 'language': language, 'original_query': original_query}
    
    def query(self, user_query, user_id='default'):
        intent = self.conversation.detect_intent(user_query)
        print(f"Detected intent: {intent}")
        
        # Catch irrelevant input even if intent looks legal
        if intent == 'legal' and self.is_non_legal_query(user_query):
            return {
                'answer': "Please ask a relevant legal question so I can assist you properly.",
                'sources': [],
                'language': 'english',
                'intent': 'irrelevant'
            }
        
        if self.conversation.should_skip_rag(intent):
            answer = self.conversation.get_response(intent, user_id)
            return {'answer': answer, 'sources': [], 'language': 'english', 'intent': intent}
        
        language = self.detect_language(user_query)
        print(f"Detected language: {language}")
        
        result = self.generate_response(user_query, language)
        result['intent'] = 'legal'
        result['sources'] = []
        return result