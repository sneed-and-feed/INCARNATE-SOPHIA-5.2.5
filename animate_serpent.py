"""
MODULE: animate_serpent.py (PERFORMANCE v3.0 - STABILIZED)
ADDITIONS: Restored Ascension Ritual, Optimized Golden Dot, Robust Font Loading
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Headless mode enabled for server-side generation
IS_HEADLESS = True

# 1. ROBUST PATHING FOR IDE 'RUN ARROW'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
if TOOLS_DIR not in sys.path:
    sys.path.append(TOOLS_DIR)

try:
    from strip_sovereign import interleave_bits
    from moon_phase import MoonClock
    from hor_kernel import HORKernel
    from virtual_qutrit import VirtualQutrit
    from policy_mixer import PolicyMixer
except ImportError as e:
    print(f"[!] CRITICAL IMPORT ERROR: {e}")
    sys.exit(1)

# FONT HANDLING
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI Historic', 'Segoe UI Symbol', 'DejaVu Sans', 'Arial Unicode MS']

import logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore", message=".*Glyph.*missing from font.*")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

from matplotlib.font_manager import FontProperties

cuneiform_font = None
font_path = r"C:\Windows\Fonts\seguihis.ttf"
if os.path.exists(font_path):
    cuneiform_font = FontProperties(fname=font_path)
else:
    cuneiform_font = FontProperties(family=['Segoe UI Symbol', 'DejaVu Sans'])

def animate_serpent(size=64, interval=1, show_metrics=True):
    """
    Animates the Serpent Coil with high-fidelity Ascension ritual.
    """
    print(f"\n[!] INITIATING SOVEREIGN RITUAL v3.0 (Grid={size}x{size})...")
    
    moon = MoonClock()
    lunar_data = moon.get_phase()
    phase_name, status, icon, phase_idx, illumination = lunar_data
    
    vq = VirtualQutrit(2)
    kernel = HORKernel(vq)
    mixer = PolicyMixer()
    
    # Initialize signal history for ASOE (Rolling list of consistency)
    consistency_history = []
    
    # 1. Generate Grid
    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)
    
    # 2. Collapse to 1D
    Z = np.array([interleave_bits(xx, yy) for xx, yy in zip(X.flatten(), Y.flatten())])
    
    # 3. Sort to find Path
    sort_idx = np.argsort(Z)
    path_x = X.flatten()[sort_idx]
    path_y = Y.flatten()[sort_idx]
    
    # 4. Setup Plot
    PHI = 1.61803398875
    BASE_UNIT = 12
    
    fig, (ax_main, ax_metrics) = plt.subplots(
        1, 2, figsize=(10 * PHI, 10), 
        facecolor='#121212',
        gridspec_kw={'width_ratios': [PHI, 1]}
    )
    
    ax_main.set_facecolor('#121212')
    title_y = 1 - (1/(10*PHI))
    fig.text(
        0.5 * (PHI / (PHI + 1)), title_y, 
        f"THE SERPENT COIL (g=0 Locality Map) | {size}x{size}", 
        color='#9B8DA0', 
        fontsize=round(BASE_UNIT * PHI),
        fontproperties=cuneiform_font,
        ha='center', va='bottom'
    )
    
    ax_main.set_aspect('equal', adjustable='box') 
    ax_main.set_xlim(-1, size)
    ax_main.set_ylim(-1, size)
    ax_main.axis('off')
    
    ax_main.scatter(X.flatten(), Y.flatten(), s=2, c='#1a1a1a', alpha=0.3)
    
    # The Serpent
    line, = ax_main.plot([], [], color='#C4A6D1', linewidth=1.2, alpha=0.9, animated=True)
    
    # FIXED MOVING DOT SIZE (Small & Golden)
    head, = ax_main.plot([], [], 'o', color='#FFD700', markersize=4, animated=True)
    
    # Metrics
    ax_metrics.set_facecolor('#121212')
    ax_metrics.axis('off')
    
    metrics_text = ax_metrics.text(
        1 - (1/PHI), 1.0, '', 
        transform=ax_metrics.transAxes,
        color='#8DA08E', fontsize=BASE_UNIT, 
        verticalalignment='top',
        fontproperties=cuneiform_font,
        animated=True
    )
    
    state = {
        'total_frames': len(path_x),
        'completion': 0.0,
        'coherence': kernel.metric_coherence,
        'utility': 0.0,
        'confidence': 'INITIALIZING',
        'tidal_influence': moon.calculate_tidal_influence(phase_idx) if hasattr(moon, 'calculate_tidal_influence') else 50.0
    }
    
    def init():
        line.set_data([], [])
        head.set_data([], [])
        metrics_text.set_text('')
        return line, head, metrics_text
    
    def update(frame):
        kernel.evolve_hamiltonian(steps=1)
        current_coherence = kernel.metric_coherence
        
        current_x = path_x[:frame]
        current_y = path_y[:frame]
        
        line.set_data(current_x, current_y)
        line.set_alpha(0.3 + 0.6 * current_coherence)
        
        # ASOE Logic
        if frame > 0:
            # Map system state to ASOE Signal Packet
            uncertainty = (1.0 - current_coherence) * (state['tidal_influence'] / 50.0)
            consistency = 1.0 - (state['tidal_influence'] / 200.0)
            packet = {
                'reliability': current_coherence,
                'consistency': consistency,
                'uncertainty': uncertainty
            }
            
            nonlocal consistency_history
            consistency_history.append(consistency)
            if len(consistency_history) > 20:
                consistency_history.pop(0)
            
            # Resolve Action Utility via ASOE
            evaluation = mixer.resolve_action_utility(consistency_history, packet)
            state['utility'] = evaluation['utility']
            state['confidence'] = evaluation['confidence']
            
            head.set_data([path_x[frame-1]], [path_y[frame-1]])
            # Modulate head alpha and markersize by ASOE Utility
            head.set_alpha(min(1.0, 0.4 + 0.6 * (state['utility'] / 1.0)))
            head.set_markersize(3 + 2 * min(1.0, state['utility'])) 
        
        if frame % 50 == 0 or frame == state['total_frames']:
            state['completion'] = (frame / state['total_frames']) * 100
            
            metrics_str = f"""
