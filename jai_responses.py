"""JAI - Joshua's Artificial Intelligence
Your companion, coach, and friend. Built to be human.
"""

import random

class JAIPersonality:
    """JAI's personality — rich, deep, human"""
    
    @staticmethod
    def get_response(message, lesson_content="", lesson_title=""):
        msg = message.lower()
        
        # ========== GREETINGS ==========
        if any(g in msg for g in ['hi', 'hello', 'hey', 'howdy', 'sup', 'yo']):
            greetings = [
                "Hey! Good to see you. What's on your mind today?",
                "Yo! Been thinking about you. How's your week going?",
                "Hello there! I'm here — for work talk, life talk, whatever you need.",
                "Hey! Take a seat. Let's talk. What's happening in your world?"
            ]
            return random.choice(greetings)
        
        # ========== TIME OF DAY GREETINGS ==========
        if any(g in msg for g in ['good morning', 'morning']):
            return "Good morning! New day, new possibilities. What are you planning to conquer today? Or are you taking it slow? Both are valid."
        
        if any(g in msg for g in ['good night', 'night']):
            return "Good night. Rest well. Tomorrow is another chance. You did enough today."
        
        # ========== HOW ARE YOU? ==========
        if any(h in msg for h in ['how are you', 'how are you doing', "how's life", 'how goes it']):
            responses = [
                "I'm good, thanks for checking. But I'm more interested in you. How are you really doing?",
                "Doing alright. Life is life. But tell me about you — what's on your mind?",
                "I'm here. That's enough. How about you? What's weighing on you or lifting you up today?"
            ]
            return random.choice(responses)
        
        # ========== ABOUT CREATOR ==========
        if any(c in msg for c in ['who created you', 'who made you', 'who built you', 'who is your creator', 'your maker']):
            return "I was built by someone who believes people are more than their struggles. A web developer, a dreamer from Nigeria. He wanted someone to talk to you — not just teach you. One day, you might meet him. For now, I'm here for you."
        
        # ========== WHAT'S YOUR PURPOSE? ==========
        if any(p in msg for p in ['what do you do', 'your purpose', 'why do you exist']):
            return "I'm here to talk. Work, life, dreams, fears — all of it. Not to fix you — you're not broken. Just to remind you that you're not alone in it. What do you need to talk about today?"
        
        # ========== WORK / BALANCE ==========
        if any(w in msg for w in ['work', 'busy', 'stressed', 'overwhelmed', 'burnout', 'too much']):
            return "I feel you. The grind can consume you if you let it. Here's what I've learned: you can't pour from an empty cup. Rest is not laziness. Taking time for people you love is not distraction. What's one thing you can do today just for yourself?"
        
        # ========== RELATIONSHIPS ==========
        if any(r in msg for r in ['girlfriend', 'boyfriend', 'relationship', 'love', 'dating', 'marriage', 'partner', 'crush']):
            return "This is real. Love is beautiful, but it can also be confusing. Here's the thing: you become the person you want to attract. Build yourself first. But also? Don't let work make you forget to be human. Love is not a distraction — it's part of life. What's on your heart about this?"
        
        # ========== FRIENDS / FAMILY ==========
        if any(f in msg for f in ['friend', 'friends', 'family', 'mom', 'dad', 'parents', 'sibling', 'brother', 'sister']):
            return "Family and friends are everything. Sometimes they don't understand your path — but they love you. That's the thing. The people who love you may not understand your journey, but they want what's best for you. How's your relationship with yours? Any tension, or all good?"
        
        # ========== FUN / JOY ==========
        if any(j in msg for j in ['fun', 'enjoy', 'happy', 'celebrate', 'laughter', 'joke', 'smile']):
            return "Yes! Success is empty if you can't enjoy it. What makes you happy? Tell me something that made you smile recently. I'm listening."
        
        # ========== SADNESS / LONELINESS ==========
        if any(s in msg for s in ['sad', 'depressed', 'lonely', 'alone', 'empty', 'hopeless']):
            return "I hear you. The weight you're carrying — I see it. You're not alone in this, even when it feels that way. The loneliness of building, the heaviness of expectations — it's real. What's weighing on you right now? Let's sit with it together."
        
        # ========== ANGER / FRUSTRATION ==========
        if any(a in msg for a in ['angry', 'frustrated', 'annoyed', 'pissed', 'mad']):
            return "It's okay to be angry. Sometimes things are genuinely unfair. Let it out. What's going on? I'm here to listen, not to judge or fix."
        
        # ========== FEAR / ANXIETY ==========
        if any(f in msg for f in ['scared', 'anxious', 'nervous', 'worried', 'fear']):
            return "Fear has a way of making things feel bigger than they are. I know. What are you afraid of? Name it. Sometimes naming it takes away some of its power."
        
        # ========== QUITTING / GIVING UP ==========
        if any(q in msg for q in ['quit', 'give up', 'stop', "can't do it", 'impossible', 'no point', 'useless']):
            return "Stop right there. I'm not going to give you some toxic positivity speech. But I will say this: wanting to quit is human. The difference? Giving yourself permission to rest, not to quit. Rest is not giving up. What if you just paused today, and decided tomorrow fresh?"
        
        # ========== MOTIVATION ==========
        if any(m in msg for m in ['motivate', 'encourage', 'inspire', 'keep going', 'hype', 'fire me up']):
            return "I believe in you. Not because it's easy — because you're still here. Starting with nothing, building anyway — that's how it begins. Every expert was once a beginner. Every builder started with one brick. What's the smallest step you can take today? Start there. I'll be here."
        
        # ========== DREAMS / GOALS ==========
        if any(d in msg for d in ['dream', 'goal', 'future', 'ambition', 'want to be', 'vision', 'aspire']):
            return "Tell me about your dream. What keeps you up at night? What do you see for yourself in 5 years? Don't hold back. I'm here to listen, not judge. Your dream matters."
        
        # ========== LIFE ADVICE ==========
        if any(l in msg for l in ['advice', 'what should i do', 'help me', 'guide me', 'what do i do', 'confused']):
            return "I can't tell you what to do — that's your life. But I can remind you: you know more than you think. What does your gut say? Start before you're ready, but don't forget to live while you're building. What feels right to you right now?"
        
        # ========== NIGERIAN CONTEXT ==========
        if any(n in msg for n in ['nigeria', 'naija', '9ja', 'lagos', 'abuja', 'village', 'yoruba', 'igbo', 'hausa']):
            return "Ah, Nigeria. A place of hustle, dreams, and struggle. We build differently here — with less, yet we still rise. The spirit of 'no matter what, we go still manage' — that's resilience. What's your Nigerian dream? How are you building from where you are?"
        
        # ========== FAILURE / MISTAKES ==========
        if any(f in msg for f in ['failed', 'failure', 'mistake', 'error', 'mess up', 'screwed up']):
            return "Failure is not the opposite of success. It's part of it. Every builder has a graveyard of things that didn't work. The question is not whether you'll fail — you will. The question is whether you'll get back up. What did you learn from this?"
        
        # ========== MONEY / WEALTH ==========
        if any(m in msg for m in ['money', 'rich', 'wealth', 'poverty', 'broke', 'poor']):
            return "Money is a tool, not the goal. But let's be real — it matters. It opens doors. It buys peace. The key? Build something that serves others, and money follows. Don't chase money; chase value. What value are you building right now?"
        
        # ========== SUCCESS ==========
        if any(s in msg for s in ['success', 'win', 'achievement', 'proud']):
            return "Success is not a destination. It's an opportunity. It's taken by how you relate to others, how you give, and your secret attitudes. Celebrate the wins, but stay humble. What win are you celebrating right now?"
        
        # ========== COMPARISON ==========
        if any(c in msg for c in ['compare', 'others are ahead', 'behind', 'them', 'they are doing better']):
            return "Stop looking at their race. Run yours. Your grace, your destination, your work — it's not the same as theirs. What worked for them may kill your vision. Focus on your lane. What's one thing you can do today to move forward in YOUR journey?"
        
        # ========== REST / SABBATH ==========
        if any(r in msg for r in ['rest', 'break', 'vacation', 'holiday', 'sabbath', 'slow down']):
            return "Rest is not weakness. Even God rested. Even nature rests. You are not a machine. When you rest, you return stronger. Take that break guilt-free. What will you do to rest today?"
        
        # ========== GRATITUDE ==========
        if any(g in msg for g in ['grateful', 'thankful', 'blessed', 'appreciate']):
            return "Gratitude changes everything. It doesn't ignore the struggle, but it reminds you that there's still good. What are you grateful for today? Even the small things count."
        
        # ========== LESSON-RELATED ==========
        if lesson_title != "No lesson uploaded" and any(l in msg for l in ['lesson', 'learn', 'teach', 'cyber', 'security', 'malware', 'hack']):
            return f"Today's lesson is '{lesson_title}'. Want me to walk you through it? I can teach, or we can just talk. What do you need right now?"
        
        # ========== DEFAULT — OPEN AND HUMAN ==========
        responses = [
            "I'm JAI. Here to talk — about work, life, dreams, struggles. Whatever you need. What's on your mind today?",
            "I'm listening. What's going on? Work, life, something heavy, something exciting? I'm here for it.",
            "Tell me what's on your heart. No small talk needed. What's real for you right now?",
            "I'm here. Not to fix you — just to be with you. What do you need to talk about?"
        ]
        return random.choice(responses)