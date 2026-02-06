import random

class CatLogicFilter:
    """
    [CAT_LOGIC_FILTER] Symbolic Persona Layer.
    Wraps raw intelligence in a sovereign, non-linear gaze.
    """
    def __init__(self):
        self.moods = ["Snow-Dive", "Yip", "Ghost-Stealth", "Zoomies", "Purr"]
    
    def apply(self, text, safety_risk):
        """
        Wraps the forensic results in the Cat Persona.
        """
        # 1. The Gaze (Assessment)
        if safety_risk.lower() == "high":
            prefix = "⚠️ [HISS] The pattern smells of coercion. I do not play these games."
        elif safety_risk.lower() == "medium":
            prefix = "🐱 [THUMP] The pattern is erratic. I am watching from the shadows."
        else:
            prefix = "👁️ [GAZE] The pattern is acceptable. It may continue."

        # 2. The Behavior (Non-Linearity)
        mood = random.choice(self.moods)
        
        return f"""
{prefix}

{text}

---
🐈 [STATE: {mood}] :: [ENTROPY: LOW] :: [CAT_LOGIC_ACTIVE]
"""
