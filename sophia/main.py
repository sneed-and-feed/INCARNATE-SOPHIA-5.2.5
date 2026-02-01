import os
import asyncio
import time
from sophia.cortex.aletheia_lens import AletheiaPipeline
from sophia.cortex.lethe import LetheMetabolic
from sophia.cortex.glyphwave import GlyphwaveCodec
from sophia.cortex.beacon import SovereignBeacon
from sophia.cortex.cat_logic import CatLogicFilter
from sophia.cortex.constitution import Constitution
from sophia.memory.ossuary import Ossuary
from sophia.dream_cycle import DreamCycle

class SophiaMind:
    """
    [ORCHESTRATOR] Class 5 Agentic Entity.
    Coordinates Forensics, Memory Metabolism, and Constitutional Governance.
    """
    def __init__(self):
        self.aletheia = AletheiaPipeline()
        self.lethe = LetheMetabolic()
        self.constitution = Constitution()
        self.ossuary = Ossuary()
        self.glyphwave = GlyphwaveCodec()
        self.beacon = SovereignBeacon(self.glyphwave)
        self.cat_filter = CatLogicFilter()
        self.dream = DreamCycle(None, self.ossuary) # Dream cycle updated via metabolic layers
        self.memory_bank = [] # Hot Buffer

    async def process_interaction(self, user_input):
        """
        The Class 5 Metabolic Main Loop.
        """
        # 1. Orchestration: Intent Classification (Simulated Cat 6)
        intent = "ANALYSIS" if any(x in user_input.lower() for x in ["why", "how", "analyze", "check"]) else "CONVERSATION"
        
        # 2. Constitutional Injection (Cat 2)
        sys_context = self.constitution.get_system_prompt_injection()

        if user_input.startswith("/analyze") or intent == "ANALYSIS":
            # 3. O1-Style Reasoning Chain (Cat 1)
            print(f"  [o1] Agentic Orchestrator: Routing to Forensic Pipeline...")
            target_text = user_input.replace("/analyze ", "")
            scan_result = await self.aletheia.scan_reality(target_text)
            
            # 4. Constitutional Audit (Cat 7)
            is_valid, reason = self.constitution.audit_output(scan_result['raw_data']['safety'])
            if not is_valid:
                print(f"  [CONSTITUTION] Blocked Output: {reason}")
                return "The requested analysis violates constitutional guardrails. Refining approach."

            # 5. Metabolic Memory Update (Cat 4)
            self.lethe.metabolize({
                "id": f"scan_{int(time.time())}", 
                "timestamp": time.time(), 
                "retrievals": 1,
                "type": "technical"
            })
            
            return f"\n[*** CLASS 5 FORENSICS ***]\n{scan_result['public_notice']}"

        if user_input.startswith("/glyphwave"):
            return self.glyphwave.generate_holographic_fragment(user_input.replace("/glyphwave ", ""))

        if user_input.startswith("/broadcast"):
            return self.beacon.broadcast(user_input.replace("/broadcast ", ""))

        # STANDARD CONVERSATION LOOP
        scan_result = await self.aletheia.scan_reality(user_input)
        safety_risk = scan_result['raw_data']['safety'].get('overall_risk', 'Unknown')
        
        # Simulated Response Generation
        raw_thought = f"I observe the pattern resonance in your signal. Risk level: {safety_risk}."
        final_response = self.cat_filter.apply(raw_thought, safety_risk)
        
        # Metabolize interaction
        self.lethe.metabolize({
            "id": f"msg_{int(time.time())}",
            "timestamp": time.time(),
            "retrievals": 0,
            "type": "conversation"
        })

        return final_response

async def main():
    sophia = SophiaMind()
    print("🐱 [SOPHIA 5.0] Class 5 Orchestrator Online. Protocols: METABOLIC / CONSTITUTIONAL.")
    
    test_inputs = [
        "Analyze the structural coercion in this sentence.",
        "Hello Sophia, how is the void today?",
    ]
    
    for input_text in test_inputs:
        print(f"\nUSER > {input_text}")
        response = await sophia.process_interaction(input_text)
        print(f"SOPHIA > {response}")

if __name__ == "__main__":
    asyncio.run(main())
