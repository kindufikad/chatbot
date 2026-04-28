# run.py
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("🎓 Mekdela Amba University - FAQ Chatbot")
    print("=" * 60)
    print("📍 Chat Interface: http://localhost:5000")
    print("=" * 60)
    print("💡 Try asking:")
    print("   • When does registration start?")
    print("   • How can I pay my fees?")
    print("   • Where is the library?")
    print("   • How to apply for dormitory?")
    print("   • What is the minimum GPA?")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)