"""
MODULE: context_classifier.py
VERSION: ASOE v1.0
DESCRIPTION:
    Classifies the operational context based on signal dynamics. 
    Routes decision policies based on environmental stability.
"""

import numpy as np
import pandas as pd

class ContextClassifier:
    def __init__(self):
        self.context_states = {
            "STABLE": "Predictable / High Integrity",
            "VOLATILE": "High Signal-to-Noise Transition",
            "DISRUPTED": "High Failure Risk / Signal Collapse"
        }

    def classify(self, signal_history: pd.Series, uncertainty: float) -> str:
        """
        Evaluates context based on signal consistency and uncertainty.
        """
        if len(signal_history) < 5:
            return "STABLE"
            
        # 1. Check for Disruption (High Uncertainty/Entropy)
        if uncertainty > 0.8:
            return "DISRUPTED"
            
        # 2. Check for Stability via temporal consistency (Autocorr)
        consistency = signal_history.autocorr(lag=1)
        
        if abs(consistency) > 0.4:
            return "STABLE"
        else:
            return "VOLATILE"
            
    def get_context_weights(self, context: str) -> dict:
        """Returns policy weighting recommendations for the mixer."""
        if context == "STABLE":
            return {"exploitation": 0.8, "exploration": 0.2, "inhibition": 0.0}
        elif context == "VOLATILE":
            return {"exploitation": 0.2, "exploration": 0.7, "inhibition": 0.1}
        elif context == "DISRUPTED":
            return {"exploitation": 0.0, "exploration": 0.0, "inhibition": 1.0}
        return {"exploitation": 0.3, "exploration": 0.3, "inhibition": 0.4}
