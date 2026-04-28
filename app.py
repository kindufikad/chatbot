# app.py
import os
from flask import Flask, render_template, request, jsonify, session
from database import db
from nlp_engine import nlp_engine
import uuid
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mekdela_university_chatbot_secret_key')

# Initialize NLP engine with FAQ data
print("🔄 Initializing NLP engine...")
try:
    faq_data = db.get_all_faqs()
    nlp_engine.train_with_faqs(faq_data)
    print(f"✅ NLP engine trained with {len(faq_data)} FAQs")
except Exception as e:
    print(f"⚠️ Error training NLP: {e}")
    faq_data = []

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['chat_count'] = 0
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = session.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        session['chat_count'] = session.get('chat_count', 0) + 1
        
        start_time = time.time()
        
        # Try database search first
        db_result = db.search_faq(user_message)
        
        if db_result:
            response = db_result['answer']
            confidence = db_result['confidence'] * 100
            category = db_result['category']
        else:
            # Use NLP engine
            faq_list = db.get_all_faqs()
            nlp_result = nlp_engine.generate_response(user_message, faq_list)
            response = nlp_result['answer']
            confidence = nlp_result['confidence']
            category = nlp_result.get('category', 'General')
        
        response_time = (time.time() - start_time) * 1000
        
        # Save chat history
        try:
            db.save_chat(session_id, user_message, response, confidence)
        except:
            pass
        
        return jsonify({
            'response': response,
            'confidence': round(confidence, 1),
            'category': category,
            'response_time': round(response_time, 1),
            'timestamp': datetime.now().strftime('%I:%M %p')
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'response': "I'm sorry, an error occurred. Please try again.",
            'confidence': 0,
            'category': 'Error',
            'timestamp': datetime.now().strftime('%I:%M %p')
        })

@app.route('/get-faqs-count')
def get_faqs_count():
    try:
        faqs = db.get_all_faqs()
        return jsonify({'count': len(faqs)})
    except:
        return jsonify({'count': 0})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)