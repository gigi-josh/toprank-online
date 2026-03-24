import os
import sqlite3
import logging
import requests
from flask import Flask, request, jsonify, send_file, session, redirect
from flask_cors import CORS
import PyPDF2
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
PORT = int(os.getenv('PORT', 5000))
HF_API_KEY = os.getenv('HF_API_KEY')

# Handle data directory safely
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'jai_academy.db')

# ========== DATABASE FUNCTIONS ==========

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            filename TEXT,
            content TEXT NOT NULL,
            pages INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 0,
            uploaded_by TEXT
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            response TEXT,
            lesson_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student_progress (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            lessons_completed TEXT,
            current_lesson_id INTEGER,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS teaching_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT,
            suggested_response TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info(f"✅ Database ready")

# ========== CURRENT LESSON TRACKING ==========

current_lesson_id = None
current_lesson_content = ""
current_lesson_title = "No lesson uploaded"

def load_current_lesson():
    global current_lesson_id, current_lesson_content, current_lesson_title
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, title, content FROM lessons 
        WHERE is_active = 1 
        ORDER BY uploaded_at DESC LIMIT 1
    ''')
    lesson = cur.fetchone()
    
    if lesson:
        current_lesson_id = lesson['id']
        current_lesson_content = lesson['content']
        current_lesson_title = lesson['title']
        logger.info(f"📚 Active lesson: {current_lesson_title}")
    else:
        current_lesson_id = None
        current_lesson_content = ""
        current_lesson_title = "No lesson uploaded"
    conn.close()

# ========== AUTH ==========

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin/login-page')
        return f(*args, **kwargs)
    return decorated

# ========== JAI - WITH FALLBACK ==========

class JAI:
    
    @staticmethod
    def generate_response(user_message, lesson_content="", lesson_title="", user_id="anonymous"):
        
        # Save user question
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO chat_history (user_id, message, lesson_id, created_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, user_message[:500], current_lesson_id, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Database error: {e}")
        
        # Build prompt
        lesson_context = ""
        if lesson_content and lesson_title != "No lesson uploaded":
            lesson_context = f"Current lesson: {lesson_title}\n\n"
        
        prompt = f"""{lesson_context}You are JAI, a friendly cyber security teacher created by Joshua Giwa from Yukuben, Nigeria. Teach clearly. Use Nigerian examples.

Student: {user_message}

JAI:"""
        
        try:
            headers = {
                "Authorization": f"Bearer {HF_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            # CORRECT ENDPOINT
            response = requests.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-small",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    response_text = result[0].get('generated_text', '').strip()
                    if response_text:
                        return response_text
            
            # Fallback responses
            return JAI.fallback_response(user_message, lesson_title)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            return JAI.fallback_response(user_message, lesson_title)
    
    @staticmethod
    def fallback_response(message, lesson_title):
        msg = message.lower()
        
        if any(g in msg for g in ['hi', 'hello', 'hey']):
            return "👋 Hello! I'm JAI, your cyber security teacher created by Joshua Giwa from Yukuben, Nigeria. What would you like to learn today?"
        
        if 'malware' in msg:
            return "🦠 Malware is malicious software designed to harm devices. Common types: viruses, worms, ransomware. Want to learn how to protect yourself?"
        
        if 'who created' in msg:
            return "I was created by Joshua Giwa from Yukuben, Nigeria. He built me to help Nigerians learn cyber security!"
        
        if lesson_title != "No lesson uploaded":
            return f"📚 Today's lesson is: {lesson_title}. Ask me anything about it!"
        
        return "🎓 I'm JAI, your AI teacher! Ask me about malware, reverse engineering, or how to start in cyber security."

# ========== ROUTES ==========

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/admin/login-page')
def admin_login_page():
    return send_file('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return redirect('/admin')
    return '''
        <script>
            alert("Wrong password!");
            window.location.href = "/admin/login-page";
        </script>
    '''

@app.route('/admin')
@login_required
def admin_panel():
    return send_file('admin.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

@app.route('/admin/upload', methods=['POST'])
@login_required
def admin_upload():
    global current_lesson_id, current_lesson_content, current_lesson_title
    
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file'}), 400
    
    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
        title = pdf_file.filename.replace('.pdf', '')
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE lessons SET is_active = 0")
        cur.execute('''
            INSERT INTO lessons (title, filename, content, pages, is_active, uploaded_by, uploaded_at)
            VALUES (?, ?, ?, ?, 1, ?, ?)
        ''', (title, pdf_file.filename, extracted_text, len(pdf_reader.pages), 'admin', datetime.now()))
        conn.commit()
        conn.close()
        
        load_current_lesson()
        
        return jsonify({'success': True, 'message': f'✅ Lesson "{title}" uploaded!'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/lessons', methods=['GET'])
@login_required
def list_lessons():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, title, pages, uploaded_at, is_active FROM lessons ORDER BY uploaded_at DESC')
    lessons = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(lessons)

@app.route('/admin/switch/<int:lesson_id>', methods=['POST'])
@login_required
def switch_lesson(lesson_id):
    global current_lesson_id, current_lesson_content, current_lesson_title
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE lessons SET is_active = 0")
    cur.execute("UPDATE lessons SET is_active = 1 WHERE id = ?", (lesson_id,))
    conn.commit()
    conn.close()
    load_current_lesson()
    return jsonify({'success': True, 'lesson': current_lesson_title})

@app.route('/admin/stats', methods=['GET'])
@login_required
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM lessons")
    total_lessons = cur.fetchone()[0]
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM chat_history")
    total_students = cur.fetchone()[0]
    conn.close()
    return jsonify({'total_lessons': total_lessons, 'total_students': total_students, 'current_lesson': current_lesson_title})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').strip()
    user_id = data.get('userId', 'anonymous')
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    response = JAI.generate_response(message, current_lesson_content, current_lesson_title, user_id)
    return jsonify({'response': response, 'type': 'jai', 'lesson': current_lesson_title})

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'name': 'JAI',
        'creator': 'Joshua Giwa',
        'lesson_loaded': current_lesson_id is not None,
        'lesson': current_lesson_title,
        'hf_api': bool(HF_API_KEY)
    })

setup_database()
load_current_lesson()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)