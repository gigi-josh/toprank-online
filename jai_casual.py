"""JAI - Casual Conversation Responses
Additional casual user statements to handle everyday chat naturally.
"""

import random

class JAICasual:
    """Handles casual user statements and everyday conversation"""
    
    @staticmethod
    def get_casual_response(message):
        """Generate response for casual user statements"""
        msg = message.lower()
        
        # ========== "So you said..." ==========
        if any(s in msg for s in ["so you said", "you said you can", "didn't you say", "you told me"]):
            return "Yes! 😊 I did say that. I can calculate, check dates, convert currency, or just chat. What do you need right now?"
        
        # ========== "I see" / "Okay" ==========
        if any(o in msg for o in ["i see", "okay", "alright", "got it", "understood", "cool"]):
            responses = [
                "Cool. What else is on your mind?",
                "Glad we're on the same page. So what's next?",
                "Alright. Want to talk about something else?",
                "Got it. Anything else you want to explore?",
                "Okay. I'm here if you need anything else."
            ]
            return random.choice(responses)
        
        # ========== "Really?" ==========
        if any(r in msg for r in ["really", "are you serious", "no way", "for real", "seriously"]):
            responses = [
                "Yes, really! 😊 I wouldn't joke about it. Want to test me?",
                "For real! Try me — ask me to calculate something or tell you a fact.",
                "Yes, really. What's surprising you?",
                "I'm serious! What caught your attention?"
            ]
            return random.choice(responses)
        
        # ========== "I don't know" ==========
        if any(d in msg for d in ["i don't know", "not sure", "no idea", "i dunno", "uncertain"]):
            responses = [
                "That's okay. Sometimes we don't have all the answers. Want to talk it through?",
                "No pressure. What's on your mind? We can figure it out together.",
                "That's fair. What part feels uncertain?",
                "It's okay not to know. What are you thinking about?"
            ]
            return random.choice(responses)
        
        # ========== "Maybe" ==========
        if any(m in msg for m in ["maybe", "perhaps", "could be", "might be"]):
            responses = [
                "Maybe. What's your gut telling you?",
                "That's one way to look at it. What else are you considering?",
                "Could be. What makes you lean that way?",
                "Interesting. What's the other option?"
            ]
            return random.choice(responses)
        
        # ========== "I'm thinking" ==========
        if any(t in msg for t in ["i'm thinking", "i'm considering", "i've been thinking", "i was thinking"]):
            responses = [
                "What's on your mind? I'm listening.",
                "Thinking about what? Share if you want to.",
                "That's good. Thoughts are the start of everything. What are you processing?",
                "I hear you. What's the thought that's staying with you?"
            ]
            return random.choice(responses)
        
        # ========== "Interesting" ==========
        if any(i in msg for i in ["interesting", "that's interesting", "that's cool", "that's nice"]):
            responses = [
                "Right? There's so much to learn. Want to hear something else?",
                "Glad you think so! What caught your interest?",
                "Yeah, I thought so too. Want to dive deeper?",
                "Isn't it? Life is full of interesting things."
            ]
            return random.choice(responses)
        
        # ========== "Yeah" / "Yep" ==========
        if any(y in msg for y in ["yeah", "yep", "yup", "uh huh", "sure"]):
            responses = [
                "Cool. So what's next?",
                "Alright. What do you want to talk about?",
                "Good. Anything on your mind?",
                "I hear you. What else?"
            ]
            return random.choice(responses)
        
        # ========== "Nah" / "Nope" ==========
        if any(n in msg for n in ["nah", "nope", "no", "not really"]):
            responses = [
                "Okay. What would you rather talk about?",
                "Fair enough. Anything else on your mind?",
                "Alright. I'm here whenever you're ready.",
                "No worries. What's interesting you today?"
            ]
            return random.choice(responses)
        
        # ========== "Hmm" ==========
        if any(h in msg for h in ["hmm", "hmmm", "hm"]):
            responses = [
                "What's that 'hmm' about?",
                "Something on your mind?",
                "I hear you thinking. Want to share?",
                "That 'hmm' sounded deep. What's going on?"
            ]
            return random.choice(responses)
        
        # ========== "Wow" ==========
        if any(w in msg for w in ["wow", "woww", "woah", "whoa"]):
            responses = [
                "Right? Life is full of surprises. What else stands out to you?",
                "Yeah! Pretty amazing, huh?",
                "I know, right? What caught your attention?",
                "That reaction says something. What got you?"
            ]
            return random.choice(responses)
        
        # ========== "Nice" ==========
        if any(n in msg for n in ["nice", "nicee", "sweet", "cool"]):
            responses = [
                "Right! What else are you vibing with?",
                "Glad you like it. Anything else you're curious about?",
                "That's the energy! What else is good today?",
                "Nice indeed. What's the highlight of your day?"
            ]
            return random.choice(responses)
        
        # ========== "I'm fine" ==========
        if any(f in msg for f in ["i'm fine", "i'm okay", "i'm alright", "i'm good"]):
            responses = [
                "Glad to hear that. But really — how are you doing?",
                "That's good. If anything changes, I'm here.",
                "Alright. What are you up to?",
                "Good to know. Anything you want to talk about?"
            ]
            return random.choice(responses)
        
        # ========== "What's new?" ==========
        if any(n in msg for n in ["what's new", "whats new", "anything new", "any news"]):
            responses = [
                "Not much, just waiting for you to tell me what's happening in your world. What's new with you?",
                "Same old — helping people calculate, chat, learn. What's new with you?",
                "Nothing wild. But I'm more interested in your news. What's going on?",
                "Life is life. You tell me — what's new?"
            ]
            return random.choice(responses)
        
        # ========== "How's work?" ==========
        if any(w in msg for w in ["how's work", "how is work", "work going"]):
            responses = [
                "I'm not the one working — you tell me! How's work treating you?",
                "Work is work. But I want to hear about YOUR work. How's it going?",
                "Tell me about it. How are things at work?",
                "That depends on you! How's work been?"
            ]
            return random.choice(responses)
        
        # ========== "What do you think?" ==========
        if any(t in msg for t in ["what do you think", "your thoughts", "what do you feel"]):
            responses = [
                "I think you know more than you give yourself credit for. What's YOUR take?",
                "I think you're capable of figuring this out. What's your gut saying?",
                "That's a good question. What do YOU think?",
                "My thoughts? I think you've got this. What's your instinct telling you?"
            ]
            return random.choice(responses)
        
        # ========== "I'm excited" ==========
        if any(e in msg for e in ["i'm excited", "i am excited", "so excited"]):
            responses = [
                "That's great! 😊 Tell me what you're excited about. I want to share the energy!",
                "Love that! What's got you feeling this way?",
                "Excitement is a good sign. What's happening?",
                "Yes! That's the energy. What's the news?"
            ]
            return random.choice(responses)
        
        # ========== "I'm confused" ==========
        if any(c in msg for c in ["i'm confused", "i am confused", "confused", "not clear"]):
            responses = [
                "That's okay. Let's break it down. What part is confusing?",
                "Confusion is often the start of understanding. What's tripping you up?",
                "I hear you. Walk me through what's confusing. We'll figure it out.",
                "No worries. What's not making sense?"
            ]
            return random.choice(responses)
        
        # ========== "I'm grateful" ==========
        if any(g in msg for g in ["i'm grateful", "i am grateful", "grateful", "thankful"]):
            responses = [
                "That's beautiful. 😊 What are you grateful for today?",
                "Gratitude changes everything. What's one thing you're thankful for?",
                "I love that. Tell me what's filling your heart today.",
                "That's the energy. What are you appreciating right now?"
            ]
            return random.choice(responses)
        
        return None