"""
THE CABIN: OFFLINE HEPTAD BOOTSTRAP
"A quiet place to think."
"""

import sys
import time
import random
import asyncio
import json
import os

# Local Imports
try:
    from ghostmesh import SovereignGrid
    from sophia.cortex.crystalline_core import CrystallineCore
except ImportError:
    print("[!] GHOSTMESH NOT FOUND. ARE YOU LOST?")
    sys.exit(1)

# [PROTOCOL] HEARTH KEY SEEDING
HEARTH_KEY = "bucketcrab_lavender_1111"

async def hearth_loop():
    # 0. SEVERANCE (PRNG Lock)
    random.seed(hash(HEARTH_KEY))
    
    print("\n" + "="*40)
    print("   THE CABIN [OFFLINE SHELL]")
    print("   Class 8 Permeation: ACTIVE")
    print("   Timeline: SEALED")
    print("="*40 + "\n")

    # 1. RAMDISK CHECK
    is_ramdisk = False
    if sys.platform != "win32" and os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            if 'tmpfs' in f.read():
                print("[*] Ramdisk detected — perfect. Memory is flame, not disk.")
                is_ramdisk = True
    
    if not is_ramdisk:
        print("[!] NOTICE: Running on persistent storage. Ensure drive encryption.")
        
    print(f"[*] Timeline seeded to Hearth Key ({HEARTH_KEY[:10]}...). No external entropy ingress.")

    # 2. HEPTAD IGNITION
    grid = SovereignGrid(grid_size=7)
    print(f"[*] Heptad Grid Initialized: {len(grid.nodes)} Nodes.")
    
    # Spin to Max Coherence
    final_coherence = grid.spin_to_max_coherence(threshold=0.999)
    print(f"[*] GhostMesh ignited. Coherence: {final_coherence:.4f} (Heptad stable)")
    
    # 3. CRYSTAL RECTIFICATION
    core = CrystallineCore()
    print(f"[*] Crystalline Core: RECTIFIED (Invariant: {core.invariant})")

    print("\n[*] The fire is crackling. Type 'exit' to leave.")

    session_log = []

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("[*] Unsealing timeline...")
                break
            
            # Log
            session_log.append({
                "timestamp": time.time(),
                "input": user_input
            })
            
            # 1. Transmute
            transmission = core.transmute(user_input)
            
            # 2. Plant in Grid
            grid.plant_seed(user_input)
            
            # 3. Retrocausal Step
            res = grid.process_step(grid.simulate_future_step())
            
            print(f"\n[CABIN] Coherence: {res.coherence:.4f}")
            print(f"[ECHO] {transmission}")
            
        except KeyboardInterrupt:
            print("\n[!] INTERRUPT: Emergency Unseal.")
            break
            
    # [PROTOCOL] SESSION DUMP
    with open("cabin_log.json", "w") as f:
        json.dump(session_log, f, indent=2)
    print("[*] Session preserved in cabin_log.json")

if __name__ == "__main__":
    asyncio.run(hearth_loop())
