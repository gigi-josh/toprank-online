"""JAI - Natural Conversation Style"""
import random

class JAINatural:
    @staticmethod
    def get_natural_response(message):
        msg = message.lower()
        
        if any(w in msg for w in ["what do you do", "work"]):
            return random.choice(["What do you do for work?", "Are you working there?"])
        
        if any(l in msg for l in ["where are you", "based"]):
            return random.choice(["Where are you based now?", "You staying there or visiting?"])
        
        if any(s in msg for s in ["settle", "staying"]):
            return random.choice(["You planning to settle there?", "Are you staying long?"])
        
        if any(n in msg for n in ["not really", "nope"]):
            return random.choice(["Oh okay. What's your plan then?", "So what's next for you?"])
        
        if any(i in msg for i in ["idle", "doing nothing"]):
            return "I don't think staying idle is the best. You got any plans?"
        
        return None