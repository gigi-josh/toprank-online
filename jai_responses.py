"""JAI - Joshua's Artificial Intelligence
Your companion, coach, friend, calculator, and calendar.
Now with dynamic response generation.
"""

import random
import re
from datetime import datetime
from jai_generator import JAIResponseGenerator
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
        
        # ========== CAPABILITY CONFIRMATION ==========
        if any(c in msg for c in ["so you", "do you", "can you", "you said", "calculate stuff"]):
            if "calculate" in msg or "math" in msg:
                return "Yes! 🧮 I can calculate anything — percentages, equations, anything. Just ask me like 'What's 15% of 200?' or '4+4'. Want to try something?"
            return "Yes! 😊 I can calculate, check dates, convert currency, or just chat. What do you need?"
        
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
            return random.choice([
                "You're welcome! 😊 Anything else you need?",
                "Anytime! That's what I'm here for.",
                "Glad I could help! What's next?"
            ])
        
        # ========== GOODBYE ==========
        if any(b in msg for b in ["bye", "goodbye", "see you", "later"]):
            return random.choice([
                "Alright! Take care. Come back anytime!",
                "Later! You're doing great.",
                "See you soon! Remember: start before you're ready."
            ])
        
        # ========== CASUAL USER STATEMENTS ==========
        casual = JAICasual.get_casual_response(message)
        if casual:
            return casual
        
        # ========== NATURAL CONVERSATION ==========
        natural = JAINatural.get_natural_response(message)
        if natural:
            return natural
        
        # ========== REAL CONVERSATION FLOW ==========
        conv = JAIConversational.get_response(message)
        if conv:
            return conv
        
        # ========== DYNAMIC RESPONSE GENERATION ==========
        # This creates unique responses for anything not caught above
        return JAIResponseGenerator.generate_response(message, lesson_title)