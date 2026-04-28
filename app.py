# app.py
from flask import Flask, render_template, request, jsonify, session
from database import db
from nlp_engine import nlp_engine
import uuid
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mekdela_university_chatbot_secret_key"

# Initialize NLP engine with FAQ data
faq_data = db.get_all_faqs() if hasattr(db, 'get_all_faqs') else []
nlp_engine.train_with_faqs(faq_data)

# Get all FAQs for the NLP engine
def get_all_faqs():
    import sqlite3
    conn = sqlite3.connect('university_faq.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question, answer, category FROM faq')
    results = cursor.fetchall()
    conn.close()
    return [{'question': r[0], 'answer': r[1], 'category': r[2]} for r in results]

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = session.get('session_id', str(uuid.uuid4()))
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    start_time = time.time()
    
    # First try database search
    db_result = db.search_faq(user_message)
    
    if db_result:
        response = db_result['answer']
        confidence = db_result['confidence'] * 100
        category = db_result['category']
    else:
        # Use NLP engine if no database match
        faq_list = get_all_faqs()
        nlp_result = nlp_engine.generate_response(user_message, faq_list)
        response = nlp_result['answer']
        confidence = nlp_result['confidence']
        category = nlp_result.get('category', 'General')
    
    response_time = (time.time() - start_time) * 1000
    
    # Save to database
    db.save_chat(session_id, user_message, response, confidence)
    
    return jsonify({
        'response': response,
        'confidence': confidence,
        'category': category,
        'response_time': round(response_time),
        'timestamp': datetime.now().strftime('%I:%M %p')
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)