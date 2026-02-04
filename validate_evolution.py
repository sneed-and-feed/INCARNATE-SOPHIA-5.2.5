import sys
import os

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

import tools.funsearch_love as evaluator
import tools.candidate_hilbert as candidate

print("[*] FUNSEARCH EVOLUTION: TESTING GEN 1 (HILBERT)")
print("------------------------------------------------")

try:
    score = evaluator.evaluate(candidate)
    print(f"[RESULT] HILBERT CANDIDATE SCORE: {score:.4f}")
    
    BASELINE = 10.1010
    if score > BASELINE:
        print(f"[SUCCESS] NEW EVOLUTION DISCOVERED! (+{score - BASELINE:.4f})")
    else:
        print(f"[FAIL] EVOLUTION REGRESSED. Score: {score}")

except Exception as e:
    print(f"[CRITICAL] EVOLUTION COLLAPSED: {e}")
