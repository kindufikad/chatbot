# nlp_engine.py
import re
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

class NLPEngine:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.synonyms = self.load_synonyms()
        self.faq_data = []
    
    def load_synonyms(self):
        return {
            'registration': ['enroll', 'enrollment', 'register', 'sign up', 'admission', 'apply'],
            'fee': ['payment', 'tuition', 'cost', 'price', 'pay', 'expense', 'money'],
            'library': ['book', 'reading', 'study', 'resource', 'borrow'],
            'dormitory': ['hostel', 'accommodation', 'room', 'housing', 'residence'],
            'result': ['grade', 'score', 'mark', 'outcome', 'gpa'],
            'exam': ['test', 'assessment', 'quiz', 'midterm', 'final'],
            'deadline': ['due date', 'last date', 'closing date', 'cutoff'],
            'scholarship': ['financial aid', 'grant', 'funding', 'sponsorship'],
            'medical': ['clinic', 'health', 'doctor', 'hospital'],
            'id card': ['identification', 'student id', 'card', 'badge']
        }
    
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens 
                 if t not in self.stop_words and len(t) > 2]
        return ' '.join(tokens)
    
    def expand_synonyms(self, text):
        words = text.lower().split()
        expanded = []
        for word in words:
            expanded.append(word)
            for main_word, synonyms in self.synonyms.items():
                if word in synonyms:
                    expanded.append(main_word)
                elif word == main_word:
                    expanded.extend(synonyms[:2])
        return ' '.join(expanded)
    
    def calculate_similarity(self, text1, text2):
        processed1 = self.preprocess_text(text1)
        processed2 = self.preprocess_text(text2)
        if not processed1 or not processed2:
            return 0
        try:
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([processed1, processed2])
            similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
            return similarity[0][0]
        except:
            return 0
    
    def extract_keywords(self, text):
        processed = self.preprocess_text(text)
        return processed.split()[:5]
    
    def generate_response(self, message, faq_list):
        expanded_message = self.expand_synonyms(message)
        
        # Greeting detection
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        for g in greetings:
            if g in message.lower():
                return {
                    'answer': "Hello! 👋 Welcome to Mekdela Amba University Chatbot. How can I assist you today?",
                    'confidence': 1.0,
                    'category': 'Greeting'
                }
        
        # Goodbye detection
        goodbyes = ['bye', 'goodbye', 'see you', 'exit', 'quit']
        for g in goodbyes:
            if g in message.lower():
                return {
                    'answer': "Goodbye! 👋 Have a great day! Come back if you have more questions.",
                    'confidence': 1.0,
                    'category': 'Goodbye'
                }
        
        # Thank you detection
        thanks = ['thank you', 'thanks', 'appreciate', 'thank']
        for t in thanks:
            if t in message.lower():
                return {
                    'answer': "You're welcome! 😊 Is there anything else I can help you with?",
                    'confidence': 1.0,
                    'category': 'Thanks'
                }
        
        # Help detection
        help_words = ['help', 'what can you do', 'capabilities', 'features']
        if any(w in message.lower() for w in help_words):
            return {
                'answer': """📚 **I can help you with:**

🎓 **Admissions & Registration**
- Registration dates and deadlines
- Admission requirements
- Application process

💰 **Fees & Payments**
- Tuition fees by program
- Payment methods
- Scholarship information

🏠 **Dormitory & Housing**
- Application process
- Fee structure
- Room allocation

📖 **Library & Facilities**
- Location and hours
- Book borrowing
- Medical center

📝 **Academics**
- Courses and programs
- Exam results
- Grading system

What would you like to know? Just type your question!""",
                'confidence': 1.0,
                'category': 'Help'
            }
        
        # Find best match
        best_match = None
        best_score = 0
        
        for faq in faq_list:
            question = faq['question']
            similarity = self.calculate_similarity(expanded_message, question)
            
            msg_keywords = set(self.extract_keywords(message))
            q_keywords = set(self.extract_keywords(question))
            keyword_overlap = len(msg_keywords & q_keywords) / max(len(msg_keywords), 1)
            
            total_score = similarity * 0.6 + keyword_overlap * 0.4
            
            if total_score > best_score:
                best_score = total_score
                best_match = faq
        
        if best_match and best_score > 0.3:
            return {
                'answer': best_match['answer'],
                'confidence': round(best_score * 100, 1),
                'category': best_match.get('category', 'General')
            }
        
        # Fallback responses
        fallbacks = [
            "I'm not sure about that. Could you please rephrase your question?",
            "I don't have information about that yet. Please contact the university office directly.",
            "Can you ask me something about admissions, fees, courses, library, or dormitory?",
            "Try asking about: registration dates, tuition fees, library hours, or dormitory applications."
        ]
        
        return {
            'answer': random.choice(fallbacks),
            'confidence': round(best_score * 100, 1),
            'category': 'Unknown'
        }
    
    def train_with_faqs(self, faq_data):
        self.faq_data = faq_data
        questions = [f['question'] for f in faq_data]
        processed = [self.preprocess_text(q) for q in questions]
        if processed:
            self.vectorizer = TfidfVectorizer()
            self.question_vectors = self.vectorizer.fit_transform(processed)

# Create singleton instance
nlp_engine = NLPEngine()