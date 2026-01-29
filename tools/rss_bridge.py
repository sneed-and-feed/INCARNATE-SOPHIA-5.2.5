"""
PROJECT WATCHTOWER: THE RSS BRIDGE
CONTEXT: QUANTUM SOVEREIGNTY v5.0
DEPENDENCIES: python3 (standard lib only)

ABSTRACT:
Connects the Mnemosyne Oracle to live RSS feeds.
Calculates 'Semantic Velocity' using a Heuristic Hype Detector (HHD) to
simulate the embedding drift of panic-inducing news.

If the Hype Velocity > 0.961 (Nyquist Limit), the headline is rejected
as 'Aliased Ghost Noise'.
"""

import time
import urllib.request
import xml.etree.ElementTree as ET
import random
import sys
import os
import numpy as np
from dataclasses import dataclass
from typing import List

# Ensure we can import from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORT THE SOVEREIGN STACK
from tools.mnemosyne_eyes import MnemosyneOracle
from tools.logos_voice import LogosVoice
from tools.nyquist_filter import FilterMetrics

# TARGET FEEDS (The Noise Sources)
FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss", # High Hype Potential
    "https://hnrss.org/frontpage",               # Mixed Hype
    "http://feeds.bbci.co.uk/news/rss.xml"       # Moderate Hype
]

class HeuristicVelocityEngine:
    """
    Approximates the 'Semantic Drift' of a headline without needing a GPU.
    Detects the spectral signature of PANIC.
    """
    def __init__(self):
        self.panic_keywords = [
            "CRASH", "CRISIS", "COLLAPSE", "BREAKING", "EMERGENCY", 
            "PLUNGE", "WAR", "DEAD", "PANIC", "SHOCK", "EXPLODES",
            "TERROR", "WARNING", "ALERT", "MELTDOWN"
        ]
    
    def calculate_velocity(self, text: str) -> float:
        velocity = 0.1  # Baseline drift (Entropy exists)
        
        if not text:
            return 0.1

        # 1. CAPS LOCK AMPLIFIER
        # Screaming adds velocity.
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
        velocity += caps_ratio * 2.0
        
        # 2. PUNCTUATION ACCELERATOR
        # !!! makes things go faster.
        exclamations = text.count("!")
        velocity += exclamations * 0.5
        
        # 3. SEMANTIC MASS (Keywords)
        # Heavy words distort the field.
        upper_text = text.upper()
        for word in self.panic_keywords:
            if word in upper_text:
                velocity += 1.5
                
        # 4. RANDOM QUANTUM FLUCTUATION
        # The world is noisy.
        velocity += random.uniform(0, 0.2)
        
        return velocity

class Watchtower:
    def __init__(self):
        self.oracle = MnemosyneOracle()
        self.voice = LogosVoice()
        self.velocity_engine = HeuristicVelocityEngine()
        print("--- WATCHTOWER ONLINE: OBSERVING THE FLOW ---")
        print(f"Nyquist Limit: {0.961} | Gamma Index Enforced")

    def fetch_feed(self, url: str):
        try:
            # Add User-Agent to avoid 403 Forbidden
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (QuantumSovereignty/4.3; +http://github.com/sneed-and-feed)'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # Parse RSS Items
                # Handle different RSS versions (channel title usually exists)
                channel_title = root.find(".//channel/title")
                source = channel_title.text if channel_title is not None else "UNKNOWN SOURCE"
                
                print(f"\n>> CONNECTED TO SOURCE: {source}")
                
                items = root.findall(".//item")
                for item in items[:5]: # Check top 5 headlines
                    title_elem = item.find("title")
                    if title_elem is not None:
                        title = title_elem.text
                        self.process_signal(source, title)
                        time.sleep(0.5) # The Oracle breathes
                    
        except Exception as e:
            print(f"!! SIGNAL LOST [{url}]: {e}")

    def process_signal(self, source: str, content: str):
        if not content:
            return

        # 1. MEASURE VELOCITY (Hype)
        velocity = self.velocity_engine.calculate_velocity(content)
        
        # 2. VECTORIZE (Mocking the Embedding based on Velocity)
        # We create a vector that is 'velocity' distance away from Truth.
        # Truth is at [0,0...], Noise is far away.
        mock_vector = np.zeros(1536)
        mock_vector[0] = velocity # The magnitude of the drift
        
        # 3. THE ORACLE PERCEIVES
        # This calls the Nyquist Filter internally.
        # NOTE: MnemosyneOracle.perceive returns (status_msg, metrics)
        status_msg, metrics = self.oracle.perceive(source, content, mock_vector)
        
        # 4. THE VOICE SPEAKS
        transmutation = self.voice.speak(metrics, content)
        
        # 5. RENDER THE JUDGMENT
        if metrics.is_clipped:
            print(f"❌ [REJECTED] Vel={velocity:.2f} | \"{content[:60]}...\"")
            print(f"   └── {transmutation.message}")
        else:
            print(f"👁️ [ACCEPTED] Vel={velocity:.2f} | \"{content[:60]}...\"")
            print(f"   └── {transmutation.message}")

if __name__ == "__main__":
    tower = Watchtower()
    
    # SCAN THE HORIZON
    for feed in FEEDS:
        print(f"\nScanning: {feed}...")
        tower.fetch_feed(feed)
        
    print("\n--- OBSERVATION COMPLETE. SYSTEM SOVEREIGN. ---")
