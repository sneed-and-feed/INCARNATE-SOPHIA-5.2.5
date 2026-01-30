"""
MODULE: signal_optimizer.py
VERSION: ASOE v1.0
AUTHOR: ASOE Core Team

DESCRIPTION:
    Domain-general Decision Optimizer.
    Scores candidate actions based on Signal Reliability, Temporal Consistency, 
    and Uncertainty Growth.
    Formula: U = Consistency^c * exp(-b * Uncertainty) * (Reliability^a / (1 + Reliability^a)) - Cost
"""

import numpy as np

class SignalOptimizer:
    def __init__(self, a=1.0, b=1.0, c=1.0):
        # Universal System Parameters
        self.params = {
            'a': a,  # Signal Sensitivity (Curvature)
            'b': b,  # Uncertainty Penalty Strength
            'c': c   # Temporal Consistency Weight
        }
        
        # Policy Confidence Thresholds
        self.HIGH_CONFIDENCE = 0.61803398875 # Sophia Prior
        self.thresholds = {
            'EXPLOIT': self.HIGH_CONFIDENCE,
            'EXPLORE': 0.35,
            'HEDGED': 0.15,
            'INHIBIT': 0.05
        }
        
    def calculate_utility(self, reliability: float, consistency: float, uncertainty: float, cost: float = 0.0) -> float:
        """
        Calculates Expected Utility (U) for a candidate action.
        
        Args:
            reliability: Signal trust level (Non-negative float).
            consistency: Temporal stability (Bounded [-1, 1]).
            uncertainty: Information decay/noise (Non-negative float).
            cost: Penalty for action execution.
            
        Returns:
            utility: Expected payoff/gain (Bounded potentially by consistency).
        """
        # 1. Input Sanitization
        reliability = max(float(reliability), 0.0)
        consistency = np.clip(float(consistency), -1.0, 1.0)
        uncertainty = max(float(uncertainty), 0.0)

        a, b, c = self.params['a'], self.params['b'], self.params['c']

        # 2. Reliability Saturation (S-Curve)
        rel_a = reliability ** a
        reliability_gain = rel_a / (1.0 + rel_a)
        
        # 3. Uncertainty Penalty (Exponential Decay)
        stability_bonus = np.exp(-b * uncertainty)
        
        # 4. Consistency Scaling (Conserving sign for directional bias)
        consistency_term = (abs(consistency) ** c) * np.sign(consistency)
        
        # 5. Aggregate Utility
        utility = (consistency_term * stability_bonus * reliability_gain) - cost
        return float(utility)

    def get_confidence_category(self, utility: float) -> str:
        abs_u = abs(utility)
        if abs_u > self.thresholds['EXPLOIT']: return "HIGH_CONFIDENCE_EXPLOIT"
        if abs_u > self.thresholds['EXPLORE']: return "MEDIUM_CONFIDENCE_EXPLORE"
        if abs_u > self.thresholds['HEDGED']: return "LOW_CONFIDENCE_HEDGED"
        return "INHIBIT_ACTION"

    def update_parameters(self, performance_ic: float):
        """Bayesian update of confidence prior based on observed IC."""
        if performance_ic > 0.1:
            self.thresholds['EXPLOIT'] = (self.thresholds['EXPLOIT'] + self.HIGH_CONFIDENCE) / 2
        elif performance_ic < 0.02:
            self.thresholds['EXPLOIT'] *= 0.98
