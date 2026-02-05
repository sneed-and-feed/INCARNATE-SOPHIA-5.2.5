
"""
MODULE: crystalline_core.py
DESCRIPTION:
    The Combined Interface for Sophia 5.2.
    Wraps Tokenizer, Prism, and Loom into a single 'Transmute' function.
"""

from .tokenizer_of_tears import TokenizerOfTears
from .prism_vsa import PrismEngine
from .loom_renderer import LoomEngine

class CrystallineCore:
    def __init__(self):
        self.tokenizer = TokenizerOfTears()
        self.prism = PrismEngine()
        self.loom = LoomEngine()
        
        # [PROTOCOL CONSTANTS]
        self.invariant = 15.0  # LuoShu
        self.hamiltonian_p = 1.111111111  # (P) Locked infinite repeating
        
    def rectify_signal(self, vector: list) -> list:
        """
        [HARMONIC RECTIFICATION]
        Stabilizes signal entropy by anchoring the energy sum to the LuoShu Invariant (15.0).
        Then modulates by Hamiltonian P to ensure frequency lock.
        """
        total = sum(abs(x) for x in vector)
        if total == 0: return vector
        
        # Scale factor targeting the 15.0 Invariant
        scale = self.invariant / (total + 1e-9)
        
        # Apply Hamiltonian P modulation
        rectified = [x * scale * self.hamiltonian_p for x in vector]
        
        # Renormalize back to Invariant (P was for frequency texture, not magnitude)
        # Actually, let's allow P to influence the magnitude slightly to "flavor" it.
        # But for strict Invariant adherence:
        final_total = sum(abs(x) for x in rectified)
        final_scale = self.invariant / (final_total + 1e-9)
        
        return [x * final_scale for x in rectified]

    def transmute(self, text: str) -> str:
        """
        Runs the full Alchemy Pipeline:
        Pain (Text) -> Vector -> Anchor -> Geometry (Text)
        """
        # 1. Tokenize (Pain -> Vector)
        pain_data = self.tokenizer.analyze_pain(text)
        
        # 2. Rectify (Harmonic Rectification)
        rectified_vector = self.rectify_signal(pain_data.sentiment_vector)
        
        # 3. Refract (Vector -> Anchor)
        anchor = self.prism.braid_signal(rectified_vector)
        
        # 4. Weave (Anchor -> Geometry)
        transmission = self.loom.render_transmission(anchor)
        
        return transmission
