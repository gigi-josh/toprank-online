import os
import sqlite3
import logging
import base64
import io
from flask import Flask, request, jsonify, send_file, session, redirect
from flask_cors import CORS
import PyPDF2
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime
from gtts import gTTS

# Import JAI's personality
from jai_responses import JAIPersonality

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
    
    # Bot taught responses (Q&A)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            response TEXT NOT NULL,
            approved INTEGER DEFAULT 1,
            times_used INTEGER DEFAULT 0,
            teaching_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP
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

# ========== TEXT-TO-SPEECH ==========

@app.route('/speak', methods=['POST'])
def speak():
    """Convert text to speech and return audio"""
    data = request.json
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Text required'}), 400
    
    try:
        # Create speech using gTTS
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to memory buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64 for frontend
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'audio': audio_base64,
            'text': text[:500]
        })
        
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return jsonify({'error': str(e)}), 500

# ========== JAI HANDLER WITH DATABASE LEARNING ==========

class JAI:
    @staticmethod
    def get_taught_response(message):
        """Check if this question has been taught before"""
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                SELECT response, times_used FROM bot 
                WHERE text LIKE ? AND approved = 1 
                ORDER BY times_used ASC LIMIT 1
            ''', (f'%{message}%',))
            result = cur.fetchone()
            
            if result:
                # Update usage count
                cur.execute('''
                    UPDATE bot SET times_used = times_used + 1, last_used = NOW() 
                    WHERE text LIKE ?
                ''', (f'%{message}%',))
                conn.commit()
                conn.close()
                return result['response']
            conn.close()
        except Exception as e:
            logger.error(f"DB error in get_taught_response: {e}")
        return None
    
    @staticmethod
    def save_teaching_suggestion(user_id, message, response):
        """Save a teaching suggestion for admin review"""
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO teaching_suggestions (user_id, message, suggested_response, created_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, message[:500], response[:500], datetime.now()))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"DB error saving suggestion: {e}")
            return False
    
    @staticmethod
    def generate_response(user_message, lesson_content="", lesson_title="", user_id="anonymous"):
        # Save question to chat history
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('INSERT INTO chat_history (user_id, message, lesson_id, created_at) VALUES (?, ?, ?, ?)',
                       (user_id, user_message[:500], current_lesson_id, datetime.now()))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB error: {e}")
        
        # FIRST: Check if this question has been taught before
        taught_response = JAI.get_taught_response(user_message)
        if taught_response:
            logger.info(f"📚 Used taught response for: {user_message[:50]}")
            return taught_response
        
        # SECOND: Get response from personality file
        response = JAIPersonality.get_response(user_message, lesson_content, lesson_title)
        
        # Save response to chat history
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
            ''', (response[:1000], user_id))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"DB error: {e}")
        
        return response

# ========== LEARNING SYSTEM ROUTES ==========

@app.route('/admin/learn-page')
@login_required
def admin_learn_page():
    return send_file('admin_learn.html')

@app.route('/admin/learn', methods=['GET'])
@login_required
def learning_dashboard():
    """Dashboard to review and approve learning suggestions"""
    conn = get_db()
    cur = conn.cursor()
    
    # Get pending suggestions
    cur.execute("""
        SELECT id, user_id, message, suggested_response, created_at 
        FROM teaching_suggestions 
        WHERE status = 'pending' 
        ORDER BY created_at DESC
    """)
    pending = [dict(row) for row in cur.fetchall()]
    
    # Get approved Q&A count
    cur.execute("SELECT COUNT(*) FROM bot WHERE approved = 1")
    total_taught = cur.fetchone()[0]
    
    # Get learning stats
    cur.execute("SELECT COUNT(*) FROM chat_history")
    total_conversations = cur.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'pending': pending,
        'total_taught': total_taught,
        'total_conversations': total_conversations
    })

