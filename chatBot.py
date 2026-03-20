import os
import re
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import PyPDF2
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import hashlib
import hmac
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.getenv('CHATBOT_API_KEY', 'your_chatbot_api_key_here')
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME', 'k-lynx'),
    'user': os.getenv('DB_USER', 'Joshua'),
    'password': os.getenv('DB_PASSWORD', '27Kly'),
    'host': os.getenv('DB_HOST', 'k-lynx'),
    'port': os.getenv('DB_PORT', 5432)
}

# API Key authentication middleware
def require_api_key(f):
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        
        if not provided_key:
            logger.warning(f"API key missing from request from {request.remote_addr}")
            return jsonify({'error': 'API key required'}), 401
        
        # Use constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(provided_key, API_KEY):
            logger.warning(f"Invalid API key attempt from {request.remote_addr}")
            return jsonify({'error': 'Invalid API key'}), 403
            
        return f(*args, **kwargs)
    return decorated

# Load GPT-2 model (lazy loading to save memory)
class GPT2Model:
    _instance = None
    _model = None
    _tokenizer = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = GPT2Model()
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            logger.info("Loading GPT-2 model...")
            self.model_name = "gpt2"
            self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            logger.info("GPT-2 model loaded successfully!")
    
    def generate_response(self, prompt, max_length=50):
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            
            outputs = self.model.generate(
                inputs,
                max_new_tokens=max_length,
                no_repeat_ngram_size=2,
                temperature=0.7,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove the prompt from the response
            response = full_response[len(prompt):].strip()
            
            return response if response else "I'm not sure how to respond to that."
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I encountered an error while thinking."

# Load PDF knowledge base
class KnowledgeBase:
    _instance = None
    _text_data = ""
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = KnowledgeBase()
        return cls._instance
    
    def __init__(self):
        try:
            pdf_path = 'knowledge.pdf'
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        self._text_data += page.extract_text()
                logger.info(f"PDF loaded: {len(self._text_data)} characters")
            else:
                logger.warning("No knowledge.pdf found, running without knowledge base")
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
    
    def get_text_data(self):
        return self._text_data

# Initialize components
gpt2 = GPT2Model.get_instance()
knowledge = KnowledgeBase.get_instance()

# ========== CONTENT FILTERING ==========

class ContentFilter:
    # Inappropriate content patterns
    INAPPROPRIATE_PATTERNS = [
        r'\b(hate|kill|violent|racist|sexist|discriminate|abuse|harm)\b',
        r'\b(curse|swear|profanity|damn|hell)\b',  # Add actual curse words
        r'\b(terrorist|bomb|attack|weapon)\b',
        r'(sexual|explicit|porn|nude|xxx)',
    ]
    
    # Dogmatic language patterns
    DOGMATIC_PATTERNS = [
        r'\b(only way|must believe|absolute truth|always|never|everyone should)\b',
        r'\b(you have to|you must|everyone knows|obviously|clearly)\b',
        r'\b(without doubt|undoubtedly|certainly|definitely)\b',
        r'(correct answer|right answer|wrong answer)',
    ]
    
    @classmethod
    def is_appropriate(cls, text):
        """Check if text is appropriate"""
        if not text:
            return True
        
        text_lower = text.lower()
        
        # Check inappropriate patterns
        for pattern in cls.INAPPROPRIATE_PATTERNS:
            if re.search(pattern, text_lower):
                logger.warning(f"Inappropriate content detected: {pattern}")
                return False
        
        return True
    
    @classmethod
    def is_dogmatic(cls, text):
        """Check if text is too dogmatic"""
        if not text:
            return False
        
        text_lower = text.lower()
        
        # Check dogmatic patterns
        for pattern in cls.DOGMATIC_PATTERNS:
            if re.search(pattern, text_lower):
                logger.info(f"Dogmatic language detected: {pattern}")
                return True
        
        return False
    
    @classmethod
    def soften_dogmatic_response(cls, text):
        """Add softening phrases to dogmatic responses"""
        if cls.is_dogmatic(text):
            softeners = [
                "In my understanding, ",
                "Based on available information, ",
                "One perspective is that ",
                "Some might say that ",
                "It could be that "
            ]
            import random
            return random.choice(softeners) + text.lower()
        return text

# ========== DATABASE FUNCTIONS ==========

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

def get_taught_response(message):
    """Get a taught response from the database"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # First try exact match
        cur.execute("""
            SELECT response, times_used, teaching_date 
            FROM bot 
            WHERE text = %s AND approved = TRUE
            ORDER BY times_used ASC, teaching_date DESC 
            LIMIT 1
        """, (message,))
        
        result = cur.fetchone()
        
        if result:
            # Update usage count
            cur.execute(
                "UPDATE bot SET times_used = times_used + 1, last_used = NOW() WHERE text = %s",
                (message,)
            )
            conn.commit()
            
            return {
                'response': result['response'],
                'type': 'taught',
                'times_used': result['times_used']
            }
        
        # If no exact match, try fuzzy match (simple contains)
        cur.execute("""
            SELECT text, response, times_used 
            FROM bot 
            WHERE %s ILIKE '%' || text || '%' AND approved = TRUE
            ORDER BY LENGTH(text) DESC, times_used ASC
            LIMIT 1
        """, (message,))
        
        result = cur.fetchone()
        
        if result:
            # Update usage count
            cur.execute(
                "UPDATE bot SET times_used = times_used + 1, last_used = NOW() WHERE text = %s",
                (result['text'],)
            )
            conn.commit()
            
            return {
                'response': result['response'],
                'type': 'taught_fuzzy',
                'matched_pattern': result['text']
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting taught response: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_teaching_suggestion(user_id, message, response):
    """Save a teaching suggestion for review"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO teaching_suggestions (user_id, message, suggested_response, status, created_at)
            VALUES (%s, %s, %s, 'pending', NOW())
            RETURNING id
        """, (user_id, message, response))
        
        suggestion_id = cur.fetchone()[0]
        conn.commit()
        
        logger.info(f"Teaching suggestion {suggestion_id} saved from user {user_id}")
        return suggestion_id
        
    except Exception as e:
        logger.error(f"Error saving teaching suggestion: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_response_from_knowledge(message):
    """Check if message is in knowledge base"""
    text_data = knowledge.get_text_data()
    if not text_data:
        return None
    
    # Simple relevance check
    message_words = set(message.lower().split())
    text_words = set(text_data.lower().split())
    
    common_words = message_words.intersection(text_words)
    
    # If more than 50% of words match, it's relevant
    if len(common_words) > len(message_words) * 0.5:
        return "I found this in my knowledge base. " + gpt2.generate_response(message)
    
    return None

# ========== API ROUTES ==========

@app.route('/chat', methods=['POST'])
@require_api_key
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        user_id = data.get('userId')
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        logger.info(f"Chat request from user {user_id}: {message[:50]}...")
        
        # Check if message is appropriate
        if not ContentFilter.is_appropriate(message):
            return jsonify({
                'response': "I can only discuss appropriate topics. Please try a different question.",
                'type': 'filtered'
            })
        
        # Try to get taught response first
        taught = get_taught_response(message)
        if taught:
            response = ContentFilter.soften_dogmatic_response(taught['response'])
            return jsonify({
                'response': response,
                'type': taught['type']
            })
        
        # Check knowledge base
        knowledge_response = get_response_from_knowledge(message)
        if knowledge_response:
            return jsonify({
                'response': knowledge_response,
                'type': 'knowledge_base'
            })
        
        # Generate new response with GPT-2
        generated = gpt2.generate_response(message)
        softened = ContentFilter.soften_dogmatic_response(generated)
        
        return jsonify({
            'response': softened,
            'type': 'generated'
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/teach', methods=['POST'])
@require_api_key
def teach():
    try:
        data = request.json
        message = data.get('message', '').strip()
        response = data.get('response', '').strip()
        user_id = data.get('userId')
        
        if not message or not response:
            return jsonify({'error': 'Message and response required'}), 400
        
        # Check if content is appropriate
        if not ContentFilter.is_appropriate(message) or not ContentFilter.is_appropriate(response):
            return jsonify({
                'error': 'Teaching content must be appropriate'
            }), 400
        
        # Check for dogmatic language
        if ContentFilter.is_dogmatic(response):
            return jsonify({
                'error': 'Teaching response contains dogmatic language. Please rephrase more openly.'
            }), 400
        
        # Save for review
        suggestion_id = save_teaching_suggestion(user_id, message, response)
        
        if suggestion_id:
            return jsonify({
                'success': True,
                'message': 'Teaching suggestion submitted for review',
                'suggestion_id': suggestion_id
            })
        else:
            return jsonify({'error': 'Failed to save teaching suggestion'}), 500
            
    except Exception as e:
        logger.error(f"Teach error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': gpt2.model is not None,
        'knowledge_loaded': bool(knowledge.get_text_data()),
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('CHATBOT_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting chatbot API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)