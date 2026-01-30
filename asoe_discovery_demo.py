"""
MODULE: asoe_discovery_demo.py
VERSION: ASOE v1.0
DESCRIPTION:
    Scientific Discovery Simulation.
    Demonstrates ASOE optimizing decision-making in a non-financial domain.
    The engine chooses whether to commit to an 'Experiment' based on signal integrity.
"""

from signal_streamer import SignalStreamer
from policy_mixer import PolicyMixer
import pandas as pd
import numpy as np

def run_scientific_demo(steps=50):
    streamer = SignalStreamer()
    mixer = PolicyMixer()
    
    print("### [ ASOE DEMO: SCIENTIFIC DISCOVERY ENGINES ]")
    print("Domain:       Abstract Experiment Selection")
    print("Engine:       Adaptive Signal Optimization (v1.0)")
    print("-" * 60)
    
    results = []
    
    # Simulate a drift in context over time
    for i in range(steps):
        # Shift context to test adaptability
        if i < 20:
            context = 'STABLE'
        elif i < 35:
            context = 'VOLATILE'
        else:
            context = 'DISRUPTED'
            
        packet = streamer.generate_signal_packet(context)
        history = pd.DataFrame([packet]) # Simplified history for demo
        
        # ASOE Evaluation
        evaluation = mixer.resolve_action_utility(history, packet)
        
        results.append({
            'step': i,
            'context': context,
            'detected_context': evaluation['context'],
            'utility': evaluation['expected_utility'],
            'confidence': evaluation['confidence']
        })
        
        if i % 10 == 0:
            print(f"Step {i:02} | Context: {context:<10} | ASOE Result: {evaluation['confidence']}")
            
    print("-" * 60)
    df = pd.DataFrame(results)
    
    # 1. Accuracy of Context Detection
    accuracy = (df['context'] == df['detected_context']).mean()
    # 2. Inhibition in Disrupted context
    inhibition_rate = (df[df['context'] == 'DISRUPTED']['confidence'] == 'INHIBIT_ACTION').mean()
    
    print(f"Context Detection Accuracy: {accuracy*100:.1f}%")
    print(f"Disruption Inhibition Rate: {inhibition_rate*100:.1f}%")
    print("-" * 60)
    
    if inhibition_rate > 0.9:
        print(">>> VERDICT: ASOE STABILIZED (Resilient Decision Logic)")
    else:
        print(">>> VERDICT: SYSTEM FRAGILE (Inhibition Failed)")

if __name__ == "__main__":
    run_scientific_demo()
