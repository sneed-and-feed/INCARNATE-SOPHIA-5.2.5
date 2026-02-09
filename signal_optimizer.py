import numpy as np
from qtorch import torch
nn = torch.nn
from sophia.cortex.kernels import BitLinear, RMSNorm

class ComplexityRouter(nn.Module):
    """
    Neural router for categorizing input complexity.
    Determines if a signal needs Fast Path or Deep Path processing.
    """
    def __init__(self, input_dim=3, hidden_dim=8):
        super().__init__()
        self.layer1 = BitLinear(input_dim, hidden_dim)
        self.layer2 = BitLinear(hidden_dim, 1)
        self.norm = RMSNorm(input_dim)
        self.activation = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> float:
        with torch.no_grad():
            h = self.layer1(self.norm(x))
            h_act = h.tanh() 
            score = self.activation(self.layer2(h_act))
            return float(score.mean().item())

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
        
        # Quillan-Ronin Tiered Optimization
        self.router = ComplexityRouter()
        self.COMPLEXITY_THRESHOLD = 0.6 # From Quillan v5.1 config
        
    def calculate_utility(self, reliability: float, consistency: float, uncertainty: float, cost: float = 0.0, sovereign_boost: float = 1.0, agency_score: float = 0.0) -> float:
        """
        Calculates Expected Utility (U) for a candidate action.
        Incorporates Agency Score for Sovereign Priority.
        """
        reliability = max(float(reliability), 0.0)
        consistency = np.clip(float(consistency), -1.0, 1.0)
        uncertainty = max(float(uncertainty), 0.0)

        a, b, c = self.params['a'], self.params['b'], self.params['c']

        # Agency Modulator: High agency increases reliability gain floor
        agency_floor = agency_score * 0.2
        rel_a = reliability ** a
        reliability_gain = max(rel_a / (1.0 + rel_a), agency_floor)
        
        stability_bonus = np.exp(-b * uncertainty)
        
        consistency_term = (abs(consistency) ** c) * np.sign(consistency)
        
        # Apply Sovereign Boost and Agency Delta
        utility = ((consistency_term * stability_bonus * reliability_gain) * sovereign_boost) + (agency_score * 0.1) - cost
        return float(utility)

    def route_signal(self, context_vector: torch.Tensor) -> str:
        """
        Uses the ComplexityRouter to determine the processing tier.
        """
        complexity = self.router(context_vector)
        if complexity > self.COMPLEXITY_THRESHOLD:
            return "DEEP_PATH"
        return "FAST_PATH"

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
