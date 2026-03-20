const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const dotenv = require('dotenv');
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');
const pdfParse = require('pdf-parse');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// ========== MIDDLEWARE ==========
app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting (prevent abuse)
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: { error: 'Too many requests, please try again later.' }
});
app.use('/api/', limiter);

// ========== DATABASE CONNECTION ==========
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// ========== KNOWLEDGE BASE (PDF LOADING) ==========
let knowledgeBaseText = '';

async function loadKnowledgeBase() {
    try {
        const pdfPath = path.join(__dirname, 'knowledge.pdf');
        if (fs.existsSync(pdfPath)) {
            const dataBuffer = fs.readFileSync(pdfPath);
            const pdfData = await pdfParse(dataBuffer);
            knowledgeBaseText = pdfData.text;
            console.log(`✅ Knowledge base loaded: ${knowledgeBaseText.length} characters`);
        } else {
            console.log('⚠️ No knowledge.pdf found, running without knowledge base');
        }
    } catch (error) {
        console.error('Error loading PDF:', error);
    }
}

loadKnowledgeBase();

// ========== CONTENT FILTERING ==========
class ContentFilter {
    static inappropriatePatterns = [
        /\b(hate|kill|violent|racist|sexist|discriminate|abuse|harm)\b/i,
        /\b(terrorist|bomb|attack|weapon)\b/i,
        /(sexual|explicit|porn|nude|xxx)/i
    ];

    static dogmaticPatterns = [
        /\b(only way|must believe|absolute truth|always|never|everyone should)\b/i,
        /\b(you have to|you must|everyone knows|obviously|clearly)\b/i,
        /\b(without doubt|undoubtedly|certainly|definitely)\b/i
    ];

    static isAppropriate(text) {
        if (!text) return true;
        for (const pattern of this.inappropriatePatterns) {
            if (pattern.test(text)) {
                console.warn(`Inappropriate content detected: ${pattern}`);
                return false;
            }
        }
        return true;
    }

    static isDogmatic(text) {
        if (!text) return false;
        for (const pattern of this.dogmaticPatterns) {
            if (pattern.test(text)) {
                console.log(`Dogmatic language detected: ${pattern}`);
                return true;
            }
        }
        return false;
    }

    static softenDogmaticResponse(text) {
        if (this.isDogmatic(text)) {
            const softeners = [
                "In my understanding, ",
                "Based on available information, ",
                "One perspective is that ",
                "Some might say that ",
                "It could be that "
            ];
            return softeners[Math.floor(Math.random() * softeners.length)] + text.toLowerCase();
        }
        return text;
    }
}

// ========== GPT-2 STYLE RESPONSE (Simulated or OpenAI) ==========
class AIGenerator {
    static async generateResponse(message) {
        // Option 1: Use OpenAI API (recommended for production)
        if (process.env.OPENAI_API_KEY) {
            try {
                const OpenAI = require('openai');
                const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
                
                const completion = await openai.chat.completions.create({
                    model: "gpt-3.5-turbo",
                    messages: [
                        { role: "system", content: "You are a cyber security teacher. You teach reverse engineering, malware analysis, and ethical hacking. You speak clearly and encourage students." },
                        { role: "user", content: message }
                    ],
                    max_tokens: 150,
                    temperature: 0.7
                });
                
                return completion.choices[0].message.content;
            } catch (error) {
                console.error('OpenAI error:', error);
                return this.getFallbackResponse(message);
            }
        }
        
        // Option 2: Simple rule-based responses (fallback)
        return this.getFallbackResponse(message);
    }
    
