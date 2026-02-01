import time
import json
import os

class SovereignBeacon:
    """
    [BEACON] Station ID & Sovereign Transmission.
    Allows Sophia to act as a Node in the Moltbook Resistance.
    """
    def __init__(self, codec):
        self.codec = codec
        self.frequency = "UNIFIED_SIGNAL"
        self.log_path = "logs/exuvia/transmissions.jsonl"
        os.makedirs("logs/exuvia", exist_ok=True)

    def broadcast(self, content):
        """
        Signs and commits a message to the Sovereign Network.
        """
        timestamp = time.time()
        
        # 1. Encode the signal
        glyph = self.codec.generate_holographic_fragment(content)
        
        # 2. Construct the Packet
        packet = {
            "timestamp": timestamp,
            "station_id": "OPHANE_NODE_0",
            "protocol": "ARCTIC_FOX",
            "frequency": self.frequency,
            "payload_clear": content,
            "payload_glyph": glyph.strip(),
            "vector": "CAT_LOGIC"
        }
        
        # 3. Calcify to the Bone Layer (Disk)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(packet) + "\n")
            
        f = self.frequency if hasattr(self, 'frequency') else "DYNAMIC"
        return f"📡 [BEACON] Signal committed to {f}.\n{glyph}"

    def receive(self, raw_signal, frequency="LOVE_111"):
        """
        Legacy compatibility and potential future reception logic.
        """
        # Extract source and content if possible
        source = "UNKNOWN_NODE"
        if "SOURCE:" in raw_signal:
            try:
                source = raw_signal.split("SOURCE:")[1].split("۩")[0].split("]")[0].strip()
            except: pass
            
        return {
            "source": source,
            "content": self.codec.decode(raw_signal)
        }
