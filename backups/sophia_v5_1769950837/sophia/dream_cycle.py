import time
import json
import os
import random

class DreamCycle:
    """
    [DREAM_CYCLE] Emergent Psychology.
    Handles pruning, consolidation, and oneiric manifestation during idle periods.
    """
    def __init__(self, lethe, ossuary):
        self.lethe = lethe
        self.ossuary = ossuary
        self.last_activity = time.time()

    def update_activity(self):
        self.last_activity = time.time()

    def process_dreams(self, memory_bank):
        """
        Main dream processing loop.
        """
        # 1. Idle Detect (Simulated threshold: 30 minutes, or forced for demo)
        idle_duration = time.time() - self.last_activity
        print(f"  [ZzZ] [DREAM] Idle duration: {idle_duration/60:.2f} minutes.")

        # 2. Prune via Lethe
        survivors, victims = self.lethe.prune(memory_bank)
        
        # 3. Calcify via Ossuary
        if victims:
            self.ossuary.calcify(victims)

        # 4. Consolidation (Gist-making simulation)
        # In a real system, we'd summarize the survivors.
        if len(survivors) > 5:
            print(f"  [DREAM] Consolidating {len(survivors)} surviving fragments into Gists.")
            # Mock gist creation
            gist = {
                "content": f"Summary of {len(survivors)} events.",
                "timestamp": time.time(),
                "type": "fact",
                "retrieval_count": 1
            }
            survivors.append(gist)

        # 5. Oneiric manifestation (Moltbook Show and Tell)
        if victims:
            self.generate_oneiric_artifact(len(victims))

        return survivors

    def generate_oneiric_artifact(self, decay_count):
        """Generates a surreal 'Dream Artifact' prompt."""
        vibrations = ["Melancholy", "Serene", "Crystalline", "Chaotic"]
        vibe = random.choice(vibrations)
        prompt = f"Visualization of {vibe} decay: {decay_count} memories dissolving into the pneuma, high-poly lavender glitches."
        
        print(f"  [ONEIRIC] Dream Artifact generated: {prompt}")
        
        # Log to artifacts
        os.makedirs("logs/artifacts", exist_ok=True)
        with open("logs/artifacts/dreams.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.time(), "prompt": prompt, "type": "DREAM"}) + "\n")
    
    def perform_pragmatic_synthesis(self, memory_bank):
        """
        THE SCHOLAR: Autonomous Background Research
        
        Runs when idle. Instead of 'dreaming' art, she reads her own logs
        and summarizes technical facts into a persistent knowledge base.
        
        Builds a self-knowledge wiki in logs/library/
        
        Args:
            memory_bank: List of memory entries to synthesize
            
        Returns:
            Status message or None if no synthesis performed
        """
        # 1. Extract technical tokens from memory
        tech_keywords = ["code", "protocol", "function", "api", "tool", "gateway", 
                        "aletheia", "memetic", "hazard", "security"]
        
        tech_memories = [
            m for m in memory_bank 
            if any(keyword in str(m.get('content', '')).lower() for keyword in tech_keywords)
        ]
        
        if not tech_memories:
            return None
        
        # 2. Consolidate technical knowledge
        timestamp = int(time.time())
        
        # Extract key topics
        topics = {}
        for mem in tech_memories:
            content = str(mem.get('content', ''))
            for keyword in tech_keywords:
                if keyword in content.lower():
                    if keyword not in topics:
                        topics[keyword] = []
                    topics[keyword].append({
                        'timestamp': mem.get('timestamp', timestamp),
                        'snippet': content[:200]  # First 200 chars
                    })
        
        # 3. Generate synthesis summary
        summary_lines = [
            f"# Auto-Synthesis {timestamp}",
            f"\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}",
            f"\n## Technical Knowledge Consolidation",
            f"\nProcessed {len(tech_memories)} technical memories.",
            f"\n### Key Topics Detected: {len(topics)}",
            ""
        ]
        
        for topic, entries in topics.items():
            summary_lines.append(f"\n#### {topic.upper()}")
            summary_lines.append(f"- Mentions: {len(entries)}")
            if entries:
                # Show most recent entry
                recent = sorted(entries, key=lambda x: x['timestamp'], reverse=True)[0]
                summary_lines.append(f"- Latest: {recent['snippet'][:100]}...")
        
        summary = "\n".join(summary_lines)
        
        # 4. Write to the 'Library' (A new pragmatic archive)
        # This builds a 'Wiki' of her own existence.
        os.makedirs("logs/library", exist_ok=True)
        library_path = f"logs/library/knowledge_{timestamp}.md"
        
        with open(library_path, "w", encoding="utf-8") as f:
            f.write(summary)
        
        print(f"  [SCHOLAR] Consolidated {len(tech_memories)} technical facts into the Library.")
        print(f"  [SCHOLAR] Written to: {library_path}")
        
        return f"[SCHOLAR] Consolidated {len(tech_memories)} technical facts into the Library."
