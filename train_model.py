# train_model.py
import sqlite3
import nltk
import json

nltk.download('punkt')
nltk.download('stopwords')

def analyze_faq_data():
    """Analyze FAQ data and create simple patterns"""
    conn = sqlite3.connect('university_chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question, answer, category, keywords FROM faq')
    faqs = cursor.fetchall()
    conn.close()
    
    # Create keyword patterns
    patterns = {}
    for question, answer, category, keywords in faqs:
        keyword_list = keywords.split(',')
        for keyword in keyword_list:
            keyword = keyword.strip()
            if category not in patterns:
                patterns[category] = []
            patterns[category].append(keyword)
    
    # Save patterns to file
    with open('patterns.json', 'w') as f:
        json.dump(patterns, f, indent=2)
    
    print(f"Analyzed {len(faqs)} FAQs")
    print("\nCategory patterns:")
    for category, keywords in patterns.items():
        print(f"{category}: {len(keywords)} keywords")
    
    return patterns

def add_more_faqs():
    """Add more FAQs to the database"""
    conn = sqlite3.connect('university_chatbot.db')
    cursor = conn.cursor()
    
    additional_faqs = [
        ("What is the university's phone number?", "You can reach us at +251-XXX-XXXX or email info@mu.edu.et", "General", "phone,contact,call,number"),
        ("How do I check my grades?", "Grades are available on the student portal. Login with your student ID.", "Academics", "grades,gpa,results,marks"),
        ("When is the exam schedule?", "Exam schedules are posted 4 weeks before exams on the notice board and student portal.", "Academics", "exam,schedule,test,final"),
        ("How to get a transcript?", "Request transcripts at the Registrar's Office. Processing takes 3-5 business days.", "Academics", "transcript,records,documents"),
        ("Is there a medical center?", "Yes, the university clinic is near the dormitories, open 8 AM - 8 PM daily.", "Facilities", "medical,clinic,health,doctor"),
        ("How to join clubs?", "Student club registration is during the first 2 weeks of each semester at the Student Affairs office.", "General", "clubs,activities,extracurricular,societies"),
        ("What's the dress code?", "Business casual is recommended. No shorts or flip-flops in academic buildings.", "General", "dress,code,clothing,attire"),
        ("How to appeal a grade?", "Grade appeals must be submitted within 2 weeks of grade posting to the department head.", "Academics", "appeal,grade,complaint,dispute"),
    ]
    
    for faq in additional_faqs:
        cursor.execute('''
            INSERT OR IGNORE INTO faq (question, answer, category, keywords)
            VALUES (?, ?, ?, ?)
        ''', faq)
    
    conn.commit()
    conn.close()
    print(f"Added {len(additional_faqs)} new FAQs!")

if __name__ == "__main__":
    add_more_faqs()
    analyze_faq_data()
    print("\n✅ Training completed successfully!")