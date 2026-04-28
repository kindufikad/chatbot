# database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="university_faq.db"):
        self.db_name = db_name
        self.create_tables()
        self.insert_sample_data()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # FAQ Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT,
                keywords TEXT,
                times_asked INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database tables created successfully")
    
    def insert_sample_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM faq")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_faqs = [
                # Admissions
                ("When does registration start?", "Registration starts on September 1, 2024 for first semester and February 1, 2025 for second semester.", "Registration", "registration,start,date,begin,semester"),
                ("What is the registration deadline?", "Regular registration deadline is October 15, 2024. Late registration until October 22 with 500 ETB late fee.", "Registration", "deadline,last date,registration,end"),
                ("What is the minimum GPA for admission?", "The minimum GPA for undergraduate admission is 2.0. Competitive programs require 2.5.", "Admissions", "gpa,minimum,requirement,admission"),
                ("What documents are needed for admission?", "Required documents: Application form, transcripts, EUEE score card, birth certificate, 4 photos, 2 recommendation letters, personal statement.", "Admissions", "documents,required,application"),
                ("Where is the admissions office?", "The admissions office is located in the main administration building, on the second floor.", "Admissions", "admissions,office,location,where"),
                ("Where is the registration building?", "The registration building is located in the main administration building, on the second floor.", "Registration", "registration,building,location,where"),
                
                # Fees
                ("How can I pay my fees?", "You can pay through: 1) University portal, 2) Bank transfer to CBE account, 3) In-person at finance office, 4) CBE Birr or Amole.", "Fees", "payment,fees,tuition,pay"),
                ("How much is tuition  Computer Science?", "Computer Science tuition is 15,000 ETB per year for regular students.", "Fees", "tuition,computer science,fee,cost"),
                ("How much is tuition for Engineering?", "Engineering tuition is 16,000 ETB per year for regular students.", "Fees", "tuition,engineering,fee,cost"),
                ("What is the late payment penalty?", "Late payment penalty is 100 ETB per week, up to 1000 ETB maximum.", "Fees", "late,penalty,payment"),
                ("How to apply for scholarship?", "Submit scholarship application to registrar's office by January 30. Merit-based and need-based available.", "Fees", "scholarship,financial aid,grant"),
                 ("How much is tuition for information technology?", "Information Technology tuition is 15,000 ETB per year for regular students.", "Fees", "tuition,information technology,fee,cost"),
                    ("How much is tuition for business?", "Business tuition is 14,000 ETB per year for regular students.", "Fees", "tuition,business,fee,cost"),
                    ("How much is tuition for accounting?", "Accounting tuition is 14,000 ETB per year for regular students.", "Fees", "tuition,accounting,fee,cost"),
                    ("How much is tuition for natural sciences?", "Natural Sciences tuition is 13,000 ETB per year for regular students.", "Fees", "tuition,natural sciences,fee,cost"),
                     ("How much is tuition for social sciences?", "Social Sciences tuitionis 12,000 ETB per year for regular students.", "Fees", "tuition,social sciences,fee,cost"),
                   ("How much is tuition for distance learning?", "Distance learning tuition is 10,000 ETB per year for regular students.", "Fees", "tuition,distance learning,fee,cost"),
                    ("How much is tuition for postgraduate programs?", "Postgraduate tuition is 20,000 ETB per year for regular students.", "Fees", "tuition,postgraduate,fee,cost"),
                    ("How much is tuition for first-year students?", "First-year tuition is 12,000 ETB per year for regular students.", "Fees", "tuition,first-year,fee,cost"),
                    ("How much is tuition for distance learning?", "Distance learning tuition is 10,000 ETB per year for regular students.", "Fees", "tuition,distance learning,fee,cost"),
                    ("How much is tuition for regular students?", "Regular student tuition is 15,000 ETB per year for Computer Science, 16,000 ETB for Engineering, 14,000 ETB for Business and Accounting, 13,000 ETB for Natural Sciences, and 12,000 ETB for Social Sciences.", "Fees", "tuition,regular students,fee,cost"),
                    ("How much is tuition for postgraduate students?", "Postgraduate tuition is 20,000 ETB per year for regular students.", "Fees", "tuition,postgraduate,fee,cost"),
                 ("How much is tuition for first-year students?", "First-year tuition is 12,000 ETB per year for regular students.", "Fees", "tuition,first-year,fee,cost"),
             
                            
                
                # Facilities
                ("Where is the library?", "The library is located near the student cafeteria, next to the Administration Building.", "Facilities", "library,location,books,study"),
                ("What are library hours?", "Monday-saturday: 8 AM- 6 PM, Sunday: 2 AM-6 am. Exam weeks: 24/7.", "Facilities", "library,hours,open,closed"),
                ("Is there a medical center?", "Yes, medical center is  the commercial area, open 24/7 for emergencies.", "Facilities", "medical,clinic,health,hospital"),
                 ("Where is the student cafeteria?", "The student cafeteria is located in the central campus area, near the library.", "Facilities", "cafeteria,food,dining,location"),
                 ("What are cafeteria hours?", "Monday-Friday: 7 AM-7 PM, Saturday-Sunday: 8 AM-5 PM.", "Facilities", "cafeteria,hours,open,closed"),
                ("Is there a gym?", "Yes, the gym is located near biology laboratory, open from 6 AM to 10 PM daily.", "Facilities", "gym,fitness,exercise,sports"),
                 ("Where is the sports field?", "The sports field is located on the west side of campus, next to the the women's dormitory.", "Facilities", "sports field,location,athletics"),
                 ("Where is the computer lab?", "The computer lab is located in the seminar building, first floor.", "Facilities", "computer lab,location,computers"),
                ("Where is the bookstore?", "The bookstore is located in the commercial area, next to the medical center.", "Facilities", "bookstore,location,textbooks,supplies"),
                 ("Where is the student center?", "The student center is located in the central campus area, near the library.", "Facilities", "student center,location,activities,events"),
                 ("Where is the parking lot?", "The parking lot is located on the north side of campus, near the engineering building.", "Facilities", "parking lot,location,parking"),
                ("Where is the science lab?", "The science lab is located in the natural sciences building, second floor.", "Facilities", "science lab,location,laboratory"),
                 ("Where is the engineering workshop?", "The engineering workshop is located in the engineering building, first floor.", "Facilities", "engineering workshop,location,workshop"),

                ("Where is the art studio?", "The art studio is located in the social sciences building, third floor.", "Facilities", "art studio,location,studio"),

                                  
                     
                  
                
                # Dormitory
                ("How to apply for dormitory?", "Apply online through student portal during registration. Priority to first-year and distance students.", "Dormitory", "dormitory,hostel,accommodation,room,apply"),
                ("What are dormitory fees?", "Shared room (4-person): 8,000 ETB/semester, Shared (2-person): 12,000 ETB, Single: 18,000 ETB.", "Dormitory", "dorm,fee,cost,price"),                  
                ("What is the dormitory address?", "Dormitory is located under student building , near the sports field.", "Dormitory", "dormitory,address,location,where"),
                     
                ("What are dormitory rules?", "No smoking, no alcohol, no noise,  quiet hours 10 PM-6 AM, guests allowed only with permission.", "Dormitory", "dormitory,rules,regulations"),
                ("How to contact dormitory office?", "under student building, Phone: 0961806188", "Dormitory", "contact,dormitory,phone,email"),
                ("What is the dormitory check-in time?", "Check-in time is from 8 AM to 8 PM on move-in day. Early check-in available with prior approval.", "Dormitory", "dormitory,check-in,time"),
                ("What is the dormitory check-out time?", "Check-out time is by 12 PM on move-out day. Late check-out available with prior approval.", "Dormitory", "dormitory,check-out,time"),
                ("What is the dormitory curfew?", "Curfew is from 10 PM to 6 AM. Students must be in dormitory during curfew hours.", "Dormitory", "dormitory,curfew,time"),
                ("What is the dormitory guest policy?", "Guests allowed only with prior permission from dormitory office. Overnight guests not allowed.", "Dormitory", "dormitory,guest,policy"),
                ("What is the dormitory laundry policy?", "Laundry facilities available in dormitory. Free for residents. Open 24/7.", "Dormitory", "dormitory,laundry,policy"),    
                   

                      
                 




                # Academics
                ("What courses are offered?", "We offer Computer Science, Engineering, Business, Accounting, Natural Sciences, and Social Sciences etc.....", "Academics", "courses,programs,departments"),
                ("How to check exam results?", "Check results through student portal using your ID and password.", "Academics", "result,grades,exam,score"),
                ("What is the grading scale?", "A(85-100)=4.0, B(70-79)=3.0, C(50-59)=2.0, D(45-49)=1.0, F(below 35)=0.0", "Academics", "grading,gpa,scale"),
                ("What is academic probation?", "Probation when GPA below 2.0. Two semesters to improve or suspension.", "Academics", "probation,gpa,suspension"),
                ("What is the academic calendar?", "First semester: Sep-Jan, Second semester: Feb-July. Summer break: August.", "Academics", "calendar,semester,dates"),
                ("How to register for classes?", "Register through registration office during registration period. Select courses and submit.", "Academics", "register,classes,courses,registration"),
               ("What is the credit hour system?", "Each course has credit hours. Full-time students must take at least 12 credit hours per semester.", "Academics", "credit hours,full-time,part-time"),
               ("What is the course withdrawal policy?", "Withdraw by week 8 without penalty. After week 8, withdrawal requires approval and may incur fees.", "Academics", "course withdrawal,drop course,policy"),
               ("What is the academic advising process?", "Academic advising available through student services. Schedule appointment for guidance on course selection and career planning.", "Academics", "advising,academic advisor,appointment"),
               ("What is the graduation requirement?", "To graduate, students must complete required credit hours, maintain minimum GPA, and submit graduation application in final semester.", "Academics", "graduation,requirements,credit hours,gpa"),
               ("What is the thesis requirement for postgraduate students?", "Postgraduate students must complete a thesis project under faculty supervision, including proposal, research, and defense.", "Academics", "thesis,postgraduate,requirement"),
               ("What is the internship requirement?", "Some programs require an internship for graduation. Check with your department for specific requirements.", "Academics", "internship,requirement,graduation"),
               ("What is the policy on academic integrity?", "Academic integrity is expected. Violations include plagiarism, cheating, and fabrication. Penalties range from warning to expulsion.", "Academics", "academic integrity,plagiarism,cheating,policy"),
               ("What is the policy on course attendance?", "Attendance is expected for all courses. Some instructors may have specific attendance policies. Check with your instructor.", "Academics", "attendance,policy,course"),
               ("What is the policy on course retakes?", "Students may retake a course if they receive a failing grade. Retake policies vary by department. Check with your academic advisor.", "Academics", "course retake,policy,retake"),
               ("What is the policy on academic appeals?", "Students may appeal academic decisions through the academic appeals process. Submit appeal form to registrar's office with supporting documentation.", "Academics", "academic appeals,policy,appeal"),
               ("What is the policy on academic leave?", "Students may request academic leave for personal, medical, or other reasons. Submit leave request form to registrar's office with supporting documentation.", "Academics", "academic leave,policy,leave"),
               ("What is the policy on academic dismissal?", "Students may be dismissed for academic reasons if they fail to meet minimum GPA requirements after probation period. Dismissal decisions can be appealed.", "Academics", "academic dismissal,policy,dismissal"),
               ("What is the policy on academic honors?", "Students with high academic achievement may be eligible for honors such as Dean's List or graduation with honors. Check with your department for specific criteria.", "Academics", "academic honors,policy,honors"),
                
                                # Student Services
                ("How to get student ID card?", "ID cards issued at registrar's office after registration. Fee: 100 ETB.", "Services", "id card,student id,identification"),
                ("How to contact registrar?", "Email: registrar@mekdela.edu.et, Phone: 033-123-4567", "Services", "contact,registrar,phone,email"),
                ("How to withdraw from a course?", "Course withdrawal deadline is week 8. Submit form to registrar's office.", "Registration", "withdrawal,drop course"),
                ("How to apply for leave of absence?", "Submit leave of absence form to registrar's office with supporting documentation.", "Services", "leave of absence,academic leave,policy"),
                ("How to request transcript?", "Request transcripts through student portal. Fee: 200 ETB for regular processing, 500 ETB for expedited.", "Services", "transcript,request,fee"),
                ("How to access counseling services?", "Counseling services available through student services. Schedule appointment for support with personal, academic, or career issues.", "Services", "counseling,services,appointment"),
                ("How to access career services?", "Career services available through student services. Schedule appointment for resume review, job search assistance, and career counseling.", "Services", "career services,appointment,resume,job search"),
                ("How to access disability services?", "Disability services available through student services. Contact office for accommodations and support.", "Services", "disability services,accommodations,support"),
                ("How to access financial aid?", "Financial aid available through registrar's office. Submit application with required documentation by January 30.", "Services", "financial aid,scholarship,application"),
                ("How to access tutoring services?", "Tutoring services available through student services. Schedule appointment for academic support in various subjects.", "Services", "tutoring,services,appointment,academic support"),
                ("How to access library resources?", "Library resources available to all students. Access online databases and physical materials during library hours.", "Services", "library resources,access,databases,materials"),
                ("How to access health services?", "Health services available at medical center. Open 24/7 for emergencies and regular hours for non-emergency care.", "Services", "health services,medical center,access"),
                ("How to access IT support?", "IT support available through computer lab. Contact lab staff for assistance with technical issues.", "Services", "IT support,computer lab,technical assistance")
            
            ]
            
            cursor.executemany('''
                INSERT INTO faq (question, answer, category, keywords)
                VALUES (?, ?, ?, ?)
            ''', sample_faqs)
            
            conn.commit()
            print(f"✅ Database initialized with {len(sample_faqs)} FAQs")
        else:
            print(f"✅ Database already has {count} FAQs")
        
        conn.close()
    
    def get_all_faqs(self):
        """Get all FAQs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, question, answer, category FROM faq ORDER BY times_asked DESC')
        results = cursor.fetchall()
        conn.close()
        return [{'id': r[0], 'question': r[1], 'answer': r[2], 'category': r[3]} for r in results]
    
    def search_faq(self, question):
        """Search for answer to user question"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Try exact match first
        cursor.execute('''
            SELECT question, answer, category FROM faq 
            WHERE LOWER(question) = LOWER(?)
        ''', (question,))
        result = cursor.fetchone()
        
        if result:
            conn.close()
            return {'question': result[0], 'answer': result[1], 'category': result[2], 'confidence': 1.0}
        
        # Keyword search
        words = question.lower().split()
        best_match = None
        best_score = 0
        
        for word in words:
            if len(word) > 2:
                cursor.execute('''
                    SELECT question, answer, category, keywords FROM faq 
                    WHERE LOWER(question) LIKE ? OR LOWER(keywords) LIKE ?
                    ORDER BY times_asked DESC
                    LIMIT 3
                ''', (f'%{word}%', f'%{word}%'))
                
                results = cursor.fetchall()
                for row in results:
                    score = 0
                    if word in row[0].lower():
                        score += 3
                    if row[3] and word in row[3].lower():
                        score += 2
                    if score > best_score:
                        best_score = score
                        best_match = row
        
        conn.close()
        
        if best_match and best_score > 0:
            # Update times asked
            self.update_times_asked(best_match[0])
            return {
                'question': best_match[0],
                'answer': best_match[1],
                'category': best_match[2],
                'confidence': min(0.95, 0.5 + (best_score / 10))
            }
        return None
    
    def update_times_asked(self, question):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE faq SET times_asked = times_asked + 1 WHERE question = ?', (question,))
        conn.commit()
        conn.close()
    
    def save_chat(self, session_id, user_message, bot_response, confidence):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chat_history (session_id, user_message, bot_response, confidence)
            VALUES (?, ?, ?, ?)
        ''', (session_id, user_message, bot_response, confidence))
        conn.commit()
        conn.close()

# Create database instance
db = Database()