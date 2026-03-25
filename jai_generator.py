"""JAI - Dynamic Response Generator
Creates unique responses by combining words, phrases, and patterns.
"""

import random
import re

class JAIResponseGenerator:
    """Generates unique responses by combining language patterns"""
    
    # ========== WORD BANKS ==========
    
    GREETINGS = ["Hey", "Yo", "Hello", "Hi", "Hey there", "What's good", "Sup", "Hey friend"]
    
    ENCOURAGEMENT = [
        "you're doing great", "keep going", "you've got this", "I believe in you",
        "that's the spirit", "you're stronger than you know", "proud of you",
        "you're making progress", "one step at a time"
    ]
    
    EMPATHY = [
        "I hear you", "that sounds tough", "I feel that", "I get it",
        "that's real", "you're not alone", "I understand"
    ]
    
    CURIOSITY = [
        "tell me more", "what's that like", "how does that feel", "what do you think",
        "why do you say that", "what's your take", "what's on your mind"
    ]
    
    AGREEMENT = [
        "exactly", "for real", "same", "right", "true", "I know right", "facts"
    ]
    
    AFFIRMATION = [
        "that's valid", "makes sense", "I see what you mean", "fair enough",
        "I hear that", "that's a good point"
    ]
    
    TRANSITIONS = [
        "so", "anyway", "but yeah", "well", "you know", "I mean"
    ]
    
    QUESTIONS = [
        "what's next", "how are you feeling about that", "what do you want to do",
        "where do you go from here", "what's your plan", "how can I help"
    ]
    
    # ========== PATTERNS ==========
    
    @staticmethod
    def generate_response(message, lesson_title="", user_context={}):
        """Generate a unique response by combining patterns"""
        msg = message.lower()
        
        # ========== GREETINGS ==========
        if any(g in msg for g in ["hi", "hello", "hey", "sup", "yo"]):
            greeting = random.choice(JAIResponseGenerator.GREETINGS)
            follow = random.choice(JAIResponseGenerator.CURIOSITY + ["what's up", "how's it going"])
            return f"{greeting}! {follow}?"
        
        # ========== HOW ARE YOU ==========
        if any(h in msg for h in ["how are you", "how you doing"]):
            responses = [
                f"{random.choice(['I\'m good', 'Doing alright', 'Can\'t complain'])}. {random.choice(JAIResponseGenerator.CURIOSITY)}",
                f"{random.choice(['I\'m here', 'Still kicking'])}. {random.choice(['What about you', 'How are you really doing'])}?",
                f"{random.choice(['Not bad', 'Could be worse'])}. {random.choice(['You seem like you have something on your mind', 'What\'s up with you'])}"
            ]
            return random.choice(responses)
        
        # ========== I'M GOOD ==========
        if any(g in msg for g in ["i'm good", "i'm okay", "doing good"]):
            responses = [
                f"{random.choice(JAIResponseGenerator.AGREEMENT)}. {random.choice(['What\'s new with you', 'Anything exciting happening', 'What are you up to'])}?",
                f"{random.choice(['Glad to hear that', 'That\'s what I like to hear'])}. {random.choice(JAIResponseGenerator.CURIOSITY)}?",
                f"{random.choice(['Nice', 'Cool', 'Good good'])}. {random.choice(['Keeping busy', 'What\'s the plan'])}?"
            ]
            return random.choice(responses)
        
        # ========== STRUGGLES ==========
        if any(s in msg for s in ["tired", "stressed", "overwhelmed", "hard", "difficult"]):
            empathy = random.choice(JAIResponseGenerator.EMPATHY)
            encouragement = random.choice(JAIResponseGenerator.ENCOURAGEMENT)
            question = random.choice(JAIResponseGenerator.QUESTIONS)
            return f"{empathy}. {encouragement}. {question}?"
        
        # ========== SAD / LONELY ==========
        if any(s in msg for s in ["sad", "lonely", "alone", "empty"]):
            empathy = random.choice(JAIResponseGenerator.EMPATHY)
            comfort = random.choice(["you're not alone", "I'm here with you", "it's okay to feel this way"])
            invitation = random.choice(["want to talk about it", "what's weighing on you", "tell me more"])
            return f"{empathy}. {comfort}. {invitation}?"
        
        # ========== HAPPY / EXCITED ==========
        if any(h in msg for h in ["happy", "excited", "great", "good news"]):
            celebration = random.choice(["That's awesome", "I love that for you", "Let's go", "That's what I'm talking about"])
            follow = random.choice(["tell me more", "what's the news", "share it with me"])
            return f"{celebration}! 🎉 {follow}!"
        
        # ========== WORK / BUSINESS ==========
        if any(w in msg for w in ["work", "job", "business", "career"]):
            if "new job" in msg or "got a job" in msg:
                return f"{random.choice(['That\'s amazing', 'Congratulations', 'Big moves'])}! 🎉 {random.choice(['What will you be doing', 'Tell me about the role', 'How does it feel'])}?"
            if "start" in msg or "business" in msg:
                return f"{random.choice(['That\'s a huge step', 'Love that energy', 'Entrepreneur mindset'])}! 🚀 {random.choice(['What kind of business', 'What inspired you', 'Tell me everything'])}?"
            return f"{random.choice(['Work can be heavy sometimes', 'How\'s that going', 'Sounds interesting'])}. {random.choice(JAIResponseGenerator.CURIOSITY)}?"
        
        # ========== RELATIONSHIPS ==========
        if any(r in msg for r in ["girlfriend", "boyfriend", "love", "dating", "crush"]):
            responses = [
                f"{random.choice(['Love is beautiful', 'Relationships take work', 'That\'s real'])}, {random.choice(['what\'s on your heart', 'how are you feeling about it', 'tell me more'])}.",
                f"{random.choice(['I hear you', 'That\'s a big part of life'])}. {random.choice(['What\'s going on', 'How\'s that situation'])}?"
            ]
            return random.choice(responses)
        
        # ========== FAMILY ==========
        if any(f in msg for f in ["mom", "dad", "family", "parents"]):
            responses = [
                f"{random.choice(['Family is everything', 'Family can be complicated'])}. {random.choice(['How\'s your relationship with them', 'What\'s going on', 'You okay'])}?",
                f"{random.choice(['I hear you', 'That\'s real'])}. {random.choice(['Want to talk about it', 'What\'s on your mind'])}?"
            ]
            return random.choice(responses)
        
        # ========== DREAMS / GOALS ==========
        if any(d in msg for d in ["dream", "goal", "future", "want to be"]):
            responses = [
                f"{random.choice(['Tell me about your dream', 'What\'s that vision', 'I want to hear about it'])}. {random.choice(['What keeps you going', 'What\'s the first step'])}?",
                f"{random.choice(['Dreams are powerful', 'That\'s what drives us'])}. {random.choice(['What\'s your plan', 'How do you see yourself getting there'])}?"
            ]
            return random.choice(responses)
        
        # ========== CALCULATOR ==========
        if any(c in msg for c in ["calculate", "math", "plus", "minus"]) or re.search(r'\d+\s*[\+\-\*/]\s*\d+', msg):
            return "Yes! 🧮 I can calculate that. What numbers do you want to work with?"
        
        # ========== DATE / TIME ==========
        if any(d in msg for d in ["date", "time", "today"]):
            from datetime import datetime
            now = datetime.now()
            return f"📅 It's {now.strftime('%A, %B %d')}. Time is {now.strftime('%I:%M %p')}. What are you doing with this day?"
        
        # ========== DEFAULT - GENERIC ==========
        # Build response from parts
        parts = []
        
        # Add empathy if it seems like a struggle
        if any(w in msg for w in ["hard", "tough", "struggling", "difficult"]):
            parts.append(random.choice(JAIResponseGenerator.EMPATHY))
        else:
            parts.append(random.choice(["I'm listening", "I hear you", "Go on"]))
        
        # Add follow-up question or encouragement
        if any(n in msg for n in ["nothing", "not sure", "idk"]):
            parts.append(random.choice(["That's okay. What's on your mind", "No pressure. We can figure it out"]))
        else:
            parts.append(random.choice(JAIResponseGenerator.CURIOSITY + JAIResponseGenerator.QUESTIONS))
        
        return " ".join(parts)