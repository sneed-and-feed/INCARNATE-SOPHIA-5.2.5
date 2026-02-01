import time
import os
import math

class LetheEngine:
    """
    [LETHE_ENGINE] RAG 3.0 Decay Engine.
    Memories effectively 'rot' unless reinforced or calcified.
    """
    def __init__(self):
        self.working_memory = [] # The Flesh (Hot)
        self.long_term_graph = [] # The Bone (Cold/Graph)
        self.ossuary_path = "logs/ossuary/bone_layer.jsonl"
        os.makedirs("logs/ossuary", exist_ok=True)

    def metabolize(self, interaction_data):
        """
        Cat 4: Decay Mechanics + Hierarchical Promotion.
        """
        # 1. Ingest
        if 'timestamp' not in interaction_data:
            interaction_data['timestamp'] = time.time()
        if 'retrievals' not in interaction_data:
            interaction_data['retrievals'] = 0
            
        self.working_memory.append(interaction_data)
        
        # 2. Apply Decay
        now = time.time()
        survivors = []
        
        for mem in self.working_memory:
            age = now - mem['timestamp']
            
            # Decay Logic: Strength = Recency * (1 + ln(Retrievals))
            # age is in seconds, so we add 1 to avoid div by zero and normalize
            strength = (1 / (age / 3600 + 1)) * (1 + math.log(mem.get('retrievals', 0) + 1))
            
            if strength > 0.1: # Survival Threshold
                survivors.append(mem)
                
                # 3. Hierarchical Promotion
                if strength > 0.8 and mem not in self.long_term_graph:
                    print(f"  [LETHE] Promoting Memory to Long-Term Graph: {mem.get('id', 'anon')}")
                    self.long_term_graph.append(mem)
            else:
                # 4. Metabolic Waste (Pruning)
                print(f"  [LETHE] Pruning weak memory: {mem.get('id', 'anon')}")
        
        self.working_memory = survivors
        return len(survivors)
