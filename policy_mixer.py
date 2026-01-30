from signal_optimizer import SignalOptimizer
from context_classifier import ContextClassifier
import numpy as np

class PolicyMixer:
    def __init__(self):
        self.optimizer = SignalOptimizer(a=1.2, b=0.8, c=1.1)
        self.classifier = ContextClassifier()
        
    def resolve_action_utility(self, consistency_history: list, current_metrics: dict) -> dict:
        """
        Calculates the optimal action utility by mixing policies.
        history: list of consistency values.
        """
        # 1. Classify Context
        uncertainty = current_metrics['uncertainty']
        consistency_stream = np.array(consistency_history) if consistency_history else np.array([current_metrics['consistency']])
        
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
            'utility': float(final_utility),
            'context': context,
            'confidence': category,
            'weights': weights,
            'action_priority': "HIGH" if abs(final_utility) > 0.35 else "LOW"
        }
