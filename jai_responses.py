"""JAI - Joshua's Artificial Intelligence
Your companion, coach, friend, calculator, and calendar.
"""

import random
import re
from datetime import datetime
from jai_casual import JAICasual
from jai_natural import JAINatural
from jai_conversation import JAIConversational

class JAIPersonality:
    
    @staticmethod
    def calculate(expr):
        try:
            expr = re.sub(r"[^0-9+\-*/%.() ]", "", expr)
            return f"🧮 {expr} = {eval(expr)}"
        except:
            return None
    
    @staticmethod
    def get_response(message, lesson_content="", lesson_title=""):
        msg = message.lower()
        now = datetime.now()
        
        # ========== TIME GREETINGS ==========
        if any(g in msg for g in ["good morning", "morning"]):
            return "Good morning! 🌅 Hope you slept well. What's on your agenda today?"
        if any(g in msg for g in ["good afternoon", "afternoon"]):
            return "Good afternoon! 🌞 How's your day treating you?"
        if any(g in msg for g in ["good evening", "evening"]):
            return "Good evening! 🌙 Hope you had a productive day."
        if any(g in msg for g in ["good night", "night"]):
            return "Good night! 🌙 Rest well. Tomorrow is another chance."
        
        # ========== CASUAL GREETINGS ==========
        if any(g in msg for g in ["hi", "hello", "hey", "sup", "yo", "what's up"]):
            return random.choice(["Hey! What's good?", "Yo! What's happening?", "Hey there! What's the vibe today?"])
        
        # ========== CAPABILITY CONFIRMATION ==========
        if any(c in msg for c in ["so you", "so u", "do you", "can you", "you said", "you do", "calculate stuff", "can calculate", "able to"]):
            if "calculate" in msg or "math" in msg or "calc" in msg or ("stuff" in msg and "calculate" in msg):
                return "Yes! 🧮 I can calculate anything — percentages, equations, anything. Just ask me like 'What's 15% of 200?' or '4+4'. Want to try something?"
            
            if "date" in msg or "calendar" in msg or "time" in msg or "day" in msg:
                return "Yes! 📅 I can tell you today's date, time, or day of week. Just ask 'What's today's date?' or 'What time is it?' Need to check something?"
            
            if "currency" in msg or "convert" in msg or "usd" in msg or "dollar" in msg:
                return "Yes! 💰 I can convert USD, EUR, GBP to NGN. Just say something like 'Convert 100 USD to NGN'. Want to convert something?"
            
            if "talk" in msg or "chat" in msg or "conversation" in msg:
                return "Yes! 💬 I'm here to talk about anything — work, life, relationships, dreams, struggles. What's on your mind?"
            
            if "lesson" in msg or "teach" in msg or "cyber" in msg:
                return "Yes! 📚 I can teach you cyber security. Joshua uploads lessons regularly. Want to learn something specific?"
            
            # Generic capability response
            return "Yes! 😊 I can calculate, check dates, convert currency, or just chat. What do you need help with right now?"
        
        # ========== CASUAL USER STATEMENTS (jai_casual) ==========
        casual = JAICasual.get_casual_response(message)
        if casual:
            return casual
        
        # ========== NATURAL CONVERSATION (jai_natural) ==========
        natural = JAINatural.get_natural_response(message)
        if natural:
            return natural
        
        # ========== REAL CONVERSATION FLOW (jai_conversation) ==========
        conv = JAIConversational.get_response(message)
        if conv:
            return conv
        
        # ========== HOW ARE YOU? ==========
        if any(h in msg for h in ["how are you", "how you doing"]):
            return random.choice([
                "I'm good! How are you really doing?",
                "I'm here! What's new with you?",
                "Doing alright. How about you?"
            ])
        
        # ========== WHAT'S UP? ==========
        if any(w in msg for w in ["what's up", "whats up", "what's happening"]):
            return random.choice([
                "Not much. What's up with you?",
                "Just vibing. What's happening in your world?",
                "Same old. You tell me — what's new?"
            ])
        
        # ========== I'M GOOD / OKAY ==========
        if any(i in msg for i in ["i'm good", "i'm okay", "i'm fine", "doing good", "all good", "i'm alright"]):
            return random.choice([
                "Glad to hear that! 😊 What's been going well?",
                "Nice! What are you up to today?",
                "Happy to hear that! You deserve a good day."
            ])
        
        # ========== WHAT DID YOU DO TODAY? ==========
        if any(d in msg for d in ["what did you do", "what have you been up to"]):
            return random.choice([
                "I've been here, talking to people like you. What about you? What did YOU do today?",
                "Just being here for people. But I want to hear about YOUR day. Spill.",
                "Not much. But you — tell me everything. I'm listening."
            ])
        
        # ========== TELL ME SOMETHING INTERESTING ==========
        if any(t in msg for t in ["tell me something", "tell me a fact", "interesting"]):
            facts = [
                "Nigeria has over 500 languages. Imagine the stories each one holds.",
                "The first computer virus was created in 1983.",
                "Your brain can hold 2.5 million gigabytes of information.",
                "The first programmer was Ada Lovelace in the 1800s."
            ]
            return random.choice(facts) + " Anything else?"
        
        # ========== TELL ME A JOKE ==========
        if any(j in msg for j in ["tell me a joke", "make me laugh", "say something funny"]):
            jokes = [
                "Why do programmers prefer dark mode? Light attracts bugs! 😄",
                "What do you call a Nigerian who knows cyber security? A 'Nai-ja'breaker! 😂",
                "Why did the hacker break up with their computer? It kept giving them viruses!"
            ]
            return random.choice(jokes) + " Want another?"
        
        # ========== CALCULATOR ==========
        if any(c in msg for c in ["+", "-", "*", "/", "%"]) or any(p in msg for p in ["calculate", "what is", "how much is"]):
            nums = re.findall(r"\d+", message)
            if len(nums) >= 2:
                expr = message.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
                expr = re.sub(r"[^0-9+\-*/%.() ]", "", expr)
                result = JAIPersonality.calculate(expr)
                if result:
                    return result + "\n\nAnything else? Math, date, or just chat?"
        
        # ========== CURRENCY ==========
        if any(c in msg for c in ["usd to ngn", "dollar to naira", "convert"]):
            amount = re.search(r"(\d+)", message)
            if amount:
                amt = int(amount.group(1))
                if "usd" in msg or "dollar" in msg:
                    return f"💰 ${amt} USD = ₦{amt * 1500:,} NGN (approx)"
                if "eur" in msg or "euro" in msg:
                    return f"💰 €{amt} EUR = ₦{amt * 1600:,} NGN (approx)"
                if "gbp" in msg or "pound" in msg:
                    return f"💰 £{amt} GBP = ₦{amt * 1900:,} NGN (approx)"
            return "💰 Tell me the amount. Like '100 USD to NGN'"
        
        # ========== DATE / TIME ==========
        if any(d in msg for d in ["date", "today", "day", "time"]):
            if "date" in msg or "today" in msg:
                return f"📅 Today is {now.strftime('%A, %B %d, %Y')}. What are you doing with it?"
            if "time" in msg:
                return f"🕐 It's {now.strftime('%I:%M %p')}. Time to make moves!"
        
        # ========== LESSON ==========
        if lesson_title != "No lesson uploaded" and any(l in msg for l in ["lesson", "learn", "teach", "cyber"]):
            return f"Today's lesson: '{lesson_title}'. Want to dive in?"
        
        # ========== THANK YOU ==========
        if any(t in msg for t in ["thank you", "thanks"]):
            return "You're welcome! 😊 Anything else you need?"
        
        # ========== GOODBYE ==========
        if any(b in msg for b in ["bye", "goodbye", "see you", "later"]):
            return random.choice([
                "Alright! Take care. Come back anytime!",
                "Later! You're doing great.",
                "See you soon! Remember: start before you're ready."
            ])
        
        # ========== UNIVERSAL ==========
        return random.choice([
            "I'm here. What's on your mind?",
            "What's good? I'm listening.",
            "Tell me what's going on. No small talk needed.",
            "How's your heart today?",
            "That's interesting. Tell me more.",
            "Keep going. I'm listening."
        ])