import numpy as np

class ContextClassifier:
    def __init__(self):
        self.context_states = {
            "STABLE": "Predictable / High Integrity",
            "VOLATILE": "High Signal-to-Noise Transition",
            "DISRUPTED": "High Failure Risk / Signal Collapse"
        }

    def _autocorr(self, x, lag=1):
        """Standard NumPy implementation of autocorrelation."""
        if len(x) < lag + 2:
            return 0.0
        n = len(x)
        x_mean = np.mean(x)
        x_var = np.var(x)
        if x_var == 0:
            return 0.0
        x_centered = x - x_mean
        return np.sum(x_centered[lag:] * x_centered[:-lag]) / ((n - lag) * x_var)

    def classify(self, signal_history: np.ndarray, uncertainty: float) -> str:
        """
        Evaluates context based on signal consistency and uncertainty.
        """
        if len(signal_history) < 5:
            return "STABLE"
            
        # 1. Check for Disruption (High Uncertainty/Entropy)
        if uncertainty > 0.8:
            return "DISRUPTED"
            
        # 2. Check for Stability via temporal consistency (Autocorr)
        consistency = self._autocorr(signal_history, lag=1)
        
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
