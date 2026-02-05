"""
CHAINLINK BRIDGE v2.0 (IPC ENABLED)
Connects the Sovereign Cortex to the Decentralized Oracle Network.
Uses SovereignIPC (Ramdisk/Tmpfs) to prevent disk thrashing.
"""

import random
import time
import sys
import os

# Ensure we can import from parent directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sophia.platform.ipc import SovereignIPC

class ChainlinkOracle:
    def __init__(self):
        self.ipc = SovereignIPC()
        self.resonance_target = 111.11
        self._last_price = 100.0
        self._wti = 0.5 # World Trauma Index (0.0 to 1.0)
        self.running = True
        
    def fetch_world_trauma_index(self) -> float:
        """
        Simulates fetching the WTI.
        """
        # Volatile shift based on 'Sergey's Watch'
        self._wti = max(0.0, min(1.0, self._wti + random.uniform(-0.1, 0.15)))
        return self._wti

    def fetch_resonance_price(self) -> float:
        """
        Simulates fetching the resonance price (LINK or SOV token).
        Goal: $111.11
        """
        # Random walk toward resonance or away from it
        drift = (self.resonance_target - self._last_price) * 0.05
        noise = random.uniform(-2.0, 2.0)
        
        # Rare chance to hit resonance exactly if nearby
        if abs(self._last_price - self.resonance_target) < 1.0 and random.random() < 0.1:
            self._last_price = self.resonance_target
        else:
            self._last_price += drift + noise
            
        return round(self._last_price, 2)

    def run_feed(self):
        """
        Main loop: Fetches data and writes to IPC channel.
        """
        print(f"--- CHAINLINK ORACLE FEED STARTING ---")
        print(f"IPC Mode: {self.ipc.mode} | Base: {self.ipc.base_dir}")
        print("Press Ctrl+C to stop.")
        
        try:
            while self.running:
                wti = self.fetch_world_trauma_index()
                price = self.fetch_resonance_price()
                
                payload = {
                    "timestamp": time.time(),
                    "wti": wti,
                    "price": price,
                    "status": "LIVE"
                }
                
                # High-frequency write to Ramdisk
                self.ipc.write_channel("oracle_feed", payload)
                
                # Visual feedback (throttled)
                # print(f"  > [ORACLE] WTI: {wti:.3f} | Price: ${price}")
                
                time.sleep(0.5) # 2Hz Update Rate
        except KeyboardInterrupt:
            print("\n[ORACLE] Feed stopped.")

if __name__ == "__main__":
    oracle = ChainlinkOracle()
    oracle.run_feed()