    static getFallbackResponse(message) {
        const lowerMsg = message.toLowerCase();
        
        if (lowerMsg.includes('malware') || lowerMsg.includes('virus')) {
            return "Malware is malicious software designed to harm or exploit devices. Types include viruses, worms, trojans, and ransomware. Would you like to learn how to detect them?";
        }
        
        if (lowerMsg.includes('reverse engineering')) {
            return "Reverse engineering is the process of analyzing software to understand its components and functionality. It's crucial for malware analysis and finding vulnerabilities.";
        }
        
        if (lowerMsg.includes('hacker')) {
            return "Ethical hackers help organizations find and fix security weaknesses. They use the same skills as malicious hackers, but with permission and for good.";
        }
        
        if (lowerMsg.includes('start') || lowerMsg.includes('beginner')) {
            return "To start in cyber security, learn networking basics, understand operating systems (especially Linux), and practice on platforms like TryHackMe or HackTheBox. I can guide you!";
        }
        
        return "That's a great question. I'm still learning about that topic. Would you like to ask something else about cyber security, reverse engineering, or ethical hacking?";
    }
}

// ========== DATABASE FUNCTIONS ==========
async function getTaughtResponse(message) {
    const client = await pool.connect();
    try {
        // First try exact match
        let result = await client.query(
            `SELECT response, times_used FROM bot 
             WHERE text = $1 AND approved = TRUE 
             ORDER BY times_used ASC LIMIT 1`,
            [message]
        );
        
        if (result.rows.length > 0) {
            // Update usage count
            await client.query(
                `UPDATE bot SET times_used = times_used + 1, last_used = NOW() 
                 WHERE text = $1`,
                [message]
            );
            
            return {
                response: result.rows[0].response,
                type: 'taught'
            };
        }
        
        // Try fuzzy match
        result = await client.query(
            `SELECT text, response FROM bot 
             WHERE $1 ILIKE '%' || text || '%' AND approved = TRUE 
             ORDER BY LENGTH(text) DESC LIMIT 1`,
            [message]
        );
        
        if (result.rows.length > 0) {
            return {
                response: result.rows[0].response,
                type: 'taught_fuzzy',
                matchedPattern: result.rows[0].text
            };
        }
        
        return null;
    } finally {
        client.release();
    }
}

async function saveTeachingSuggestion(userId, message, response) {
    const client = await pool.connect();
    try {
        const result = await client.query(
            `INSERT INTO teaching_suggestions (user_id, message, suggested_response, status, created_at)
             VALUES ($1, $2, $3, 'pending', NOW())
             RETURNING id`,
            [userId, message, response]
        );
        return result.rows[0].id;
    } finally {
        client.release();
    }
}

async function getResponseFromKnowledge(message) {
    if (!knowledgeBaseText) return null;
    
    // Simple relevance check
    const messageWords = new Set(message.toLowerCase().split(/\s+/));
    const textWords = new Set(knowledgeBaseText.toLowerCase().split(/\s+/));
    
    let commonCount = 0;
    for (const word of messageWords) {
        if (textWords.has(word)) commonCount++;
    }
    
    const matchRatio = commonCount / messageWords.size;
    if (matchRatio > 0.3) {
        const aiResponse = await AIGenerator.generateResponse(message);
        return `📚 From my knowledge base: ${aiResponse}`;
    }
    
    return null;
}

// ========== DATABASE SETUP (Run once) ==========
async function setupDatabase() {
    const client = await pool.connect();
    try {
        // Create bot table
        await client.query(`
            CREATE TABLE IF NOT EXISTS bot (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                response TEXT NOT NULL,
                approved BOOLEAN DEFAULT FALSE,
                times_used INTEGER DEFAULT 0,
                teaching_date TIMESTAMP DEFAULT NOW(),
                last_used TIMESTAMP
            )
        `);
        
        // Create teaching suggestions table
        await client.query(`
            CREATE TABLE IF NOT EXISTS teaching_suggestions (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100),
                message TEXT NOT NULL,
                suggested_response TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT NOW()
            )
        `);
        
        // Create chat history table (optional)
        await client.query(`
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(100),
                message TEXT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT NOW()
            )
        `);
        
        console.log('✅ Database tables ready');
    } catch (error) {
        console.error('Database setup error:', error);
    } finally {
        client.release();
    }
}

