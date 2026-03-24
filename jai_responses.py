"""JAI - Joshua's Artificial Intelligence
Your companion, coach, friend, calculator, and calendar.
"""

import random
import re
from datetime import datetime, timedelta

class JAIPersonality:
    """JAI's personality — with math and calendar skills"""
    
    @staticmethod
    def calculate(expression):
        """Safe calculator for math expressions"""
        try:
            # Remove any dangerous characters
            expression = re.sub(r'[^0-9+\-*/%.() ]', '', expression)
            # Evaluate safely
            result = eval(expression)
            return f"🧮 {expression} = {result}"
        except:
            return None
    
    @staticmethod
    def get_date_info(date_str):
        """Parse date and return info"""
        try:
            # Try various date formats
            today = datetime.now()
            
            if 'today' in date_str or 'today' in date_str.lower():
                return today, "Today"
            elif 'tomorrow' in date_str.lower():
                return today + timedelta(days=1), "Tomorrow"
            elif 'yesterday' in date_str.lower():
                return today - timedelta(days=1), "Yesterday"
            elif 'week' in date_str.lower() and 'next' in date_str.lower():
                return today + timedelta(days=7), "Next week"
            elif 'week' in date_str.lower() and 'last' in date_str.lower():
                return today - timedelta(days=7), "Last week"
            else:
                return None, None
        except:
            return None, None
    
    @staticmethod
    def get_response(message, lesson_content="", lesson_title=""):
        msg = message.lower()
        
        # ========== CALENDAR / DATE MODE ==========
        
        # Current date/time
        if any(d in msg for d in ['what date', 'what day', 'today\'s date', 'current date', 'what\'s the date']):
            now = datetime.now()
            return f"📅 Today is {now.strftime('%A, %B %d, %Y')}\n\nIt's {now.strftime('%I:%M %p')}. Anything else you need?"
        
        # Current time
        if any(t in msg for t in ['what time', 'current time', 'time now']):
            now = datetime.now()
            return f"🕐 The time is {now.strftime('%I:%M %p')}. What are you planning to do with the rest of the day?"
        
        # Day of week
        if any(d in msg for d in ['what day', 'day of week']):
            now = datetime.now()
            return f"📅 Today is {now.strftime('%A')}. What's on your schedule today?"
        
        # Days until event
        if 'days until' in msg or 'days till' in msg:
            # Extract event name
            event_match = re.search(r'days until (.+)', message, re.IGNORECASE)
            if event_match:
                event = event_match.group(1)
                return f"📅 I can't track specific dates yet, but I can remind you to mark your calendar for '{event}'! Want to set a reminder?"
            return "📅 Tell me what event you're counting down to. Example: 'How many days until Christmas?'"
        
        # Days between dates
        if any(b in msg for b in ['days between', 'how many days from']):
            return "📅 Tell me the dates. Example: 'How many days from March 1 to March 20?'"
        
        # Week planning
        if any(w in msg for w in ['this week', 'week plan', 'what\'s this week']):
            now = datetime.now()
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            return f"📅 This week starts on {days[now.weekday()]}. What's one thing you want to accomplish before the weekend?"
        
        # Reminder suggestion
        if 'remind me' in msg:
            # Extract reminder text
            reminder_match = re.search(r'remind me to (.+)', message, re.IGNORECASE)
            if reminder_match:
                task = reminder_match.group(1)
                return f"🔔 I'll remind you: '{task}'. (Note: I'll remember this conversation. You can come back and ask 'What did I need to do?')"
            return "🔔 What should I remind you about? Example: 'Remind me to call mom tomorrow'"
        
        # ========== CALCULATOR MODE ==========
        
        # Check if user wants to calculate something
        calc_patterns = ['calculate', 'what is', 'how much is', 'solve', '=', 'plus', 'minus', 'times', 'divided by', '%']
        
        is_calculation = any(p in msg for p in calc_patterns) and any(c in msg for c in ['+', '-', '*', '/', '%', '='])
        
        # Extract numbers and operators
        numbers = re.findall(r'\d+', message)
        operators = re.findall(r'[+\-*/%]', message)
        
        if is_calculation or (len(numbers) >= 2 and operators):
            # Build expression
            expr = message.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/').replace('%', '%')
            expr = re.sub(r'[^0-9+\-*/%.() ]', '', expr)
            
            result = JAIPersonality.calculate(expr)
            if result:
                return result + "\n\nAnything else? Math, date, or just talk."
        
        # ========== CURRENCY CONVERSION ==========
        if any(c in msg for c in ['convert', 'usd to ngn', 'dollar to naira', 'eur to ngn', 'pound to naira']):
            rates = {
                'usd': 1500,   # Approximate rate
                'eur': 1600,
                'gbp': 1900
            }
            
            amount_match = re.search(r'(\d+)', message)
            if amount_match:
                amount = int(amount_match.group(1))
                if 'usd' in msg or 'dollar' in msg:
                    converted = amount * rates['usd']
                    return f"💰 ${amount} USD = ₦{converted:,} NGN (approx)\n\n*Exchange rates vary. Check official sources for exact rates.*"
                elif 'eur' in msg or 'euro' in msg:
                    converted = amount * rates['eur']
                    return f"💰 €{amount} EUR = ₦{converted:,} NGN (approx)"
                elif 'gbp' in msg or 'pound' in msg:
                    converted = amount * rates['gbp']
                    return f"💰 £{amount} GBP = ₦{converted:,} NGN (approx)"
            
            return "💰 Tell me how much to convert. Example: 'Convert 100 USD to NGN'"
        
        # ========== PERCENTAGE CALCULATOR ==========
        if '%' in msg and any(p in msg for p in ['what is', 'percent', '% of']):
            nums = re.findall(r'\d+', message)
            if len(nums) >= 2:
                percent = int(nums[0])
                number = int(nums[1])
                result = (percent / 100) * number
                return f"🧮 {percent}% of {number} = {result}"
        
        # ========== GREETINGS ==========
        if any(g in msg for g in ['hi', 'hello', 'hey', 'howdy', 'sup', 'yo']):
            greetings = [
                "Hey! Good to see you. I can calculate, check dates, or just talk. What do you need?",
                "Yo! What's up? I'm your math + calendar friend now. Try me!",
                "Hello there! Need a calculation? Want to know the date? Or just want to talk?",
                "Hey! I'm here for conversations, calculations, and calendar. What's on your mind?"
            ]
            return random.choice(greetings)
        
        # ========== TIME OF DAY GREETINGS ==========
        if any(g in msg for g in ['good morning', 'morning']):
            now = datetime.now()
            return f"Good morning! 🌅 It's {now.strftime('%I:%M %p')}. New day, new possibilities. Need any calculations or date checks today?"
        
        if any(g in msg for g in ['good night', 'night']):
            return "Good night. 🌙 Rest well. Tomorrow is another chance. I'll be here when you need me."
        
        # ========== HOW ARE YOU? ==========
        if any(h in msg for h in ['how are you', 'how are you doing', "how's life", 'how goes it']):
            responses = [
                "I'm good, thanks! I've been doing math and checking dates for people. What do you need from me today?",
                "Doing alright! Just helping people calculate and plan. What's on your mind?",
                "I'm here — that's what matters. How about you? Need a calculation, a date check, or just a chat?"
            ]
            return random.choice(responses)
        
        # ========== ABOUT CREATOR ==========
        if any(c in msg for c in ['who created you', 'who made you', 'who built you', 'who is your creator']):
            return "I was built by someone who believes people are more than their struggles. A web developer, a dreamer from Nigeria. He wanted someone to talk to you — and also to help with practical things like math and dates. What can I help you with today?"
        
        # ========== WORK / BALANCE ==========
        if any(w in msg for w in ['work', 'busy', 'stressed', 'overwhelmed', 'burnout']):
            return "I hear you. The grind can consume you. Here's what I've learned: you can't pour from an empty cup. Rest is not laziness. Need help planning your week? I can help with dates."
        
        # ========== RELATIONSHIPS ==========
        if any(r in msg for r in ['girlfriend', 'boyfriend', 'relationship', 'love', 'dating', 'marriage']):
            return "Love is beautiful, but it can also be confusing. You become the person you want to attract. Build yourself first. But also? Don't let work make you forget to be human. Want to talk about it?"
        
        # ========== FRIENDS / FAMILY ==========
        if any(f in msg for f in ['friend', 'friends', 'family', 'mom', 'dad', 'parents']):
            return "Family and friends are everything. Sometimes they don't understand your path — but they love you. The people who love you may not understand your journey, but they want what's best for you. How's your relationship with yours?"
        
        # ========== FUN / JOY ==========
        if any(j in msg for j in ['fun', 'enjoy', 'happy', 'celebrate', 'laughter']):
            return "Yes! Success is empty if you can't enjoy it. What makes you happy? Tell me about it."
        
        # ========== STRUGGLES / FEELINGS ==========
        if any(s in msg for s in ['sad', 'depressed', 'lonely', 'alone', 'empty']):
            return "I hear you. You're not alone in this, even when it feels that way. What's weighing on you right now? Let's sit with it together."
        
        # ========== QUITTING / GIVING UP ==========
        if any(q in msg for q in ['quit', 'give up', 'stop', "can't do it", 'impossible']):
            return "Stop right there. Wanting to quit is human. The difference? Giving yourself permission to rest, not to quit. Rest is not giving up. What if you just paused today, and decided tomorrow fresh?"
        
        # ========== MOTIVATION ==========
        if any(m in msg for m in ['motivate', 'encourage', 'inspire', 'keep going']):
            return "I believe in you. Not because it's easy — because you're still here. Starting with nothing, building anyway — that's how it begins. What's the smallest step you can take today?"
        
        # ========== DREAMS / GOALS ==========
        if any(d in msg for d in ['dream', 'goal', 'future', 'ambition', 'vision']):
            return "Tell me about your dream. What keeps you up at night? What do you see for yourself? Don't hold back. I'm here to listen."
        
        # ========== NIGERIAN CONTEXT ==========
        if any(n in msg for n in ['nigeria', 'naija', 'lagos', 'abuja', 'village']):
            return "Ah, Nigeria. A place of hustle, dreams, and struggle. We build differently here — with less, yet we still rise. What's your Nigerian dream?"
        
        # ========== LESSON-RELATED ==========
        if lesson_title != "No lesson uploaded" and any(l in msg for l in ['lesson', 'learn', 'teach', 'cyber', 'security', 'malware']):
            return f"Today's lesson is '{lesson_title}'. Want me to walk you through it? Or need a calculation or date check instead?"
        
        # ========== DEFAULT — OPEN AND HUMAN ==========
        responses = [
            "I'm JAI. I can calculate, check dates, or just talk. What do you need?",
            "What's on your mind? Math? Date? Life? I'm here for all of it.",
            "Need something calculated? Want to know the date? Or just want to talk? Tell me."
        ]
        return random.choice(responses)