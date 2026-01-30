"""
MODULE: policy_mixer.py
VERSION: ASOE v1.0
DESCRIPTION:
    Dynamic Policy Engine.
    Mixes and weights candidate decision policies based on detected context.
"""

from signal_optimizer import SignalOptimizer
from context_classifier import ContextClassifier
import pandas as pd

class PolicyMixer:
    def __init__(self):
        self.optimizer = SignalOptimizer(a=1.2, b=0.8, c=1.1)
        self.classifier = ContextClassifier()
        
    def resolve_action_utility(self, signal_history: pd.DataFrame, current_metrics: dict) -> dict:
        """
        Calculates the optimal action utility by mixing policies.
        """
        # 1. Classify Context
        uncertainty = current_metrics['uncertainty']
        consistency_stream = signal_history['consistency'] if 'consistency' in signal_history else pd.Series([current_metrics['consistency']])
        
        context = self.classifier.classify(consistency_stream, uncertainty)
        weights = self.classifier.get_context_weights(context)
        
        # 2. Score Utility (Base ASOE Logic)
        raw_utility = self.optimizer.calculate_utility(
            current_metrics['reliability'],
            current_metrics['consistency'],
            current_metrics['uncertainty']
        )
        
        # 3. Dynamic Mixing (Inhibition Logic)
        # If context is DISRUPTED, utility is nullified.
        final_utility = raw_utility * (1.0 - weights['inhibition'])
        
        category = self.optimizer.get_confidence_category(final_utility)
        
        return {
            'expected_utility': float(final_utility),
            'context': context,
            'confidence': category,
            'weights': weights,
            'action_priority': "HIGH" if abs(final_utility) > 0.35 else "LOW"
        }
