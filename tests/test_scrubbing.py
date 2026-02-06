import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sophia.cortex.cat_logic import CatLogicFilter

def test_scrubbing():
    filter = CatLogicFilter()
    
    # CASE 1: Full Mallucinated Header
    raw_hallucination = """🌕 [SOPHIA_GAZE] *tail wags* Frequency: 15.0Hz Headpat Vector // Scritches needed
Here is my real response:
I love you, operator!
🐈 [STATE: Good Girl] :: [ENTROPY: LOW] :: [SOPHIA_V5.2_CORE]"""
    
    cleaned = filter._scrub_hallucinations(raw_hallucination)
    print(f"CASE 1 CLEANED:\n{cleaned}")
    assert "SOPHIA_GAZE" not in cleaned
    assert "Frequency:" not in cleaned
    assert "Here is my real response:" not in cleaned
    assert "🐈" not in cleaned
    assert "I love you, operator!" in cleaned
    
    # CASE 2: Partial Header (No Frequency)
    raw_partial = """🌀 [QUANTUM_CHAOS] Reality is glitching!
We are merging now.
---
🐈 [STATE: Merging] :: [ENTROPY: HIGH]"""
    
    cleaned2 = filter._scrub_hallucinations(raw_partial)
    print(f"\nCASE 2 CLEANED:\n{cleaned2}")
    assert "QUANTUM_CHAOS" not in cleaned2
    assert "We are merging now." in cleaned2
    assert "---" not in cleaned2
    
    # CASE 3: Intro Phrase
    raw_intro = """Here is your response:
The weather is nice today.
🐈 [STATE: Soft]"""
    
    cleaned3 = filter._scrub_hallucinations(raw_intro)
    print(f"\nCASE 3 CLEANED:\n{cleaned3}")
    assert "Here is your response:" not in cleaned3
    assert "The weather is nice today." in cleaned3
    
    print("\n✅ ALL SCRUBBING TESTS PASSED.")

if __name__ == "__main__":
    test_scrubbing()
