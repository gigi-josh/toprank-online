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
HF_MODEL = os.getenv('HF_MODEL', 'microsoft/DialoGPT-small')

# Handle data directory safely (works on free tier)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'jai_academy.db')

# ========== DATABASE FUNCTIONS ==========

def get_db():
    """Get SQLite connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Create all tables if they don't exist"""
    conn = get_db()
    cur = conn.cursor()
    
    # Lessons table
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
    
    # Chat history
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
    
    # Student progress
    cur.execute('''
        CREATE TABLE IF NOT EXISTS student_progress (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            lessons_completed TEXT,
            current_lesson_id INTEGER,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Teaching suggestions
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
    logger.info(f"✅ Database ready at {DB_PATH}")

# ========== CURRENT LESSON TRACKING ==========

current_lesson_id = None
current_lesson_content = ""
current_lesson_title = "No lesson uploaded"

def load_current_lesson():
    """Load the active lesson from database"""
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

# ========== AUTH DECORATORS ==========

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin/login-page')
        return f(*args, **kwargs)
    return decorated

# ========== JAI - JOSHUA'S ARTIFICIAL INTELLIGENCE ==========

class JAI:
    """Joshua's Artificial Intelligence — Cyber Security Teacher"""
    
    @staticmethod
    def generate_response(user_message, lesson_content="", lesson_title="", user_id="anonymous"):
        """Generate response using DialoGPT"""
        
        if not HF_API_KEY:
            return "⚠️ JAI needs an API key. Please ask Joshua to configure HF_API_KEY."
        
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
            logger.info(f"📝 Saved question from {user_id}")
        except Exception as e:
            logger.error(f"Database error: {e}")
        
        # Build context from lesson if available
        context = ""
        if lesson_content and lesson_title != "No lesson uploaded":
            context = f"Current lesson: {lesson_title}\n\n"
        
        # Simple conversation prompt for DialoGPT
        prompt = f"{context}Student: {user_message}\nJAI:"
        
        try:
            headers = {
                "Authorization": f"Bearer {HF_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.8,
                    "do_sample": True,
                    "top_p": 0.9
                }
            }
            
            logger.info(f"🤖 Calling DialoGPT")
            
            response = requests.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            logger.info(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated = result[0].get('generated_text', '')
                    # Extract JAI's response
                    if "JAI:" in generated:
                        response_text = generated.split("JAI:")[-1].strip()
                    else:
                        response_text = generated.strip()
                    
                    if response_text:
                        # Save response
                        try:
                            conn = get_db()
                            cur = conn.cursor()
                            cur.execute('''
                                UPDATE chat_history 
                                SET response = ? 
                                WHERE id = (
                                    SELECT id FROM chat_history 
                                    WHERE user_id = ? 
                                    ORDER BY created_at DESC LIMIT 1
                                )
                            ''', (response_text[:1000], user_id))
                            conn.commit()
                            conn.close()
                        except Exception as e:
                            logger.error(f"Save error: {e}")
                        
                        return response_text
            
            if response.status_code == 503:
                return "🔄 JAI is waking up! The first response takes 30-60 seconds. Please try again in a moment."
            else:
                logger.error(f"API Error: {response.status_code} - {response.text[:200]}")
                return f"⏳ JAI is loading. Please wait 30 seconds and try again."
                
        except requests.exceptions.Timeout:
            return "🌐 JAI is thinking. Please try again in a moment."
        except Exception as e:
            logger.error(f"JAI error: {e}")
            return f"💡 JAI needs a moment. Please refresh and try again."

# ========== ROUTES ==========

@app.route('/')
def index():
    """Student chat page"""
    return send_file('index.html')

@app.route('/admin/login-page')
def admin_login_page():
    """Admin login page"""
    return send_file('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Handle admin login"""
    password = request.form.get('password')
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        logger.info("Admin logged in")
        return redirect('/admin')
    logger.warning("Failed admin login")
    return '''
        <script>
            alert("Wrong password!");
            window.location.href = "/admin/login-page";
        </script>
    '''

@app.route('/admin')
@login_required
def admin_panel():
    """Admin dashboard"""
    return send_file('admin.html')

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_logged_in', None)
    return redirect('/')

@app.route('/admin/upload', methods=['POST'])
@login_required
def admin_upload():
    """Upload a new lesson PDF"""
    global current_lesson_id, current_lesson_content, current_lesson_title
    
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file'}), 400
    
    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({'error': 'File must be PDF'}), 400
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text:
                extracted_text += f"\n--- Page {page_num + 1} ---\n"
                extracted_text += text
        
        if not extracted_text.strip():
            return jsonify({'error': 'No text could be extracted'}), 400
        
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
        logger.info(f"📚 Lesson uploaded: {title}")
        
        return jsonify({
            'success': True,
            'message': f'✅ Lesson "{title}" uploaded!',
            'pages': len(pdf_reader.pages),
            'characters': len(extracted_text)
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin/lessons', methods=['GET'])
@login_required
def list_lessons():
    """List all uploaded lessons"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT id, title, pages, uploaded_at, is_active 
        FROM lessons 
        ORDER BY uploaded_at DESC
    ''')
    lessons = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(lessons)