@app.route('/admin/learn/approve/<int:suggestion_id>', methods=['POST'])
@login_required
def approve_learning(suggestion_id):
    """Approve a teaching suggestion and add to bot table"""
    conn = get_db()
    cur = conn.cursor()
    
    # Get suggestion
    cur.execute("SELECT message, suggested_response FROM teaching_suggestions WHERE id = ?", (suggestion_id,))
    suggestion = cur.fetchone()
    
    if suggestion:
        # Add to bot table
        cur.execute("""
            INSERT INTO bot (text, response, approved, times_used, teaching_date)
            VALUES (?, ?, 1, 0, CURRENT_TIMESTAMP)
        """, (suggestion['message'], suggestion['suggested_response']))
        
        # Mark as approved
        cur.execute("UPDATE teaching_suggestions SET status = 'approved' WHERE id = ?", (suggestion_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Learning approved!'})
    
    conn.close()
    return jsonify({'error': 'Suggestion not found'}), 404

@app.route('/admin/learn/reject/<int:suggestion_id>', methods=['POST'])
@login_required
def reject_learning(suggestion_id):
    """Reject a teaching suggestion"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE teaching_suggestions SET status = 'rejected' WHERE id = ?", (suggestion_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Suggestion rejected'})

@app.route('/admin/learn/add', methods=['POST'])
@login_required
def add_qa():
    """Manually add a Q&A pair"""
    data = request.json
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    
    if not question or not answer:
        return jsonify({'error': 'Question and answer required'}), 400
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bot (text, response, approved, times_used, teaching_date)
        VALUES (?, ?, 1, 0, CURRENT_TIMESTAMP)
    """, (question, answer))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Q&A added!'})

@app.route('/admin/learn/auto', methods=['POST'])
@login_required
def auto_learn():
    """Auto-learn from successful conversations"""
    conn = get_db()
    cur = conn.cursor()
    
    # Find conversations that appear multiple times (popular patterns)
    cur.execute("""
        SELECT message, response, COUNT(*) as count
        FROM chat_history
        WHERE response IS NOT NULL AND response != ''
        GROUP BY message, response
        HAVING COUNT(*) >= 2
        ORDER BY count DESC
        LIMIT 10
    """)
    
    popular = [dict(row) for row in cur.fetchall()]
    
    # Auto-add to teaching suggestions for review
    added = 0
    for item in popular:
        # Check if already exists in suggestions or bot
        cur.execute("SELECT id FROM teaching_suggestions WHERE message = ? AND status = 'pending'", (item['message'],))
        existing = cur.fetchone()
        if not existing:
            cur.execute("""
                INSERT INTO teaching_suggestions (user_id, message, suggested_response, status, created_at)
                VALUES ('auto', ?, ?, 'pending', CURRENT_TIMESTAMP)
            """, (item['message'], item['response']))
            added += 1
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': f'Auto-learned {added} conversations',
        'learned': len(popular)
    })

# ========== TEACH ENDPOINT FOR USERS ==========

@app.route('/teach', methods=['POST'])
def teach():
    """Submit teaching suggestion"""
    data = request.json
    message = data.get('message', '').strip()
    suggested_response = data.get('response', '').strip()
    user_id = data.get('userId', 'anonymous')
    
    if not message or not suggested_response:
        return jsonify({'error': 'Message and response required'}), 400
    
    success = JAI.save_teaching_suggestion(user_id, message, suggested_response)
    
    if success:
        return jsonify({'success': True, 'message': 'Thank you! JAI will learn from your suggestion.'})
    else:
        return jsonify({'error': 'Failed to save suggestion'}), 500

# ========== MAIN ROUTES ==========

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
        'personality': 'Balanced Human Companion',
        'tagline': 'Work, rest, love, build. You can do all.',
        'lesson_loaded': current_lesson_id is not None,
        'lesson': current_lesson_title
    })

# ========== INITIALIZATION ==========

setup_database()
load_current_lesson()

if __name__ == '__main__':
    logger.info("🗣️ JAI - Balanced Companion starting...")
    app.run(host='0.0.0.0', port=PORT, debug=False)