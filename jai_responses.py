"""JAI - Joshua's Artificial Intelligence
Your companion, coach, friend, calculator, and calendar.
Now with NLP for true language understanding.
"""

import random
import re
from datetime import datetime
from jai_nlp import JAINLP
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
        
        # Step 1: Normalize Nigerian slang
        normalized = JAINLP.normalize_nigerian_slang(message)
        
        # Step 2: Analyze sentence with NLP
        analysis = JAINLP.analyze_sentence(message)
        
        # Step 3: Extract intent
        intent = JAINLP.extract_intent(message)
        
        # ========== TIME GREETINGS ==========
        if any(g in msg for g in ["good morning", "morning"]):
            return "Good morning! 🌅 Hope you slept well. What's on your agenda today?"
        if any(g in msg for g in ["good afternoon", "afternoon"]):
            return "Good afternoon! 🌞 How's your day treating you?"
        if any(g in msg for g in ["good evening", "evening"]):
            return "Good evening! 🌙 Hope you had a productive day."
        if any(g in msg for g in ["good night", "night"]):
            return "Good night! 🌙 Rest well. Tomorrow is another chance."
        
        # ========== INTENT-BASED RESPONSES ==========
        
        # Greeting
        if intent == 'greeting':
            return random.choice([
                "Hey! What's good? How are you doing?",
                "Yo! What's happening? You okay today?",
                "Hey there! What's the vibe?",
                "Hello! Good to see you. What's on your mind?"
            ])
        
        # Thank you
        if intent == 'thanks':
            return random.choice([
                "You're welcome! 😊 Anything else you need?",
                "Anytime! That's what I'm here for.",
                "Glad I could help! What's next?"
            ])
        
        # Goodbye
        if intent == 'goodbye':
            return random.choice([
                "Alright! Take care. Come back anytime!",
                "Later! You're doing great.",
                "See you soon! Remember: start before you're ready."
            ])
        
        # Positive emotion detection
        if intent == 'positive_emotion' and analysis:
            polarity = analysis['sentiment']['polarity']
            if polarity > 0.5:
                return f"That's amazing! 🎉 Tell me what's making you so happy. I want to celebrate with you!"
            return f"That's great to hear! 😊 What's been going well? Share it with me."
        
        # Negative emotion detection
        if intent == 'negative_emotion' and analysis:
            polarity = analysis['sentiment']['polarity']
            if polarity < -0.5:
                return "I hear you. That sounds really heavy. You're not alone in this. Want to talk about what's going on?"
            return "I hear you. Sometimes things feel tough. What's weighing on you right now? I'm here to listen."
        
        # Ask about creator
        if intent == 'ask_creator':
            return "I was built by Joshua Giwa from Yukuben, Nigeria. He's a web developer, a dreamer, and someone who believes people are more than their struggles. He built me to be here for you. What's on your heart today?"
        
        # Ask about capabilities
        if intent == 'ask_capabilities':
            return "I can do a few things:\n\n🧮 **Calculate** — percentages, equations, anything\n💰 **Convert currency** — USD, EUR, GBP to NGN\n📅 **Check dates** — today's date, time, day of week\n💬 **Talk** — life, work, relationships, dreams\n📚 **Teach** — cyber security lessons\n\nWhat do you need help with right now?"
        
        # Ask about time/date
        if intent == 'ask_date':
            return f"📅 Today is {now.strftime('%A, %B %d, %Y')}. What are you doing with it?"
        if intent == 'ask_time':
            return f"🕐 It's {now.strftime('%I:%M %p')}. Time to make moves!"
        
        # Ask about calculation
        if intent == 'ask_calculation':
            return "Yes! 🧮 I can calculate anything. Just ask me like 'What's 15% of 200?' or '4+4'. What do you want to calculate?"
        
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
        
        # ========== LESSON ==========
        if lesson_title != "No lesson uploaded" and any(l in msg for l in ["lesson", "learn", "teach", "cyber"]):
            return f"Today's lesson: '{lesson_title}'. Want to dive in?"
        
        # ========== WORD FORMATION CHECKS ==========
        # Check if the user is asking about word formation
        if any(w in msg for w in ["word", "vowel", "consonant", "spell", "syllable"]):
            words = re.findall(r'\b\w+\b', message)
            for word in words:
                if len(word) > 2 and word not in ['the', 'and', 'for', 'you', 'what']:
                    if not JAINLP.has_vowel(word):
                        return f"'{word}' doesn't have any vowels! A proper word needs at least one vowel (a, e, i, o, u)."
                    syllables = JAINLP.count_syllables(word)
                    return f"'{word}' has {syllables} syllable{'s' if syllables != 1 else ''}. It contains vowels: {', '.join([v for v in word.lower() if v in JAINLP.VOWELS])}"
        
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
        # Use extracted keywords to personalize response
        keywords = JAINLP.extract_keywords(message)
        if keywords:
            keyword_context = f" about {keywords[0]}" if keywords else ""
            return f"{random.choice(['That\'s interesting', 'Tell me more', 'I hear you'])}{keyword_context}. {random.choice(['What else is on your mind', 'How are you feeling about that', 'What do you think'])}?"
        
        # ========== DEFAULT ==========
        return random.choice([
            "I'm here. What's on your mind?",
            "What's good? I'm listening.",
            "Tell me what's going on. No small talk needed.",
            "How's your heart today?",
            "That's interesting. Tell me more.",
            "Keep going. I'm listening."
        ])