@app.route('/admin/switch/<int:lesson_id>', methods=['POST'])
@login_required
def switch_lesson(lesson_id):
    """Switch active lesson"""
    global current_lesson_id, current_lesson_content, current_lesson_title
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE lessons SET is_active = 0")
    cur.execute("UPDATE lessons SET is_active = 1 WHERE id = ?", (lesson_id,))
    conn.commit()
    conn.close()
    
    load_current_lesson()
    
    return jsonify({'success': True, 'lesson': current_lesson_title})

@app.route('/admin/backup', methods=['GET'])
@login_required
def backup_database():
    """Download database backup"""
    import shutil
    backup_name = f"jai_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    backup_path = os.path.join(DATA_DIR, backup_name)
    shutil.copy2(DB_PATH, backup_path)
    return send_file(backup_path, as_attachment=True, download_name=backup_name)

@app.route('/admin/stats', methods=['GET'])
@login_required
def get_stats():
    """Get JAI Academy statistics"""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM lessons")
    total_lessons = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM chat_history")
    total_students = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM chat_history")
    total_questions = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM teaching_suggestions WHERE status = 'pending'")
    pending_suggestions = cur.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_lessons': total_lessons,
        'total_students': total_students,
        'total_questions': total_questions,
        'pending_suggestions': pending_suggestions,
        'current_lesson': current_lesson_title,
        'db_size': os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat with JAI"""
    data = request.json
    message = data.get('message', '').strip()
    user_id = data.get('userId', 'anonymous')
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    logger.info(f"💬 Chat from {user_id}: {message[:100]}...")
    
    response = JAI.generate_response(
        message,
        current_lesson_content,
        current_lesson_title,
        user_id
    )
    
    return jsonify({
        'response': response,
        'type': 'jai',
        'lesson': current_lesson_title
    })

@app.route('/teach', methods=['POST'])
def teach():
    """Submit teaching suggestion"""
    data = request.json
    message = data.get('message', '').strip()
    suggested_response = data.get('response', '').strip()
    user_id = data.get('userId', 'anonymous')
    
    if not message or not suggested_response:
        return jsonify({'error': 'Message and response required'}), 400
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO teaching_suggestions (user_id, message, suggested_response, created_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, message[:500], suggested_response[:500], datetime.now()))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Thank you! JAI will learn from your suggestion.'})

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'name': 'JAI - Joshua\'s Artificial Intelligence',
        'creator': 'Joshua Giwa',
        'village': 'Yukuben, Nigeria',
        'database': os.path.exists(DB_PATH),
        'lesson_loaded': current_lesson_id is not None,
        'lesson': current_lesson_title,
        'hf_api': bool(HF_API_KEY),
        'hf_model': HF_MODEL
    })

@app.route('/about')
def about():
    """About JAI"""
    return jsonify({
        'name': 'JAI (Joshua\'s Artificial Intelligence)',
        'creator': 'Joshua Giwa',
        'origin': 'Yukuben, Nigeria',
        'mission': 'To teach cyber security and help build a safer digital Nigeria'
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# ========== INITIALIZATION ==========

setup_database()
load_current_lesson()

if __name__ == '__main__':
    logger.info("🤖 JAI - Joshua's Artificial Intelligence starting...")
    logger.info(f"📍 Creator: Joshua Giwa from Yukuben, Nigeria")
    logger.info(f"📚 Current lesson: {current_lesson_title}")
    logger.info(f"🔑 HF_API_KEY configured: {bool(HF_API_KEY)}")
    logger.info(f"🤖 HF_MODEL: {HF_MODEL}")
    logger.info(f"🚀 Server running on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)