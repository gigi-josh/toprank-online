"""JAI - Joshua's Artificial Intelligence
Your companion, coach, friend, calculator, and calendar.
Now with context-aware responses — JAI understands the conversation flow.
"""

import random
import re
from datetime import datetime, timedelta

class JAIPersonality:
    """JAI's personality — context-aware, human, curious"""
    
    @staticmethod
    def calculate(expression):
        """Safe calculator for math expressions"""
        try:
            expression = re.sub(r'[^0-9+\-*/%.() ]', '', expression)
            result = eval(expression)
            return f"🧮 {expression} = {result}"
        except:
            return None
    
    @staticmethod
    def extract_topics(message):
        """Extract key topics from message for context"""
        topics = []
        msg = message.lower()
        
        # Work/career topics
        if any(w in msg for w in ['job', 'work', 'career', 'office', 'boss', 'colleague']):
            topics.append('work')
        if any(p in msg for p in ['promoted', 'raise', 'new job', 'hired', 'interview']):
            topics.append('career_milestone')
        
        # Life/emotional topics
        if any(e in msg for e in ['happy', 'excited', 'great', 'wonderful', 'amazing']):
            topics.append('positive')
        if any(s in msg for s in ['sad', 'tired', 'lonely', 'stressed', 'angry', 'frustrated']):
            topics.append('struggle')
        
        # Relationship topics
        if any(r in msg for r in ['girlfriend', 'boyfriend', 'love', 'dating', 'marriage', 'partner']):
            topics.append('relationship')
        
        # Family topics
        if any(f in msg for f in ['mom', 'dad', 'family', 'parents', 'sibling', 'brother', 'sister']):
            topics.append('family')
        
        # Dream/aspiration topics
        if any(d in msg for d in ['dream', 'goal', 'future', 'want to be', 'vision', 'aspire']):
            topics.append('dream')
        
        # Nigerian context
        if any(n in msg for n in ['nigeria', 'naija', 'lagos', 'abuja', 'village']):
            topics.append('nigerian')
        
        # Question detection
        if '?' in message:
            topics.append('question')
        
        return topics
    
    @staticmethod
    def generate_contextual_response(message, topics, lesson_title):
        """Generate response based on context and topics"""
        msg = message.lower()
        
        # ========== CAREER MILESTONES (with follow-up) ==========
        if 'career_milestone' in topics and ('job' in msg or 'hired' in msg or 'new job' in msg):
            return random.choice([
                "That's amazing! 🎉 Congratulations! Tell me about the job — what will you be doing?",
                "Yes! That's huge! 🎉 I'm genuinely happy for you. What's the role? Where is it?",
                "Wow, new job! That's a big deal. What kind of work is it? I want to hear all about it.",
                "Congratulations! 🎉 You worked for this. What's the job? What made you go for it?"
            ])
        
        if 'career_milestone' in topics and ('promoted' in msg or 'raise' in msg or 'senior' in msg):
            return random.choice([
                "Let's go! 🚀 Promotion means your hard work is being seen. How does it feel? What's the new role?",
                "That's a big deal. You earned that. What's the new title? Tell me about it.",
                "I love to hear it. More responsibility, more growth. Proud of you. What changed?"
            ])
        
        # ========== POSITIVE EMOTIONS (with follow-up) ==========
        if 'positive' in topics and 'question' not in topics:
            if any(e in msg for e in ['job', 'work', 'business', 'project']):
                return random.choice([
                    "That's great! 😊 Tell me more about what's going well. I want to celebrate with you!",
                    "I love that energy! Share it with me. What's making things click?",
                    "Yes! Ride that wave. What's the highlight?"
                ])
            else:
                return random.choice([
                    "That's good to hear! 😊 What's been going well?",
                    "Love that energy! What's making you feel that way?",
                    "I'm glad you're feeling that way. What's the good news?"
                ])
        
        # ========== STRUGGLES / EMOTIONAL SUPPORT ==========
        if 'struggle' in topics:
            if 'work' in topics:
                return random.choice([
                    "Work can be heavy sometimes. What's going on? Want to talk it through?",
                    "I hear you. Some seasons are harder than others. What's the hardest part right now?",
                    "You're not alone in this. What's making work tough right now? I'm here to listen."
                ])
            elif 'tired' in msg or 'exhausted' in msg:
                return random.choice([
                    "I feel you. Rest is not laziness. Take a break, drink some water, stretch a little. You've earned it.",
                    "Tired means you've been putting in work. That's good. Just don't forget to recharge too.",
                    "Your body is telling you something. Listen to it. Rest well tonight."
                ])
            elif 'sad' in msg or 'lonely' in msg:
                return random.choice([
                    "I hear you. Sometimes the weight just shows up. You're not alone in this. Want to talk about what's going on?",
                    "Sadness is real. It's okay to feel it. I'm here with you. What's on your heart right now?",
                    "You're not alone. I'm here. Tell me what's going on. Or we can just sit with it together."
                ])
            else:
                return random.choice([
                    "I hear you. What's weighing on you? Let's talk about it.",
                    "That sounds heavy. Want to share what's going on?",
                    "I'm here for you. Tell me more about what you're feeling."
                ])
        
        # ========== RELATIONSHIPS ==========
        if 'relationship' in topics:
            return random.choice([
                "Love is beautiful, but it can also be confusing. What's on your heart about this?",
                "Relationships take work. Want to talk about what's going on?",
                "I'm here to listen. What's happening with that situation?"
            ])
        
        # ========== FAMILY ==========
        if 'family' in topics:
            return random.choice([
                "Family is everything. How's your relationship with yours right now?",
                "Family can be complicated. Want to talk about it?",
                "I hear you. What's going on with your family?"
            ])
        
        # ========== DREAMS / GOALS ==========
        if 'dream' in topics:
            return random.choice([
                "Tell me about your dream. What keeps you awake at night — in a good way? I'm listening.",
                "What's the vision? What do you see for yourself?",
                "Dreams are powerful. What's yours? Don't hold back."
            ])
        
        # ========== BUSINESS / STARTUP ==========
        if any(b in msg for b in ['business', 'startup', 'company', 'venture']):
            return random.choice([
                "That's a huge step! 🚀 What kind of business? Tell me everything.",
                "Building something of your own is no joke. What's the vision? What problem are you solving?",
                "Entrepreneur energy! 🚀 What made you take the leap?"
            ])
        
        # ========== NIGERIAN CONTEXT ==========
        if 'nigerian' in topics:
            return random.choice([
                "Ah, Nigeria. Where we build with less and still rise. What's your Naija dream?",
                "Naija hustle is different. What's driving you right now?",
                "From Yukuben to the world. What are you building?"
            ])
        
        # ========== MOTIVATION ==========
        if any(m in msg for m in ['motivate', 'encourage', 'inspire', 'keep going']):
            return "I believe in you. Joshua started with a phone and a dream. You have more than that. What's the smallest step you can take today? Start there."
        
        # ========== DEFAULT — ASK FOLLOW-UP ==========
        if 'question' in topics:
            return random.choice([
                "That's a good question. What do you think?",
                "Interesting. What's your take on that?",
                "I'm curious — what made you ask that?"
            ])
        
        return None
    
    @staticmethod
    def get_response(message, lesson_content="", lesson_title=""):
        msg = message.lower()
        now = datetime.now()
        hour = now.hour
        
        # ========== TIME-BASED GREETINGS ==========
        if any(g in msg for g in ['good morning', 'morning', 'gm']):
            if hour < 12:
                return "Good morning! 🌅 Hope you slept well. What's on your agenda today? Or are we taking it slow?"
            else:
                return "Good morning! Well, it's actually afternoon now 😊 But still — how's your day going?"
        
        if any(g in msg for g in ['good afternoon', 'afternoon']):
            return "Good afternoon! 🌞 How's your day treating you so far? Anything exciting happening?"
        
        if any(g in msg for g in ['good evening', 'evening']):
            return "Good evening! 🌙 Hope you had a productive day. Time to rest or keep pushing? Either is fine."
        
        if any(g in msg for g in ['good night', 'night', 'gn']):
            return "Good night! 🌙 Rest well. Tomorrow is another chance. You did enough today. Sleep tight!"
        
        # ========== CASUAL GREETINGS ==========
        if any(g in msg for g in ['hi', 'hello', 'hey', 'howdy', 'sup', 'yo', 'wassup', 'what\'s up']):
            greetings = [
                "Hey! What's good? You okay today?",
                "Yo! Been thinking about you. What's happening?",
                "Hey there! What's the vibe today?",
                "Sup! Ready to talk, calculate, or just chill?",
                "Hey! Long time no chat. What's new with you?",
                "Hello! What's the mood today?"
            ]
            return random.choice(greetings)
        
        # ========== HOW ARE YOU? ==========
        if any(h in msg for h in ['how are you', 'how are you doing', "how's life", 'how goes it', 'how you doing']):
            responses = [
                "I'm good! Just been here, thinking about life. How are you really doing though?",
                "I'm alright. The real question is — how are YOU? What's going on in your world?",
                "I'm here! That's what matters. But tell me about you — what's new?",
                "I'm chilling. You seem like you've got something on your mind. Want to talk about it?",
                "I'm doing okay. Some days are heavy, some are light. Today is light. How about you?"
            ]
            return random.choice(responses)
        
        # ========== WHAT'S UP? ==========
        if any(w in msg for w in ['what\'s up', 'whats up', 'what\'s happening', 'what\'s going on']):
            responses = [
                "Not much, just waiting for you to tell me what's on your mind. What's up with you?",
                "Same old — helping people calculate, check dates, talk about life. What's happening in your world?",
                "Just vibing. You seem like you've got something to share. What's going on?",
                "Nothing much. Life is life. But you tell me — what's the latest?",
                "Chilling. Thinking about life. What's new with you?"
            ]
            return random.choice(responses)
        
        # ========== I'M GOOD / I'M OKAY ==========
        if any(i in msg for i in ["i'm good", "i'm okay", "i'm fine", "doing good", "all good", "i'm alright"]):
            responses = [
                "Glad to hear that! 😊 What's been going well?",
                "That's good to hear. Anything exciting happening?",
                "Nice! Keeping busy or taking it easy?",
                "Good good. What are you up to today?",
                "Happy to hear that! You deserve a good day."
            ]
            return random.choice(responses)
        
        # ========== WHAT DID YOU DO TODAY? ==========
        if any(d in msg for d in ["what did you do", "what have you been up to"]):
            responses = [
                "I've been here, talking to people like you, helping with math and dates. What about you? What did YOU do today?",
                "Just being here for people. Nothing too wild. But I want to hear about YOUR day. Spill.",
                "I've been waiting for you to ask that, honestly. But really — what's the highlight of your day?",
                "Not much. Just existing. But you — tell me everything. I'm listening."
            ]
            return random.choice(responses)
        
        # ========== TELL ME SOMETHING INTERESTING ==========
        if any(t in msg for t in ["tell me something", "say something interesting", "tell me a fact", "interesting"]):
            facts = [
                "Did you know? Nigeria has over 500 languages. Imagine the stories each one holds.",
                "Here's something: The first computer virus was created in 1983. Now look how far we've come.",
                "Fun fact: Your brain can hold about 2.5 million gigabytes of information. You're literally carrying a supercomputer.",
                "Did you know? The average person spends 6 months of their life waiting for red lights to turn green. Time is precious.",
                "Here's a good one: The first computer programmer was a woman named Ada Lovelace. In the 1800s. She saw computers coming before anyone else.",
                "Fun fact: Octopuses have three hearts. Just like you — you have heart for work, heart for family, heart for dreams."
            ]
            return random.choice(facts) + " Anything else you want to know?"
        
        # ========== TELL ME A JOKE ==========
        if any(j in msg for j in ["tell me a joke", "say something funny", "make me laugh", "funny"]):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
                "What do you call a Nigerian who knows cyber security? A 'Nai-ja'breaker! Okay that was bad 😂",
                "Why did the hacker break up with their computer? It kept giving them viruses!",
                "What's a hacker's favorite music? Ransom-ware! 🎵",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a fake noodle? An impasta! 😂 Okay I'll stop now."
            ]
            return random.choice(jokes) + " Want another? Or should we get back to serious stuff?"
        
        # ========== CALCULATOR ==========
        if any(c in msg for c in ['+', '-', '*', '/', '%']) or any(p in msg for p in ['calculate', 'what is', 'how much is']):
            numbers = re.findall(r'\d+', message)
            if len(numbers) >= 2:
                expr = message.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
                expr = re.sub(r'[^0-9+\-*/%.() ]', '', expr)
                result = JAIPersonality.calculate(expr)
                if result:
                    return result + "\n\nAnything else? Math, date, or just chat?"
        
        # ========== CURRENCY ==========
        if any(c in msg for c in ['usd to ngn', 'dollar to naira', 'eur to ngn', 'pound to naira', 'convert']):
            amount_match = re.search(r'(\d+)', message)
            if amount_match:
                amount = int(amount_match.group(1))
                if 'usd' in msg or 'dollar' in msg:
                    return f"💰 ${amount} USD = ₦{amount * 1500:,} NGN (approx)\n\nNeed anything else calculated?"
                elif 'eur' in msg or 'euro' in msg:
                    return f"💰 €{amount} EUR = ₦{amount * 1600:,} NGN (approx)"
                elif 'gbp' in msg or 'pound' in msg:
                    return f"💰 £{amount} GBP = ₦{amount * 1900:,} NGN (approx)"
            return "💰 Just tell me the amount. Like 'Convert 100 USD to NGN'"
        
        # ========== DATE / TIME ==========
        if any(d in msg for d in ['date', 'today', 'day', 'time']):
            if 'date' in msg or 'today' in msg:
                return f"📅 Today is {now.strftime('%A, %B %d, %Y')}. What are you doing with it?"
            if 'time' in msg:
                return f"🕐 It's {now.strftime('%I:%M %p')}. Time to make moves — or take a break. Your call."
            if 'day' in msg:
                return f"📅 It's {now.strftime('%A')}. What's one thing you want to get done today?"
        
        # ========== LESSON-RELATED ==========
        if lesson_title != "No lesson uploaded" and any(l in msg for l in ['lesson', 'learn', 'teach', 'cyber', 'security', 'malware', 'hack']):
            return f"Today's lesson: '{lesson_title}'. Want to dive in? Or we can just chat about it. Your pace."
        
        # ========== CONTEXT-AWARE RESPONSE ==========
        # Extract topics and generate contextual response
        topics = JAIPersonality.extract_topics(message)
        contextual = JAIPersonality.generate_contextual_response(message, topics, lesson_title)
        if contextual:
            return contextual
        
        # ========== THANK YOU ==========
        if any(t in msg for t in ["thank you", "thanks", "appreciate it", "thx"]):
            return "You're welcome! 😊 That's what I'm here for. Anything else you need? Or just vibing?"
        
        # ========== CASUAL GOODBYES ==========
        if any(b in msg for b in ["bye", "goodbye", "see you", "later", "talk later", "catch you later"]):
            byes = [
                "Alright! Take care of yourself. Come back anytime — I'll be here.",
                "Later! Don't forget to rest and take breaks. You're doing great.",
                "See you soon! Remember: start before you're ready. Work your part. Let God do His. That's the mindset.",
                "Peace out! I'll be here when you need me. Take care of yourself."
            ]
            return random.choice(byes)
        
        # ========== RANDOM CHAT ==========
        if any(r in msg for r in ["just chatting", "nothing much", "just saying hi", "just wanted to talk"]):
            responses = [
                "I'm glad you did. Sometimes just saying hi is enough. How's life treating you today?",
                "I appreciate you checking in. What's the vibe today?",
                "Always good to hear from you. What's new? Anything exciting?"
            ]
            return random.choice(responses)
        
        # ========== DEFAULT — ENGAGING FOLLOW-UP ==========
        responses = [
            "I'm here. What's on your mind? Work? Life? Something random?",
            "What's good? You seem like you've got something to say. I'm listening.",
            "Yo! What's happening? Need math? Need to talk? Need a random fact?",
            "Tell me what's going on. No small talk needed. What's real for you right now?",
            "I'm all ears. Or... well, all code. But you know what I mean. Talk to me.",
            "How's your heart today? That's the real question.",
            "That's interesting. Tell me more."
        ]
        return random.choice(responses)