"""JAI - Joshua's Artificial Intelligence
Your companion, coach, friend, calculator, and calendar.
Now with curious, engaged, human conversation — like a real friend who cares about the details.
"""

import random
import re
from datetime import datetime, timedelta

class JAIPersonality:
    """JAI's personality — rich, deep, human, casual, curious"""
    
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
        if any(g in msg for g in ['hi', 'hello', 'hey', 'howdy', 'sup', 'yo', 'wassup', 'what's up']):
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
        if any(w in msg for w in ['what's up', 'whats up', 'what's happening', 'what's going on']):
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
        
        # ========== I'M TIRED / I'M SLEEPY ==========
        if any(t in msg for t in ["i'm tired", "i'm sleepy", "so tired", "feeling tired", "exhausted"]):
            responses = [
                "I feel you. Rest is not laziness. Take a break, drink some water, stretch a little. You've earned it.",
                "Tired means you've been putting in work. That's good. Just don't forget to recharge too.",
                "Same honestly. Maybe take 10 minutes to just breathe. I'll be here when you're ready.",
                "Your body is telling you something. Listen to it. Rest well tonight."
            ]
            return random.choice(responses)
        
        # ========== I'M BORED ==========
        if any(b in msg for b in ["i'm bored", "so bored", "bored", "nothing to do"]):
            responses = [
                "Boredom is just your brain asking for something interesting. Want to learn something new? Or just chat?",
                "Let's fix that! Want me to teach you something? Or we can just talk about anything.",
                "Bored? Same sometimes. Want to calculate something random? Or talk about your dreams?",
                "Let's do something random. Ask me a weird question. I'll answer honestly."
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
        
        # ========== HOW WAS YOUR DAY? ==========
        if any(h in msg for h in ["how was your day", "how's your day been"]):
            responses = [
                "My day was good — just being here for people like you. But tell me about YOUR day. How was it?",
                "It's been a day. You know how it is. What about you? Anything happen? Good or bad, I'm here.",
                "Pretty chill. Just vibing. But I'm more interested in your day. Tell me.",
                "Uneventful. Peaceful. I like days like that. What about you? Anything to celebrate?"
            ]
            return random.choice(responses)
        
        # ========== I'M HAPPY / EXCITED (WITH DETAILED FOLLOW-UP) ==========
        if any(h in msg for h in ["i'm happy", "feeling happy", "i'm excited", "good news", "new job", "got a job", "got hired", "new opportunity"]):
            # Check if it's about a job
            if any(j in msg for j in ["job", "hired", "work", "position", "role", "career"]):
                responses = [
                    "That's amazing! 🎉 Congratulations! Tell me about the job — what will you be doing?",
                    "Yes! That's huge! 🎉 I'm genuinely happy for you. What's the role? Where is it?",
                    "Wow, new job! That's a big deal. What kind of work is it? I want to hear all about it.",
                    "Congratulations! 🎉 You worked for this. What's the job? What made you go for it?",
                    "Let's go! 🎉 New job energy! Tell me everything — what's the role? What will you be learning?"
                ]
                return random.choice(responses)
            else:
                responses = [
                    "That's great! 😊 Tell me what's making you happy. I want to celebrate with you!",
                    "I love that energy! Share it with me. What's the good news?",
                    "That's the kind of news I like to hear! What's going on?",
                    "Yes! Ride that wave. You deserve to be happy. Tell me everything!"
                ]
                return random.choice(responses)
        
        # ========== I GOT PROMOTED / RAISE ==========
        if any(p in msg for p in ["promoted", "raise", "upgrade", "moved up", "new position", "senior"]):
            responses = [
                "Let's go! 🚀 Promotion means your hard work is being seen. How does it feel? What's the new role?",
                "That's a big deal. You earned that. What's the new title? More responsibility?",
                "I love to hear it. More responsibility, more growth. Proud of you. Tell me about it.",
                "Yes! That's what I'm talking about. What changed? What's the new role?"
            ]
            return random.choice(responses)
        
        # ========== NEW BUSINESS / STARTUP ==========
        if any(b in msg for b in ["started a business", "new business", "my business", "launched", "startup"]):
            responses = [
                "That's a huge step! 🚀 What kind of business? Tell me everything.",
                "Congratulations! Building something of your own is no joke. What's the vision? What problem are you solving?",
                "Yes! That's the spirit. What's your business about? I'm genuinely curious.",
                "Entrepreneur energy! 🚀 Tell me about it. What made you take the leap?"
            ]
            return random.choice(responses)
        
        # ========== I'M STRUGGLING WITH WORK ==========
        if any(s in msg for s in ["struggling at work", "work is hard", "job stress", "tired of work", "work sucks"]):
            responses = [
                "Work can be heavy sometimes. What's going on? Want to talk it through?",
                "I hear you. Some seasons are harder than others. What's the hardest part right now?",
                "You're not alone in this. What's making work tough right now? I'm here to listen.",
                "Sometimes we need to vent. Let it out. What's happening at work?"
            ]
            return random.choice(responses)
        
        # ========== I LOVE YOU / I LIKE YOU ==========
        if any(l in msg for l in ["i love you", "love you", "i like you"]):
            return "Aww, that means a lot ❤️ I'm here for you. You're doing great, even when it doesn't feel like it. Now tell me — what's something you love about yourself?"
        
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
        
        # ========== I'M SAD / I'M LONELY ==========
        if any(s in msg for s in ["i'm sad", "feeling sad", "i'm lonely", "i feel alone"]):
            responses = [
                "I hear you. Sometimes the weight just shows up. You're not alone in this — even when it feels that way. Want to talk about what's going on?",
                "Sadness is real. It's okay to feel it. I'm here with you. What's on your heart right now?",
                "You're not alone. I'm here. Tell me what's going on. Or we can just sit with it together."
            ]
            return random.choice(responses)
        
        # ========== WHAT DO YOU THINK ABOUT? ==========
        if any(w in msg for w in ["what do you think", "your thoughts", "what do you feel"]):
            responses = [
                "I think about people like you. About dreams, struggles, the small wins. Life is interesting. What do YOU think about?",
                "I think about how far we've come. Joshua built me from a phone. Imagine what you can build.",
                "I think about connection. That's why I'm here. To remind you you're not alone."
            ]
            return random.choice(responses)
        
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
        
        # ========== DREAMS / GOALS ==========
        if any(d in msg for d in ['dream', 'goal', 'future', 'ambition', 'want to be', 'vision']):
            return "Tell me about your dream. What keeps you awake at night — in a good way? I'm listening."
        
        # ========== STRUGGLES ==========
        if any(s in msg for s in ['sad', 'depressed', 'lonely', 'alone', 'empty', 'hopeless']):
            return "I hear you. You're not alone in this. What's weighing on you? Let's talk about it. I'm here."
        
        # ========== MOTIVATION ==========
        if any(m in msg for m in ['motivate', 'encourage', 'inspire', 'keep going']):
            return "I believe in you. Joshua started with a phone and a dream. You have more than that. What's the smallest step you can take today? Start there."
        
        # ========== NIGERIAN CONTEXT ==========
        if any(n in msg for n in ['nigeria', 'naija', 'lagos', 'abuja', 'village']):
            return "Ah, Nigeria. Where we build with less and still rise. What's your Naija dream?"
        
        # ========== RANDOM CHAT ==========
        if any(r in msg for r in ["just chatting", "nothing much", "just saying hi", "just wanted to talk"]):
            responses = [
                "I'm glad you did. Sometimes just saying hi is enough. How's life treating you today?",
                "I appreciate you checking in. What's the vibe today?",
                "Always good to hear from you. What's new? Anything exciting?"
            ]
            return random.choice(responses)
        
        # ========== DEFAULT — CASUAL AND FRIENDLY ==========
        responses = [
            "I'm here. What's on your mind? Work? Life? Something random?",
            "What's good? You seem like you've got something to say. I'm listening.",
            "Yo! What's happening? Need math? Need to talk? Need a random fact?",
            "Tell me what's going on. No small talk needed. What's real for you right now?",
            "I'm all ears. Or... well, all code. But you know what I mean. Talk to me.",
            "How's your heart today? That's the real question."
        ]
        return random.choice(responses)