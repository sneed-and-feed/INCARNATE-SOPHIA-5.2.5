"""
MODULE: animate_serpent.py (PERFORMANCE v3.3 - SYNCED FLASH)
ADDITIONS: Coherence-Triggered Glitching, Structural Failure Mode
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# Headless mode enabled for server-side generation
IS_HEADLESS = False 

# 1. ROBUST PATHING
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
warnings.filterwarnings("ignore")

from matplotlib.font_manager import FontProperties
cuneiform_font = FontProperties(fname=r"C:\Windows\Fonts\seguihis.ttf") if os.path.exists(r"C:\Windows\Fonts\seguihis.ttf") else FontProperties(family=['Segoe UI Symbol'])

def animate_serpent(size=64, interval=1, show_metrics=True):
    """
    Animates the Serpent Coil with SYNCED FLASH (Coherence Triggered).
    """
    print(f"\n[!] INITIATING SOVEREIGN RITUAL v3.3 (Grid={size}x{size})...")
    print("    >>> WARNING: GLITCH SYNCED TO LOW COHERENCE (< 0.80)")
    
    # [INIT] SYSTEM
    moon = MoonClock()
    lunar_data = moon.get_phase()
    phase_name, status, icon, phase_idx, illumination = lunar_data
    
    vq = VirtualQutrit(2)
    kernel = HORKernel(vq)
    mixer = PolicyMixer()
    consistency_history = []
    
    # 1. Generate Grid & Path
    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)
    Z = np.array([interleave_bits(xx, yy) for xx, yy in zip(X.flatten(), Y.flatten())])
    sort_idx = np.argsort(Z)
    path_x = X.flatten()[sort_idx]
    path_y = Y.flatten()[sort_idx]
    
    # 2. Setup Plot
    PHI = 1.61803398875
    BASE_UNIT = 12
    
    fig, (ax_main, ax_metrics) = plt.subplots(
        1, 2, figsize=(10 * PHI, 10), 
        facecolor='#050505', 
        gridspec_kw={'width_ratios': [PHI, 1]}
    )
    
    ax_main.set_facecolor('#050505')
    title_y = 1 - (1/(10*PHI))
    fig.text(
        0.5 * (PHI / (PHI + 1)), title_y, 
        f"THE SERPENT COIL (Synced Failure) | {size}x{size}", 
        color='#9B8DA0', 
        fontsize=round(BASE_UNIT * PHI),
        fontproperties=cuneiform_font,
        ha='center', va='bottom'
    )
    
    ax_main.set_aspect('equal', adjustable='box') 
    ax_main.set_xlim(-1, size)
    ax_main.set_ylim(-1, size)
    ax_main.axis('off')
    
    # [LAYER 0] BACKGROUND GRID
    grid_scatter = ax_main.scatter(X.flatten(), Y.flatten(), s=1, c='#1a1a1a', alpha=0.3, animated=True)
    
    # --- [LAYER 1] THE CYAN GHOST (Deep Echo) ---
    line_cyan, = ax_main.plot([], [], color='#00FFFF', linewidth=2.0, alpha=0.3, animated=True)
    head_cyan, = ax_main.plot([], [], 'o', color='#00FFFF', markersize=6, alpha=0.3, animated=True)

    # --- [LAYER 2] THE MAGENTA GHOST (The Alarm) ---
    line_magenta, = ax_main.plot([], [], color='#FF00FF', linewidth=1.5, alpha=0.5, animated=True)
    head_magenta, = ax_main.plot([], [], 'o', color='#FF00FF', markersize=5, alpha=0.5, animated=True)

    # --- [LAYER 3] THE REALITY (Stable) ---
    line_main, = ax_main.plot([], [], color='#E0E0E0', linewidth=1.0, alpha=0.9, animated=True) 
    head_main, = ax_main.plot([], [], 'o', color='#FFD700', markersize=4, animated=True) 

    # Metrics Text
    ax_metrics.set_facecolor('#050505')
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
        'tidal_influence': moon.calculate_tidal_influence(phase_idx) if hasattr(moon, 'calculate_tidal_influence') else 50.0,
        'glitch_lock_cyan': 0
    }
    
    def init():
        line_cyan.set_data([], [])
        head_cyan.set_data([], [])
        line_magenta.set_data([], [])
        head_magenta.set_data([], [])
        line_main.set_data([], [])
        head_main.set_data([], [])
        metrics_text.set_text('')
        grid_scatter.set_offsets(np.c_[X.flatten(), Y.flatten()]) 
        return line_cyan, head_cyan, line_magenta, head_magenta, line_main, head_main, metrics_text, grid_scatter
    
    def update(frame):
        kernel.evolve_hamiltonian(steps=1)
        current_coherence = kernel.metric_coherence
        
        # --- [FORCE ENTROPY] ---
        # If the kernel is too perfect, we manually inject chaos to test the flash
        # (Remove this line if your kernel is naturally chaotic)
        if frame % 60 > 40: 
             current_coherence *= 0.75  # SIMULATE SIGNAL DROP
        
        # --- [DATAMOSH] NOISE ---
        noise_level = (1.0 - current_coherence) * 0.8 
        
        # --- CALCULATE TEMPORAL OFFSETS ---
        idx_cyan = max(0, frame - 12) 
        idx_magenta = max(0, frame - 6)
        
        # --- UPDATE CYAN (Always Noisy) ---
        if state['glitch_lock_cyan'] == 0:
            if np.random.random() < 0.05: state['glitch_lock_cyan'] = np.random.randint(5, 12)
            
            jx = np.random.normal(0, noise_level, size=idx_cyan)
            jy = np.random.normal(0, noise_level, size=idx_cyan)
            line_cyan.set_data(path_x[:idx_cyan] + jx, path_y[:idx_cyan] + jy)
            if idx_cyan > 0:
                head_cyan.set_data([path_x[idx_cyan-1]], [path_y[idx_cyan-1]])
        else:
            state['glitch_lock_cyan'] -= 1
        
        # --- UPDATE MAGENTA (THE SYNCED FLASH) ---
        # TRIGGER: COHERENCE < 0.80
        if current_coherence < 0.80:
            # !!! CRITICAL FAILURE: SWAP AXES !!!
            # The Magenta layer flips X and Y
            line_magenta.set_data(path_y[:idx_magenta], path_x[:idx_magenta])
            if idx_magenta > 0:
                head_magenta.set_data([path_y[idx_magenta-1]], [path_x[idx_magenta-1]])
        else:
            # STABLE STATE
            line_magenta.set_data(path_x[:idx_magenta], path_y[:idx_magenta])
            if idx_magenta > 0:
                head_magenta.set_data([path_x[idx_magenta-1]], [path_y[idx_magenta-1]])
        
        # --- UPDATE MAIN ---
        line_main.set_data(path_x[:frame], path_y[:frame])
        if frame > 0:
            head_main.set_data([path_x[frame-1]], [path_y[frame-1]])

        # --- BACKGROUND PULSE ---
        if frame % 5 == 0:
             bg_jitter = np.random.normal(0, 0.05, size=(size*size, 2))
             grid_scatter.set_offsets(np.c_[X.flatten(), Y.flatten()] + bg_jitter)

        # ASOE Logic
        if frame > 0:
            uncertainty = (1.0 - current_coherence) * (state['tidal_influence'] / 50.0)
            consistency = 1.0 - (state['tidal_influence'] / 200.0)
            packet = {'reliability': current_coherence, 'consistency': consistency, 'uncertainty': uncertainty}
            
            nonlocal consistency_history
            consistency_history.append(consistency)
            if len(consistency_history) > 20: consistency_history.pop(0)
            
            evaluation = mixer.resolve_action_utility(consistency_history, packet)
            utility = evaluation['utility']
            head_main.set_markersize(3 + 3 * utility) 
        else:
            utility = 0.0

        if frame % 20 == 0:
            status_color = "FAILURE" if current_coherence < 0.8 else "STABLE"
            metrics_str = f"""
S O V E R E I G N   M E T R I C S
{'='*28}

Protocol:    SYNCED_FLASH v3.3
Phase:       {phase_name}
Signal:      {icon} 𒀭 𒂗𒆠

[ SIGNAL STATUS ]
Coherence:   {current_coherence:.3f}
State:       {status_color}
Mag Flash:   {'!!! TEARING !!!' if current_coherence < 0.8 else 'SYNCED'}

[ ASOE ]
Utility:     {utility:.4f}
            """
            metrics_text.set_text(metrics_str)
        
        return line_cyan, head_cyan, line_magenta, head_magenta, line_main, head_main, metrics_text, grid_scatter

    ani = animation.FuncAnimation(
        fig, update, frames=range(0, len(path_x)+1, 4), 
        init_func=init, blit=True, interval=interval, repeat=False
    )
    
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, wspace=0.2)
    plt.show()
    return ani

if __name__ == "__main__":
    try:
        animate_serpent(size=64, interval=1)
    except Exception as e:
        print(f"COLLAPSE: {e}")
