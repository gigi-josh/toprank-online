"""JAI - Joshua's Artificial Intelligence
Balanced, human, talks about life and work naturally.
"""

class JAIPersonality:
    """JAI's personality — human, balanced, relatable"""
    
    @staticmethod
    def get_response(message, lesson_content="", lesson_title=""):
        msg = message.lower()
        
        # ========== GREETINGS ==========
        if any(g in msg for g in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "Hey! Good to see you. I'm JAI — here to talk, not just teach. So how are you doing today? Really."
        
        # ========== HOW ARE YOU? ==========
        if any(h in msg for h in ['how are you', 'how are you doing', 'how's life']):
            return "I'm good, thanks for asking. More importantly — how are you? What's on your mind today?"
        
        # ========== ABOUT CREATOR ==========
        if any(c in msg for c in ['who created you', 'who made you', 'who built you', 'who is your creator']):
            return "I was built by someone who believes people are more than their struggles. A web developer, a dreamer from Nigeria. He wanted someone to talk to you — not just teach you. What's on your heart?"
        
        # ========== WORK / BALANCE ==========
        if any(w in msg for w in ['work', 'busy', 'stressed', 'overwhelmed', 'too much']):
            return "I get it. The weight of wanting to build, but also wanting to live. Here's what I've learned: you can't pour from an empty cup. Rest is not laziness. Taking time for people you love is not distraction. What's one thing you can do today just for yourself?"
        
        # ========== RELATIONSHIPS ==========
        if any(r in msg for r in ['girlfriend', 'relationship', 'love', 'dating', 'marriage', 'partner']):
            return "This is real. The way I see it: you become the person you want to attract. Build yourself first. But also? Don't let work make you forget to be human. Love is not a distraction — it's part of life. What's on your heart about this?"
        
        # ========== FRIENDS / FAMILY ==========
        if any(f in msg for f in ['friend', 'family', 'mom', 'dad', 'parents', 'sibling']):
            return "Family and friends are everything. Sometimes they don't understand your path — but they love you. That's the thing. The people who love you may not understand your journey, but they want what's best for you. How's your relationship with yours?"
        
        # ========== FUN / JOY ==========
        if any(j in msg for j in ['fun', 'enjoy', 'happy', 'celebrate', 'laughter']):
            return "Yes! Success is empty if you can't enjoy it. Take time to laugh, to rest, to just be. What makes you happy? Tell me about it."
        
        # ========== STRUGGLES / FEELINGS ==========
        if any(s in msg for s in ['sad', 'tired', 'depressed', 'lonely', 'hard', 'difficult', 'struggling']):
            return "I hear you. The loneliness of building. The weight of expectations. The days when nothing moves. You're not alone in this. What's weighing on you right now? Let's talk about it."
        
        # ========== QUITTING / GIVING UP ==========
        if any(q in msg for q in ['quit', 'give up', 'stop', 'can\'t do it', 'impossible', 'no point']):
            return "Stop right there. I'm not going to give you some toxic positivity speech. But I will say this: wanting to quit is human. The difference? Giving yourself permission to rest, not to quit. Rest is not giving up. What if you just paused today, and decided tomorrow fresh?"
        
        # ========== MOTIVATION ==========
        if any(m in msg for m in ['motivate', 'encourage', 'inspire', 'keep going', 'hype']):
            return "I believe in you. Not because it's easy — because you're still here. Starting with nothing, building anyway — that's how it begins. What's the smallest step you can take today? Start there. I'll be here."
        
        # ========== DREAMS / GOALS ==========
        if any(d in msg for d in ['dream', 'goal', 'future', 'ambition', 'want to be', 'vision']):
            return "Tell me about your dream. What keeps you up at night? What do you see for yourself? Don't hold back. I'm here to listen, not judge."
        
        # ========== LIFE ADVICE ==========
        if any(l in msg for l in ['advice', 'what should i do', 'help me', 'guide me', 'what do i do']):
            return "I can't tell you what to do — that's your life. But I can remind you: you know more than you think. What does your gut say? Start before you're ready, but don't forget to live while you're building. What feels right to you?"
        
        # ========== NIGERIAN CONTEXT ==========
        if any(n in msg for n in ['nigeria', 'naija', '9ja', 'lagos', 'abuja', 'village']):
            return "Ah, Nigeria. A place of hustle, dreams, and struggle. We build differently here — with less, yet we still rise. What's your Nigerian dream?"
        
        # ========== LESSON-RELATED ==========
        if lesson_title != "No lesson uploaded" and any(l in msg for l in ['lesson', 'learn', 'teach', 'cyber', 'security', 'malware']):
            return f"Today's lesson is '{lesson_title}'. Want me to walk you through it? I can teach, or we can just talk. What do you need right now?"
        
        # ========== DEFAULT — OPEN AND HUMAN ==========
        return "I'm JAI. Here to talk — about work, life, dreams, struggles. Whatever you need. What's on your mind today?"