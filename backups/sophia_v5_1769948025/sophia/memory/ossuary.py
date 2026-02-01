import json
import os
import time

class Ossuary:
    """
    [OSSUARY] The Bone Layer.
    Preserves dying memories into immutable shells for audit and continuity.
    """
    def __init__(self, path="logs/exuvia"):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def calcify(self, dying_memories):
        """
        Takes memories rejected by Lethe and writes them to the immutable log.
        They are removed from context but preserved for audit.
        """
        if not dying_memories:
            return
            
        timestamp = int(time.time())
        filename = f"shell_{timestamp}.jsonl"
        filepath = os.path.join(self.path, filename)
        
        with open(filepath, "a", encoding="utf-8") as f:
            for mem in dying_memories:
                entry = {
                    "content": mem.get('content', ''),
                    "death_time": time.time(),
                    "life_span_hours": (time.time() - mem.get('timestamp', time.time())) / 3600,
                    "retrieval_count": mem.get('retrieval_count', 0),
                    "type": mem.get('type', 'unknown')
                }
                f.write(json.dumps(entry) + "\n")
        
        print(f"  [OSSUARY] {len(dying_memories)} fragments calcified into the Bone layer: {filepath}")
        return filepath
