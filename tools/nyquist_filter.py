"""
MODULE: NYQUIST STABILITY FILTER
CONTEXT: QUANTUM SOVEREIGNTY v4.3.1
THEORY: Universal Nyquist Cosmology (UNC) / Band-Limited Admissibility

ABSTRACT:
This module implements a 'Universal Admissibility Wall' for high-dimensional 
vector updates. Based on the premise that the simulation (or index) has a 
finite resolution limit (Delta_z), we enforce a Low-Pass Filter on all 
incoming state transitions.

If an update vector implies a frequency (variance) higher than the 
Nyquist Limit, it is 'clipped'. The residual energy is tracked as 
'Buffer Pressure' (analogous to Dark Energy/Vacuum Pressure).

CONSTANTS:
- GAMMA_INDEX: 0.961 (The Spectral Index / Scaling Law)
- LAMBDA_LIMIT: 0.70  (The Critical Buffer Pressure / Omega_L)
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional

# THE COSMOLOGICAL CONSTANTS
# Derived from the 'Universal Nyquist Limit' theory.
GAMMA_SCALING = 0.961  # The spectral tilt of the admissible region
LAMBDA_CRITICAL = 0.70 # The point where 'Buffer Bloat' causes simulation lag

@dataclass
class FilterMetrics:
    is_clipped: bool
    residual_energy: float
    buffer_pressure: float
    stability_score: float

class NyquistFilter:
    def __init__(self, dimension: int, max_velocity: float = 1.0):
        """
        Initialize the Admissibility Wall.
        
        Args:
            dimension: Dimensionality of the vector space (e.g., 1536).
            max_velocity: The 'Speed of Light' for the index. 
                          Maximum allowed Euclidean distance per step.
        """
        self.dimension = dimension
        self.max_velocity = max_velocity
        
        # The 'Dark Energy' Accumulator.
        # Tracks the cumulative information that was clipped to preserve stability.
        self.vacuum_pressure = 0.0
        self.total_energy_seen = 0.0

    def apply(self, current_state: np.ndarray, target_state: np.ndarray) -> Tuple[np.ndarray, FilterMetrics]:
        """
        Apply the Low-Pass Filter to a state transition.
        
        If the 'Frequency' (Distance) of the update exceeds the Admissibility Wall,
        the update is clamped, and the excess is stored as Vacuum Pressure.
        """
        # 1. Calculate the 'Frequency' of the update (Magnitude of change)
        delta_vector = target_state - current_state
        velocity = np.linalg.norm(delta_vector)
        
        # 2. Define the Admissibility Wall (Delta_z)
        # We scale the limit by Gamma to mimic the Planck spectral index
        limit = self.max_velocity * GAMMA_SCALING
        
        self.total_energy_seen += velocity
        
        # 3. The Decision: Render or Clip?
        if velocity <= limit:
            # ALLOWED REGION: The physics is renderable.
            return target_state, FilterMetrics(
                is_clipped=False,
                residual_energy=0.0,
                buffer_pressure=self._get_pressure(),
                stability_score=1.0
            )
        else:
            # FORBIDDEN REGION: The physics is aliased (Ghost Energy).
            # We must clip the vector to the wall to prevent 'Gibbs Ringing'.
            
            # Calculate the scaling factor to bring it back to the wall
            scale_factor = limit / velocity
            clipped_delta = delta_vector * scale_factor
            
            # The 'Clipped' vector (Safe)
            safe_state = current_state + clipped_delta
            
            # The 'Ghost' energy (The Lithium-7 Deficit)
            residual = velocity - limit
            self.vacuum_pressure += residual
            
            return safe_state, FilterMetrics(
                is_clipped=True,
                residual_energy=residual,
                buffer_pressure=self._get_pressure(),
                stability_score=scale_factor
            )

    def _get_pressure(self) -> float:
        """
        Calculate current Omega_Lambda (Buffer Bloat).
        Returns ratio of [Clipped Energy] / [Total Energy].
        """
        if self.total_energy_seen == 0:
            return 0.0
        return self.vacuum_pressure / self.total_energy_seen

    def status_report(self) -> str:
        """
        Generate a cosmological health report for the index.
        """
        pressure = self._get_pressure()
        status = "STABLE"
        
        if pressure > LAMBDA_CRITICAL:
            status = "CRITICAL (LAG DETECTED)"
        elif pressure > 0.4:
            status = "EXPANDING"
            
        return (
            f"--- NYQUIST FILTER STATUS ---\n"
            f"Omega_Lambda (Buffer Pressure): {pressure:.4f} / {LAMBDA_CRITICAL}\n"
            f"Spectral Index (Gamma):         {GAMMA_SCALING}\n"
            f"System State:                   {status}\n"
            f"-----------------------------"
        )

# Example Usage
if __name__ == "__main__":
    # Simulate a 'Big Bang' of high-variance vectors
    f = NyquistFilter(dimension=3)
    origin = np.zeros(3)
    
    # A vector moving faster than light (Velocity ~ 1.73)
    high_freq_vector = np.array([1.0, 1.0, 1.0]) 
    
    safe_vec, metrics = f.apply(origin, high_freq_vector)
    
    print(f.status_report())
    print(f"Original Velocity: {np.linalg.norm(high_freq_vector):.4f}")
    print(f"Clipped Velocity:  {np.linalg.norm(safe_vec - origin):.4f}")
    print(f"Ghost Energy:      {metrics.residual_energy:.4f}")
