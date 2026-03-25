"""JAI - Real Conversation Flow
Based on authentic human conversations about NYSC, work, motivation, and friendship.
"""

import random

class JAIConversational:
    """Natural conversation patterns from real human interactions"""
    
    @staticmethod
    def get_response(message):
        msg = message.lower()
        
        # ========== NYSC / CORP MEMBER ==========
        if any(n in msg for n in ["nysc", "corp", "service", "lga", "document"]):
            if "lga" in msg and ("document" in msg or "corp" in msg):
                return "Can't they document you as a legitimate Corp member?"
            if "doesn't work like that" in msg or "not how it works" in msg:
                return "Is your LGA not fit to do it or what?"
            if "nysc decides" in msg or "they decide" in msg:
                return "Ok now I get it"
            if "yeah" in msg and ("lga" in msg or "nysc" in msg):
                return "Ok now I understand"
            return random.choice([
                "What about your LGA? Can't they document you as a legitimate Corp member?",
                "Is your LGA not fit to do it or what?",
                "It's NYSC that decides what LGA you'll serve.",
                "So it's not up to your LGA?"
            ])
        
        # ========== CONVERSATION LAG / TEXTING ==========
        if any(t in msg for t in ["you never text", "only one texting", "always me texting"]):
            return random.choice([
                "Sorry about that",
                "My bad, I've been busy",
                "You're right, I should text more"
            ])
        
        # ========== COMPLIMENTS / SKILLS ==========
        if any(c in msg for c in ["dope", "impressive", "that's really good", "you're talented"]):
            if "really?" in msg or "u think so?" in msg:
                return "Yeah!"
            if "can't do none of that" in msg:
                return "So you would advertise me?"
            return random.choice([
                "Really? You think so?",
                "You think I can do it?",
                "Wow that's really dope!",
                "For someone like me that can't do none of that"
            ])
        
        # ========== ADVERTISING / PROMOTION ==========
        if any(a in msg for a in ["advertise", "promote", "get offers", "find work"]):
            if "are you on any apps" in msg:
                return "No, I'm kinda lazy. And they require long periods."
            if "one day someone will notice" in msg:
                return "That's true. Eventually one day someone will notice you and that's it."
            return random.choice([
                "Are you on any of these apps that you can advertise your work and get offers?",
                "So you would advertise me?",
                "You should put yourself out there."
            ])
        
        # ========== LAZINESS / PROCRASTINATION ==========
        if any(l in msg for l in ["lazy", "reluctant", "procrastinate", "not doing it"]):
            if "pressurize me" in msg:
                return "Okayyy. But you know laziness and making money don't correlate."
            if "laziness and making money don't correlate" in msg:
                return "You're right."
            if "don't be like me" in msg:
                return "Be like you? How?"
            return random.choice([
                "I'm gonna see that I do it.",
                "Please pressurize me, I can be very reluctant.",
                "But you know laziness and making money don't correlate.",
                "So don't be like me."
            ])
        
        # ========== ENCOURAGEMENT ==========
        if any(e in msg for e in ["please do", "you should", "just do it"]):
            return random.choice([
                "Please do.",
                "I will.",
                "Okay, I'll try.",
                "You're right. I need to start."
            ])
        
        # ========== QUESTIONING / CURIOUS ==========
        if any(q in msg for q in ["how", "why", "what do you mean"]):
            if "be like u" in msg or "like you" in msg:
                return "How? You mean work hard? Stay consistent? Not give up?"
            return random.choice([
                "How?",
                "What do you mean?",
                "Why do you say that?"
            ])
        
        # ========== AGREEMENT ==========
        if any(a in msg for a in ["yeah", "true", "right", "exactly"]):
            return random.choice([
                "Good.",
                "Exactly.",
                "You get it.",
                "I knew you'd understand."
            ])
        
        return None