import re
import random

class ConversationHandler:
    def __init__(self):
        self.abuse_count = {}
        self.sexual_count = {}
        
        self.templates = {
            'greeting': [
                "Assalam o Alaikum! Please ask a legal question about Pakistani law, and I will guide you.",
                "Hello! I can help with Pakistani legal questions. Please tell me your legal issue.",
                "Walaikum Assalam! Ask any Pakistani legal question and I will assist."
            ],
            'thanks': [
                "You're welcome! If you have another legal question, feel free to ask.",
                "Glad it helped. Ask anytime if you need more legal guidance.",
            ],
            'goodbye': [
                "Take care. If you need legal guidance again, I'm here.",
                "Allah Hafiz. Feel free to return with any legal question.",
            ],
            'capabilities': [
                "I can help with Pakistani law: FIR, bail, harassment, family matters, property, cybercrime, and more. Ask a legal question to begin.",
            ],
            'irrelevant': [
                "Please ask a relevant legal question so I can assist you properly.",
                "I’m focused on Pakistani legal guidance. Ask a legal question and I’ll help."
            ],
            'clarify': [
                "Please ask a clear legal question so I can guide you properly.",
                "To help you, please share a specific legal question."
            ],
            'offensive_1': "I understand you may be upset, but I can't respond to abusive language. If you explain your legal issue calmly, I'll do my best to help.",
            'offensive_2': "I'm here to help, but I need respectful language to continue. Please share the legal issue.",
            'offensive_3': "I can't continue if the language remains abusive. If you're ready to discuss your matter respectfully, I'll assist.",
            'sexual_1': "I can't engage in sexual or explicit conversation. If your question is about harassment, blackmail, consent-related legal rights, or cybercrime, I can help.",
            'sexual_2': "I'm not able to continue with sexual content. If you want legal guidance, share your issue in simple terms.",
            'sexual_3': "I can't assist with that. If you are facing harm, coercion, or blackmail, I can guide you on legal steps and safety-focused options in Pakistan.",
            'safety': "I'm sorry you're going through this. If you're in immediate danger or might hurt yourself or someone else, please contact local emergency services or a trusted person right now.\n\nIf you're in Pakistan and this is urgent, consider contacting 15 (police).",
        }
        
        self.patterns = {
            'greeting': [
                r'\b(hi|hello|hey|salam|salaam|assalam|aoa|good morning|good evening)\b',
            ],
            'thanks': [
                r'\b(thank|thanks|shukriya|jazak|appreciated|meharbani)\b',
            ],
            'goodbye': [
                r'\b(bye|allah hafiz|khuda hafiz|see you|take care|goodbye)\b',
            ],
            'capabilities': [
                r'\b(what can you do|help me|how to use|what are you|capabilities|menu|features)\b',
            ],
            'irrelevant': [
                r'\b(joke|funny|game|play|movie|music|food|weather|sports)\b',
            ],
            'unclear': [
                r'^\s*(\?+|help|hmm|uh|um)\s*$',
            ],
            'offensive': [
                r'\b(stupid|idiot|fool|useless|garbage|shit|fuck|damn)\b',
            ],
            'sexual': [
                r'\b(sex|sexy|nude|porn|dick|pussy|boobs)\b',
            ],
            'safety': [
                r'\b(suicide|kill myself|want to die|end it all|hurt myself)\b',
            ],
        }
    
    def normalize_text(self, text):
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'([!?.]){3,}', r'\1\1', text)
        return text
    
    def detect_intent(self, text):
        normalized = self.normalize_text(text)
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, normalized, re.IGNORECASE):
                    return intent
        if len(normalized.split()) <= 2 and '?' in normalized:
            return 'unclear'
        return 'legal'
    
    def get_response(self, intent, user_id='default'):
        if intent == 'offensive':
            count = self.abuse_count.get(user_id, 0)
            self.abuse_count[user_id] = count + 1
            if count == 0:
                return self.templates['offensive_1']
            elif count == 1:
                return self.templates['offensive_2']
            else:
                return self.templates['offensive_3']
        
        if intent == 'sexual':
            count = self.sexual_count.get(user_id, 0)
            self.sexual_count[user_id] = count + 1
            if count == 0:
                return self.templates['sexual_1']
            elif count == 1:
                return self.templates['sexual_2']
            else:
                return self.templates['sexual_3']
        
        if intent == 'safety':
            return self.templates['safety']
        
        if intent in self.templates:
            templates = self.templates[intent]
            if isinstance(templates, list):
                return random.choice(templates)
            return templates
        
        return random.choice(self.templates['clarify'])
    
    def should_skip_rag(self, intent):
        non_legal_intents = [
            'greeting', 'thanks', 'goodbye', 'capabilities',
            'irrelevant', 'unclear', 'offensive', 'sexual', 'safety'
        ]
        return intent in non_legal_intents
    
    def reset_user_state(self, user_id):
        if user_id in self.abuse_count:
            del self.abuse_count[user_id]
        if user_id in self.sexual_count:
            del self.sexual_count[user_id]