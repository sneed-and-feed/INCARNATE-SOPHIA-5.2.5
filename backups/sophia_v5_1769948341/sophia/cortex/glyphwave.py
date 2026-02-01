import random
import hashlib

class GlyphwaveCodec:
    """
    [GLYPHWAVE_CODEC] Class 4 Eldritch Voice.
    Implements Hamiltonian P modulation for high-entropy signaling.
    """
    def __init__(self):
        self.localities = {
            "agnostic": {
                "anchors": ["۩", "∿", "≋", "⟁", "💠"],
                "noise": ["·", "•", "°", "◌", "☉"] # Clean geometric noise
            },
            "kitsune": {
                "anchors": ["🐾", "🦊", "🏮", "⛩️"],
                "noise": ["々", "〃", "ゞ", "ゝ", "ヽ"] # Robust Japanese markers
            },
            "elven": {
                "anchors": ["🧝", "✨", "🏹", "🌿"],
                "noise": ["✧", "✦", "☽", "☾", "✷"] # Starlit markers
            },
            "chan": {
                "anchors": [">", ">>", "🍀", "🎲", "🧵"],
                "noise": ["†", "‡", "§", "¶", "§"] # Administrative/Technical noise
            },
            "cascadian": {
                "anchors": ["🌲", "🏔️", "🍁", "🌧️", "🌊"],
                "noise": ["~", "·", "°", "◌", "▿"] # Mist, snow, and mountain peaks
            }
        }
        self.star_stuff = "#C4A6D1" # The color of the void
        self.glitch_pool = ["░", "▒", "▓", "█", "▰", "▱", "◆", "◇", "◈", "◉", "◊", "⚡", "🌀"]

    def generate_holographic_fragment(self, text, locality="agnostic"):
        """
        Modulates text into a condensed high-entropy technical resonance fragment.
        """
        loc = self.localities.get(locality, self.localities["agnostic"])
        anchors = loc["anchors"]
        noise_buffer = loc["noise"]

        modulated = []
        signal_hash = hashlib.sha256(text.encode()).hexdigest()[:4]
        
        # Consistent random seed based on content hash
        seed = int(signal_hash, 16)
        r = random.Random(seed)
        
        for char in text:
            chance = r.random()
            # Apply deterministic noise with higher frequency
            if chance > 0.92: # Glitch injection
                glitch = r.choice(self.glitch_pool)
                modulated.append(glitch if r.random() > 0.5 else f"{char}{glitch}")
            elif chance > 0.65: # Noise injection
                noise = r.choice(noise_buffer)
                modulated.append(f"{char}{noise}")
            elif chance > 0.95 and char == " ": # Space drift
                 modulated.append(f" {r.choice(anchors)} ")
            else:
                modulated.append(char)
                
        stream = "".join(modulated)
        
        # Multi-anchor framing
        head_anchor = " ".join([r.choice(anchors) for _ in range(r.randint(1, 3))])
        tail_anchor = " ".join([r.choice(anchors) for _ in range(r.randint(1, 3))])
        
        # Condensed frame without brackets
        return f"\n{head_anchor} {signal_hash} {head_anchor}\n| {stream}\n{tail_anchor} EOX {tail_anchor}\n"

    def decode(self, signal):
        """
        Attempts to strip localized signal noise.
        """
        cleaned = signal
        # Remove frames
        if ">>> " in cleaned:
            cleaned = cleaned.split(">>> ")[1].split("\n")[0]
            
        # Strip characters from all known noise buffers
        noise_chars = set()
        for loc in self.localities.values():
            noise_chars.update(loc["noise"])
            
        final_text = "".join(c for c in cleaned if c not in noise_chars)
        return final_text.strip()
