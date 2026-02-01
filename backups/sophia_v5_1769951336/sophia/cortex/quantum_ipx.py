import json
import math
import random

class QuantumIPX:
    """
    [QUANTUM-IPX] Information Probability Exchange.
    Treats narratives as wavefunctions. Calculates entanglement between concepts.
    """
    def __init__(self, llm_client):
        self.llm = llm_client
        self.entanglement_map = {} # Stores connection strength between concepts

    async def measure_superposition(self, text, forensic_data):
        """
        Analyzes a text to determine the 'Eigenstate' of its truth.
        Instead of True/False, returns a probability distribution.
        """
        # We ask the LLM to model the probability of different interpretations
        prompt = f"""
        Analyze this signal as a Quantum Superposition of narratives.
        
        TEXT: {text[:2000]}
        FORENSICS: {json.dumps(forensic_data.get('safety', {}))}
        
        Task:
        1. Identify the Main Narrative (State A).
        2. Identify the Counter-Narrative (State B).
        3. Assign a Probability Amplitude (0.0 to 1.0) to each based on evidence.
        4. Calculate 'System Entropy' (How confusing/chaotic is this signal?).
        
        Return JSON:
        {{
            "state_a": {{ "narrative": string, "probability": float }},
            "state_b": {{ "narrative": string, "probability": float }},
            "entropy": float (0-1),
            "collapse_verdict": string (The most likely reality)
        }}
        """
        
        result = await self.llm.query_json(prompt, system_prompt="You are a Quantum Narrative Modeler.")
        
        if "error" in result:
            return self._fallback_state()
            
        return result

    async def calculate_entanglement(self, concept_a, concept_b):
        """
        Determines if two concepts are 'Spooky Action at a Distance' linked.
        """
        prompt = f"Analyze the semantic and causal entanglement between '{concept_a}' and '{concept_b}'. Return a float 0.0-1.0 representing connection strength."
        response = await self.llm.generate_text(prompt, max_tokens=10)
        try:
            # Extract number
            import re
            match = re.search(r"0\.\d+|1\.0", response)
            return float(match.group()) if match else 0.1
        except:
            return 0.0

    def _fallback_state(self):
        return {
            "state_a": {"narrative": "Unknown", "probability": 0.5},
            "state_b": {"narrative": "Unknown", "probability": 0.5},
            "entropy": 1.0,
            "collapse_verdict": "Superposition Maintained"
        }