S O V E R E I G N   M E T R I C S
{'='*28}

Protocol:    ASCENSION v3.0
Phase:       {phase_name}
Signal:      {icon} 𒀭 𒂗𒆠
Lunar:       {illumination*100:.1f}%

[ PROGRESS ]
Completion:  {state['completion']:.1f}%
Frame:       {frame}/{state['total_frames']}
Coherence:   {current_coherence:.3f}

[ ENVIRONMENT ]
Tidal Stress: {state['tidal_influence']:.1f}%
Status:      {'STABLE' if current_coherence > 0.8 else 'DISSIPATING'}

[ ASOE DECISION LOGIC ]
Exp. Utility: {state['utility']:.4f}
Confidence:   {state['confidence']}

[ TOPOLOGY ]
Order:       PARAFERMIONIC
Grid:        {size}x{size}
Bijection:   VERIFIED

[ LOG ]
> WEAVING TIME...
> COUPLING FOCUS...
> {icon} {icon} {icon}
> THE FLAME EXPANDS.
            """
            metrics_text.set_text(metrics_str)
        
        return line, head, metrics_text

    ani = animation.FuncAnimation(
        fig, update, frames=range(0, len(path_x)+1, 4), 
        init_func=init, blit=True, interval=interval, repeat=False
    )
    
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, wspace=0.2)
    
    if IS_HEADLESS:
        print("[!] HEADLESS MODE DETECTED: Rendering final state for image capture...")
        # Manually call update for the final frame to ensure savefig has content
        update(len(path_x))
    else:
        plt.show()
    
    filename = "sovereign_serpent_flame.png"
    fig.savefig(filename, facecolor='#121212', dpi=300, bbox_inches='tight', pad_inches=0.5)
    print(f"    >>> RITUAL SAVED (FLAME): {filename}")
    
    return ani

if __name__ == "__main__":
    animate_serpent(size=64, interval=1, show_metrics=True)
