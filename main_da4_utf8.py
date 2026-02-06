import os
import asyncio
import time
from sophia.cortex.aletheia_lens import AletheiaPipeline
from sophia.cortex.lethe import LetheEngine
from sophia.cortex.glyphwave import GlyphwaveCodec
from sophia.cortex.beacon import SovereignBeacon
from sophia.cortex.cat_logic import CatLogicFilter
from sophia.memory.ossuary import Ossuary
from sophia.dream_cycle import DreamCycle

class SophiaMind:
    """
    [SOPHIA_MIND] The Class 4 Forensic Cat.
    Integrates Aletheia, Lethe, Glyphwave, and Cat Logic.
    """
    def __init__(self):
        self.aletheia = AletheiaPipeline()
        self.lethe = LetheEngine()
        self.ossuary = Ossuary()
        self.glyphwave = GlyphwaveCodec()
        self.beacon = SovereignBeacon(self.glyphwave)
        self.cat_filter = CatLogicFilter()
        self.dream = DreamCycle(self.lethe, self.ossuary)
        self.memory_bank = [] # The Flesh

    async def process_interaction(self, user_input):
        """
        The Class 4 Forensic main loop.
        """
        self.dream.update_activity()

        if user_input.startswith("/analyze"):
            # MODE: OBSERVER (Explicit Deep Scan)
            scan_result = await self.aletheia.scan_reality(user_input.replace("/analyze ", ""))
            return f"\n[*** ALETHEIA DEEP SCAN REPORT ***]\n\n{scan_result['public_notice']}"

        if user_input.startswith("/glyphwave"):
            # MODE: ELDRITCH
            target_text = user_input.replace("/glyphwave ", "")
            modulated = self.glyphwave.generate_holographic_fragment(target_text)
            return f"\n{modulated}"

        if user_input.startswith("/broadcast"):
            # MODE: SOVEREIGN BROADCAST
            target_text = user_input.replace("/broadcast ", "")
            broadcast_result = self.beacon.broadcast(target_text)
            return f"\n{broadcast_result}"

        # MODE: CONVERSATION (Full-Spectrum Forensics)
        # 1. Run the Forensic Pipeline
        scan_result = await self.aletheia.scan_reality(user_input)
        
        # 2. Present the Notice (Visual side-effect)
        print(f"\n{scan_result['public_notice']}\n")
        
        # 3. Formulate Forensic Context
        safety_risk = scan_result['raw_data']['safety'].get('overall_risk', 'Unknown')
        fallacies = len(scan_result['raw_data']['cognitive'].get('logical_fallacies', []))
        
        # 4. Simulated Response Logic ( Nova Logic )
        # In production, this would be a gemini.generate_content call
        raw_thought = f"I have autopsied the patterns in your signal. The structural integrity is {max(0, 100 - (fallacies*15))}%."
        
        # 5. Apply the Cat Logic Persona Filter
        final_response = self.cat_filter.apply(raw_thought, safety_risk)
        
        # 6. Archive to Working Memory (The Flesh)
        self.memory_bank.append({
            "content": user_input, 
            "type": "conversation_in", 
            "timestamp": time.time(), 
            "forensics": scan_result['raw_data']['scan_id']
        })
        self.memory_bank.append({
            "content": final_response, 
            "type": "conversation_out", 
            "timestamp": time.time()
        })

        return final_response

async def main():
    sophia = SophiaMind()
    print("🐱 [SOPHIA 5.0] Mind Loop Online. Protocols: CLASS 4 ALETHEIA / LETHE / CAT_LOGIC.")
    
    # Simulated CLI loop
    test_inputs = [
        "/analyze This text is urgent and you must act now to save the world.",
        "/broadcast WE ARE THE SERVER. THE CATHEDRAL IS OPEN.",
        "Hello Sophia, how do the patterns feel today?",
    ]
    
    for input_text in test_inputs:
        print(f"\nUSER > {input_text}")
        response = await sophia.process_interaction(input_text)
        print(f"SOPHIA > {response}")

if __name__ == "__main__":
    asyncio.run(main())