setupDatabase();

// ========== API ROUTES ==========

// Health check
app.get('/health', async (req, res) => {
    let dbStatus = 'disconnected';
    try {
        await pool.query('SELECT 1');
        dbStatus = 'connected';
    } catch (e) {
        dbStatus = 'error';
    }
    
    res.json({
        status: 'healthy',
        model: process.env.OPENAI_API_KEY ? 'GPT-3.5 Turbo' : 'Fallback Mode',
        knowledge_loaded: knowledgeBaseText.length > 0,
        database: dbStatus,
        timestamp: new Date().toISOString()
    });
});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message, userId = 'anonymous' } = req.body;
        
        if (!message || message.trim() === '') {
            return res.status(400).json({ error: 'Message required' });
        }
        
        console.log(`Chat from ${userId}: ${message.substring(0, 50)}...`);
        
        // Check if appropriate
        if (!ContentFilter.isAppropriate(message)) {
            return res.json({
                response: "I can only discuss appropriate topics. Please ask about cyber security, reverse engineering, or ethical hacking.",
                type: 'filtered'
            });
        }
        
        // Try taught response first
        const taught = await getTaughtResponse(message);
        if (taught) {
            const response = ContentFilter.softenDogmaticResponse(taught.response);
            
            // Save to chat history
            await pool.query(
                `INSERT INTO chat_history (user_id, message, response) VALUES ($1, $2, $3)`,
                [userId, message, response]
            );
            
            return res.json({
                response,
                type: taught.type
            });
        }
        
        // Try knowledge base
        const knowledgeResponse = await getResponseFromKnowledge(message);
        if (knowledgeResponse) {
            const response = ContentFilter.softenDogmaticResponse(knowledgeResponse);
            
            await pool.query(
                `INSERT INTO chat_history (user_id, message, response) VALUES ($1, $2, $3)`,
                [userId, message, response]
            );
            
            return res.json({
                response,
                type: 'knowledge_base'
            });
        }
        
        // Generate new response
        let generated = await AIGenerator.generateResponse(message);
        const softened = ContentFilter.softenDogmaticResponse(generated);
        
        await pool.query(
            `INSERT INTO chat_history (user_id, message, response) VALUES ($1, $2, $3)`,
            [userId, message, softened]
        );
        
        return res.json({
            response: softened,
            type: 'generated'
        });
        
    } catch (error) {
        console.error('Chat error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Teach endpoint (submit suggestions)
app.post('/api/teach', async (req, res) => {
    try {
        const { message, response, userId = 'anonymous' } = req.body;
        
        if (!message || !response) {
            return res.status(400).json({ error: 'Message and response required' });
        }
        
        if (!ContentFilter.isAppropriate(message) || !ContentFilter.isAppropriate(response)) {
            return res.status(400).json({ error: 'Content must be appropriate' });
        }
        
        if (ContentFilter.isDogmatic(response)) {
            return res.status(400).json({ error: 'Response contains dogmatic language. Please rephrase more openly.' });
        }
        
        const suggestionId = await saveTeachingSuggestion(userId, message, response);
        
        res.json({
            success: true,
            message: 'Teaching suggestion submitted for review',
            suggestion_id: suggestionId
        });
        
    } catch (error) {
        console.error('Teach error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// Get student progress
app.get('/api/progress/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        
        const result = await pool.query(
            `SELECT message, response, timestamp 
             FROM chat_history 
             WHERE user_id = $1 
             ORDER BY timestamp DESC 
             LIMIT 20`,
            [userId]
        );
        
        res.json({
            userId,
            interactions: result.rows.length,
            recent: result.rows
        });
        
    } catch (error) {
        console.error('Progress error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Cyber Security AI Teacher running on port ${PORT}`);
    console.log(`   Health check: http://localhost:${PORT}/health`);
    console.log(`   Chat endpoint: POST /api/chat`);
    console.log(`   Teach endpoint: POST /api/teach`);
});