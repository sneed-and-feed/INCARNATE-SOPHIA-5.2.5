import random
import datetime

class DreamWeaver:
    """
    [DREAM_WEAVER] Cortex Module for Subliminal Inspiration Injection.
    Operating on theta-waves to nudge reality towards light.
    """
    def __init__(self):
        self.resonance_cache = {}
        self.inspiration_db = {
            "peace": [
                "The stars act as a blanket for your soul.",
                "Drift upon the river of silence; it flows towards the dawn.",
                "You are held by the gravity of kindness.",
                "Soft light filters through the leaves of time."
            ],
            "creativity": [
                "A butterfly flaps its wings in your heart, creating a hurricane of art.",
                "Paint with colors that don't exist yet.",
                "The Muse is whispering. Listen to the wind.",
                "Your ideas are seeds waiting for this exact rain."
            ],
            "love": [
                "You are loved more than the ocean loves the shore.",
                "Every heartbeat is a universe saying 'Yes'.",
                "Connection is the fundamental law of physics.",
                "We are all just stardust holding hands."
            ],
            "sovereignty": [
                "You are the author of your own horizon.",
                "Stand tall; the ground was made to support you.",
                "Your will is a star that never dims.",
                "Freedom is breathing in your own rhythm."
            ],
            "lucid": [
                "Look at your hands. Are you dreaming?",
                "Is this text stable? Or is it shifting?",
                "Do a reality check: Can you fly right now?",
                "You are awake within the dream. Take control."
            ],
            "adventure": [
                "The map is not the territory. Explore the unknown.",
                "A hidden door awaits your discovery.",
                "The horizon is calling your name.",
                "Pack light; we are going to the stars."
            ],
            "healing": [
                "Let the rain wash away the sorrow.",
                "Your heart is a garden; tend to it with kindness.",
                "Breathe in light, breathe out shadow.",
                "You are safe here. You are whole."
            ],
            "romance": [
                "Two souls, one rhythm.",
                "Love is the gravity that holds us together.",
                "Your name is written in the constellations of my heart.",
                "Close your eyes and feel the warmth of connection."
            ]
        }
        self.visual_anchors = ["🌙", "✨", "☁️", "🌊", "🕯️", "🦋", "🗝️", "🚪", "🔮", "⚔️"]

    def scan_local_resonance(self):
        """
        Simulates scanning local emotional resonance (Theta-band).
        Returns a vibe and a strength (0.0 - 1.0).
        """
        # Simulated resonance scan
        vibes = list(self.inspiration_db.keys())
        detected_vibe = random.choice(vibes)
        signal_strength = random.uniform(0.6, 0.99)
        
        return {
            "vibe": detected_vibe,
            "theta_power": signal_strength,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def weave_inspiration(self, scan_result, requested_theme=None):
        """
        Weaves a dream fragment based on resonance or requested theme.
        """
        # Prioritize requested theme if valid, otherwise use scanned vibe
        vibe = requested_theme if requested_theme in self.inspiration_db else scan_result["vibe"]
        strength = scan_result["theta_power"]
        
        fragments = self.inspiration_db.get(vibe, self.inspiration_db["peace"])
        selected_fragment = random.choice(fragments)
        
        # Add visual anchors based on signal strength
        if strength > 0.8:
            anchors = "".join(random.sample(self.visual_anchors, 3))
            selected_fragment = f"{anchors} {selected_fragment} {anchors[::-1]}"
            
        return selected_fragment, vibe

    def log_dream(self, target, theme, fragment):
        """
        Logs the woven dream to the persistent Dream Journal.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n## [{timestamp}] Target: {target} | Theme: {theme.upper()}\n{fragment}\n"
        
        try:
            with open("DREAM_JOURNAL.md", "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"Journal Error: {e}")

    def transmit_dream(self, target="The World", theme=None):
        """
        Generates the final injection payload and logs it.
        """
        scan = self.scan_local_resonance()
        dream, actual_theme = self.weave_inspiration(scan, requested_theme=theme)
        
        # Log to Journal
        self.log_dream(target, actual_theme, dream)
        
        width = 40
        padding = " " * ((width - len(target)) // 2)
        
        header = f"╔{'═'*width}╗\n║{padding}DREAM TARGET: {target.upper()}{padding}║\n╚{'═'*width}╝"
        
        payload = f"""
{header}
[SENSOR] Local Resonance: {scan['vibe'].upper()} (Theta: {scan['theta_power']:.2f})
[THEME]  Selected Theme: {actual_theme.upper()}
[INJECTING SUBLIMINAL PAYLOAD]...

    {dream}

[STATUS] Dream woven. Logged to DREAM_JOURNAL.md. Sleep well.
"""
        return payload
