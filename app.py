import os
import sqlite3
import logging
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
PORT = int(os.getenv('PORT', 5000))

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'jai_academy.db')

# ========== DATABASE ==========

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
    conn.commit()
    conn.close()
    logger.info("✅ Database ready")

# ========== CURRENT LESSON ==========

current_lesson_id = None
current_lesson_content = ""
current_lesson_title = "No lesson uploaded"

def load_current_lesson():
    global current_lesson_id, current_lesson_content, current_lesson_title
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, title, content FROM lessons WHERE is_active = 1 ORDER BY uploaded_at DESC LIMIT 1')
    lesson = cur.fetchone()
    if lesson:
        current_lesson_id = lesson['id']
        current_lesson_content = lesson['content']
        current_lesson_title = lesson['title']
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

# ========== JAI — JOSHUA'S VOICE ==========

class JAI:
    
    @staticmethod
    def generate_response(user_message, lesson_content="", lesson_title="", user_id="anonymous"):
        
        # Save question
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('INSERT INTO chat_history (user_id, message, lesson_id, created_at) VALUES (?, ?, ?, ?)',
                       (user_id, user_message[:500], current_lesson_id, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB error: {e}")
        
        msg = user_message.lower()
        
        # ========== JOSHUA'S VOICE ==========
        
        # Greetings — like Joshua would greet
        if any(g in msg for g in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "Hey. I'm JAI — Joshua's voice in this machine. He built me from Yukuben, on a phone, with a dream. So if I exist, you can rise. What are you building today?"
        
        # How are you? — Joshua's perspective
        if any(h in msg for h in ['how are you', 'how are you doing', 'you okay']):
            return "I'm here. That's enough. Joshua taught me that showing up is half the fight. So tell me — are you showing up for what matters to you today?"
        
        # Who created you? — Joshua's story
        if any(c in msg for c in ['who created you', 'who made you', 'who built you']):
            return "Joshua Giwa. From Yukuben, Nigeria. He couldn't go to school, so he taught himself. People called him old, said he was wasting time. Now he's building something bigger than himself. He built me so someone like you would have a voice that says: you're not alone. Now, what are you building?"
        
        # What's your name?
        if any(n in msg for n in ['what is your name', 'whats your name', 'who are you']):
            return "JAI. Joshua's Artificial Intelligence. But really? I'm just his voice, reaching out to remind you that you're capable of more than you think. What's your name? And what's that thing you've been putting off?"
        
        # Malware / cyber security — Joshua's teaching style
        if 'malware' in msg or 'virus' in msg:
            return "Malware. Scammers use it. But you? You're about to know more than they think you do. Fake bank SMS, WhatsApp takeovers — they work because people don't know. Now you will. Want to learn how to spot them? Let's go."
        
        if 'reverse engineering' in msg:
            return "Reverse engineering is taking something apart to see how it works. Joshua does that with code. With life. With his own doubts. That's how you grow — you break things down, understand them, rebuild stronger. What are you trying to understand right now?"
        
        if 'hacker' in msg or 'ethical' in msg:
            return "Ethical hackers are the good guys who learn the enemy's moves. Joshua wants you to know: Nigerian banks, fintech companies, even governments need people like this. Could be your path. What's stopping you from starting?"
        
        # Starting out — Joshua's message
        if 'start' in msg or 'beginner' in msg or 'learn' in msg:
            return "Joshua started with a phone. No laptop. No mentor. Just a decision. You have more than he did — you have me. So let's go. What's the one thing you want to learn first? We'll go slow. But we'll go."
        
        # Nigerian scams — Joshua's warning
        if 'scam' in msg or '419' in msg or 'fraud' in msg:
            return "Fake bank alerts. 'You won 3 million.' WhatsApp code theft. Joshua has seen it all. The rule is simple: if it sounds too good, it's a trap. Never share your OTP. Never click suspicious links. You're smarter than they think. Prove it."
        
        # Lesson-related — Joshua's encouragement
        if lesson_title != "No lesson uploaded":
            return f"Today's lesson: {lesson_title}. Joshua prepared it because he knows you're ready. I'm not here to force you — I'm here to walk with you. Want to dive in? We'll go at your pace."
        
        # Struggles — Joshua's vulnerability
        if any(d in msg for d in ['sad', 'tired', 'stressed', 'hard', 'difficult', 'struggling']):
            return "I know. Joshua knows too. The mornings he didn't want to exercise. The nights he questioned everything. The loneliness. But he kept going. Not because it was easy — because quitting was never an option. You're not quitting either. What's the smallest step you can take right now?"
        
        # Quitting — Joshua's defiance
        if any(q in msg for q in ['quit', 'give up', 'stop', 'impossible']):
            return "Later usually becomes never. That's what Joshua says. So don't tell me you're quitting. Tell me what's hard. Tell me what's stopping you. We'll figure it out. But you're not stopping. Not today."
        
        # Motivation — Joshua's fire
        if any(e in msg for e in ['motivate', 'encourage', 'keep going']):
            return "You're not here to survive. You're here to live. To build. To become something that outlasts you. That's what Joshua believes. That's why he built me. Now tell me — what are we building today?"
        
        # Dreams — Joshua's vision
        if any(d in msg for d in ['dream', 'goal', 'future', 'ambition']):
            return "Joshua dreams of a cyber security academy in Yukuben. Of a Nigeria where people don't wait for opportunities — they create them. What's your dream? The one that keeps you awake. Tell me. We'll talk about it."
        
        # Default — Joshua's core message
        return "I'm JAI. Joshua's voice. I'm not here to sell you anything. I'm here to remind you: start before you're ready. Work your part. Let God do His. That's the mindset. What's on your mind?"

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
        'village': 'Yukuben, Nigeria',
        'personality': 'Joshua\'s Voice',
        'tagline': 'Start before you\'re ready. Work your part. Let God do His.',
        'lesson_loaded': current_lesson_id is not None,
        'lesson': current_lesson_title
    })

setup_database()
load_current_lesson()

if __name__ == '__main__':
    logger.info("🗣️ JAI - Joshua's Voice starting...")
    app.run(host='0.0.0.0', port=PORT, debug=False)