"""
MODULE: signal_streamer.py
VERSION: ASOE v1.0
DESCRIPTION:
    Domain-neutral Signal Generator for testing the ASOE framework.
    Simulates abstract 'Scientific Experiment' data.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class SignalStreamer:
    def __init__(self):
        self.history = []

    def generate_signal_packet(self, context='STABLE', noise_level=0.1):
        """
        Simulates a packet of signal features for a research experiment.
        Features: Reliability, Consistency, Uncertainty.
        """
        if context == 'STABLE':
            reliability = 2.0 + np.random.normal(0, 0.1)
            consistency = 0.8 + np.random.normal(0, 0.05)
            uncertainty = 0.05 + np.random.normal(0, 0.01)
        elif context == 'VOLATILE':
            reliability = 0.5 + np.random.normal(0, 0.4)
            consistency = 0.2 + np.random.normal(0, 0.3)
            uncertainty = 0.4 + np.random.normal(0, 0.1)
        elif context == 'DISRUPTED':
            reliability = 0.1 + np.random.normal(0, 0.05)
            consistency = -0.7 + np.random.normal(0, 0.1)
            uncertainty = 0.9 + np.random.normal(0, 0.05)
        else:
            reliability = np.random.uniform(0, 3)
            consistency = np.random.uniform(-1, 1)
            uncertainty = np.random.uniform(0, 1)
            
        return {
            'reliability': float(reliability),
            'consistency': float(consistency),
            'uncertainty': float(uncertainty)
        }

    def generate_stream(self, count=100, context='STABLE'):
        packets = [self.generate_signal_packet(context) for _ in range(count)]
        df = pd.DataFrame(packets)
        df['timestamp'] = [datetime.now() + timedelta(seconds=i) for i in range(count)]
        return df
