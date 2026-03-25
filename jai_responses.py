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
        if any(c in msg for c in ["so you", "do you", "can you", "you said"]):
            if "calculate" in msg or "math" in msg:
                return "Yes! 🧮 I can calculate anything. Try '15% of 200' or '4+4'."
            if "date" in msg or "time" in msg:
                return f"📅 It's {now.strftime('%A, %B %d, %I:%M %p')}. Need anything else?"
            if "currency" in msg or "convert" in msg:
                return "💰 I can convert USD, EUR, GBP to NGN. Try '100 USD to NGN'."
            return "Yes! 😊 I can calculate, check dates, convert currency, or just chat."
        
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
        if any(i in msg for i in ["i'm good", "i'm okay", "i'm fine", "doing good"]):
            return random.choice([
                "Glad to hear that! 😊 What's been going well?",
                "Nice! What are you up to today?",
                "Happy to hear that! You deserve a good day."
            ])
        
        # ========== TELL ME SOMETHING ==========
        if any(t in msg for t in ["tell me something", "tell me a fact", "interesting"]):
            facts = [
                "Nigeria has over 500 languages. Imagine the stories each one holds.",
                "The first computer virus was created in 1983.",
                "Your brain can hold 2.5 million gigabytes of information.",
                "The first programmer was Ada Lovelace in the 1800s."
            ]
            return random.choice(facts) + " Anything else?"
        
        # ========== JOKE ==========
        if any(j in msg for j in ["tell me a joke", "make me laugh"]):
            jokes = [
                "Why do programmers prefer dark mode? Light attracts bugs! 😄",
                "What do you call a Nigerian who knows cyber security? A 'Nai-ja'breaker! 😂",
                "Why did the hacker break up with their computer? It kept giving them viruses!"
            ]
            return random.choice(jokes) + " Want another?"
        
        # ========== CALCULATOR ==========
        if any(c in msg for c in ["+", "-", "*", "/", "%"]) or any(p in msg for p in ["calculate", "what is"]):
            nums = re.findall(r"\d+", message)
            if len(nums) >= 2:
                expr = message.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
                expr = re.sub(r"[^0-9+\-*/%.() ]", "", expr)
                result = JAIPersonality.calculate(expr)
                if result:
                    return result + "\n\nAnything else?"
        
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