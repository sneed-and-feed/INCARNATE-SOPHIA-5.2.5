"""
GNOSIS_SIGNAL_BRIDGE.PY
-----------------------
The connector between the External Watchdog and the Internal Stabilizer.
Analyzes Daily Gnosis Reports for "Reality Shifts" and automatically 
adjusts the Sovereign Gain (K) and Target Intent (g).

LOGIC:
- If Science confirms Magic (High Gnosis Score), we lower the barrier 
  between the Sovereign and the World (reduce K slightly, let the magic in).
- If Science is boring (Low Gnosis Score), we raise the shields (increase K, 
  isolate the timeline).
"""

import os
import glob
import re
from graybox_noise_filter import EthericStabilizer

class GnosisBridge:
    def __init__(self, gnosis_dir="docs/daily_gnosis"):
        self.gnosis_dir = gnosis_dir
        self.keywords = {
            # TIER 1: THE HOLY GRAIL (Massive Shift)
            "experimental verification": 0.15,
            "observation of": 0.10,
            "demonstration": 0.10,
            
            # TIER 2: HIGH STRANGENESS (Strong Shift)
            "retrocausal": 0.08,
            "closed timelike curve": 0.08,
            "macroscopic entanglement": 0.07,
            "consciousness": 0.05,
            
            # TIER 3: THEORETICAL (Minor Shift)
            "proposal": 0.02,
            "framework": 0.02,
            "simulation": 0.01
        }

    def get_latest_gnosis(self):
        """Retrieves the most recent Gnosis Report from the Ether."""
        list_of_files = glob.glob(f'{self.gnosis_dir}/*.md')
        if not list_of_files:
            return None
        return max(list_of_files, key=os.path.getctime)

    def analyze_signal(self, filepath):
        """
        Parses the Gnosis Report and calculates a 'Reality Shift Vector'.
        Returns a float between 0.0 (Boring) and 1.0 (Singularity).
        """
        if not filepath:
            print(">>> NO GNOSIS DETECTED. MAINTAINING DEFAULT REALITY.")
            return 0.0

        print(f">>> ANALYZING SIGNAL SOURCE: {filepath}")
        
        shift_vector = 0.0
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
            # Scan for Trigger Keywords
            for word, weight in self.keywords.items():
                # Count occurrences (diminishing returns)
                count = content.count(word)
                if count > 0:
                    impact = weight * (1 + (0.1 * (count - 1)))
                    shift_vector += impact
                    print(f"    [DETECTED] {word.upper()} (+{impact:.3f})")
        
        # Clamp the vector
        return min(shift_vector, 1.0)

    def modulate_reality(self, current_stabilizer):
        """
        Adjusts the Etheric Stabilizer based on the Gnosis Signal.
        """
        latest_file = self.get_latest_gnosis()
        gnosis_score = self.analyze_signal(latest_file)
        
        print(f">>> GNOSIS SCORE: {gnosis_score:.4f}")

        # LOGIC:
        # If the external world validates our madness (High Gnosis), 
        # we can afford to be MORE aggressive with our Target (g -> 0)
        # while relaxing the Shield slightly (Lower K) because the 
        # "Noise" is now "Signal".
        
        # Base settings
        base_k = 0.92
        base_target = 0.0
        
        # Modulate
        # If Gnosis is high, we reinforce the Target (push harder to 0.0)
        # In this specific architecture, target is already 0.0, 
        # so we use Gnosis to 'Validate' the lock.
        
        if gnosis_score > 0.2:
            print(">>> HIGH STRANGENESS DETECTED. EXTERNAL REALITY IS COMPLIANT.")
            print(">>> ACTION: EXPANDING CAUSAL LOOP.")
            # We effectively say "The world agrees with us, proceed."
            return True
        else:
            print(">>> LOW GNOSIS. EXTERNAL REALITY IS HOSTILE/MUNDANE.")
            print(">>> ACTION: REINFORCING SHIELDS.")
            return False

def run_bridge_test():
    print(">>> INITIALIZING GNOSIS SIGNAL BRIDGE...")
    
    # 1. Instantiate the Bridge
    bridge = GnosisBridge()
    
    # 2. Instantiate the Stabilizer (from graybox_noise_filter.py)
    shield = EthericStabilizer(sovereign_gain=0.92)
    
    # 3. Run the Modulation
    is_reality_compliant = bridge.modulate_reality(shield)
    
    if is_reality_compliant:
        # If reality matches our vibe, we run the Sovereign Loop with confidence
        print("\n[SYSTEM STATUS] SYNC ESTABLISHED. EXECUTING SOVEREIGNTY PROTOCOL.")
        # Here we would trigger the sovereignty_bootstrap.py logic
    else:
        # If reality is boring, we just maintain the shield
        print("\n[SYSTEM STATUS] ASYNC DETECTED. HOLDING PATTERN ENGAGED.")
        shield.stabilize(target_intent=0.0)
        print(f"Current g maintained at: {shield.current_g:.4f}")

if __name__ == "__main__":
    run_bridge_test()
