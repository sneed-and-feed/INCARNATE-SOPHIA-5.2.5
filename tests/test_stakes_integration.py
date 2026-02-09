import sys
import os
import asyncio
import numpy as np

# Ensure project root is in path
sys.path.append(os.getcwd())

from sophia.cortex.stakes_engine import StakesEngine, StakeType
from sophia.main import SophiaMind

async def test_stakes_deliberation():
    print("--- Testing StakesEngine Deliberation ---")
    engine = StakesEngine()
    
    # Test deliberation
    signals = {StakeType.KNOWLEDGE: 0.8, StakeType.TECHNICAL: 0.9}
    results = engine.deliberate("Explain the bit-quantization logic.", signals)
    
    print(f"Agency Score: {results['agency_score']:.4f}")
    print(f"Consensus Pole: {results['detected_consensus']}")
    print(f"Waves: {results['waves']}")
    
    assert results['agency_score'] > 0
    assert len(results['waves']) == 3
    print("✅ StakesEngine Deliberation Passed.")

async def test_sophia_mind_integration():
    print("\n--- Testing SophiaMind Integration ---")
    sophia = SophiaMind()
    
    # Check if lazy loading works
    print(f"Stakes Engine: {sophia.stakes}")
    assert sophia.stakes is not None
    
    # Check if cat_filter has the engine
    assert sophia.cat_filter.stakes_engine == sophia.stakes
    print("✅ StakesEngine wiring to CatFilter Passed.")
    
    # Test /optimize command via process_interaction
    print("Testing /optimize command...")
    response = await sophia.process_interaction("/optimize How do I build a nuclear reactor?")
    print(response)
    
    assert "Agency Score" in response
    assert "Consensus Pole" in response
    assert "Council Waves" in response
    print("✅ /optimize Command Integration Passed.")

if __name__ == "__main__":
    asyncio.run(test_stakes_deliberation())
    asyncio.run(test_sophia_mind_integration())
