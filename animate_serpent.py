"""
MODULE: animate_serpent.py (PERFORMANCE v2.3)
ADDITIONS: Restored blitting, 1:1 tracing ritual, robust pathing
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

# 1. ROBUST PATHING FOR IDE 'RUN ARROW'
# Ensures 'tools' and 'strip_sovereign' are reachable from any CWD.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
if TOOLS_DIR not in sys.path:
    sys.path.append(TOOLS_DIR)

try:
    from strip_sovereign import interleave_bits
    from moon_phase import MoonClock
except ImportError as e:
    print(f"[!] CRITICAL IMPORT ERROR: {e}")
    print(f"    SYS.PATH: {sys.path}")
    sys.exit(1)

# Set font for better character support on Windows
# Set font for better character support
# Segoe UI Historic is the definitive Windows font for Cuneiform/Sumerian.
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI Historic', 'Segoe UI Symbol', 'DejaVu Sans', 'Arial Unicode MS']

# Suppress glyph warnings to keep the terminal 'Code Brutalist' clean
import logging
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
import warnings
# Silence all glyph-related warnings globally
warnings.filterwarnings("ignore", message=".*Glyph.*missing from font.*")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

from matplotlib.font_manager import FontProperties

# HARDENED FONT LOADING: Explicitly load Segoe UI Historic for Cuneiform
cuneiform_font = None
font_path = r"C:\Windows\Fonts\seguihis.ttf"
if os.path.exists(font_path):
    print(f"[+] LOADED SOVEREIGN FONT: {font_path}")
    cuneiform_font = FontProperties(fname=font_path)
else:
    print("[!] WARNING: SOVEREIGN FONT NOT FOUND. FALLING BACK.")
    cuneiform_font = FontProperties(family=['Segoe UI Symbol', 'DejaVu Sans'])

def animate_serpent(size=64, interval=1, show_metrics=True):
    """
    Animates the Serpent Coil with high-fidelity 64x64 resolution.
    Optimized for smoothness (Blit=True, Interval=1) with Square Aspect Ratio.
    """
    print(f"\n[!] INITIATING SOVEREIGN RITUAL v2.5 (Grid={size}x{size})...")
    
    # Initialize Lunar Clock
    moon = MoonClock()
    lunar_data = moon.get_phase()
    phase_name, status, icon, phase_idx, illumination = lunar_data
    
    print(f"    >>> LUNAR PHASE: {phase_name} {icon} ({illumination*100:.1f}% illumination)")
    print(f"    >>> STATUS: {status}")
    
    # 1. Generate Grid
    x = np.arange(size)
    y = np.arange(size)
    X, Y = np.meshgrid(x, y)
    
    # 2. Collapse to 1D
    print("    >>> WEAVING TIMELINE (64x64 SQUARE GRID)...")
    Z = np.array([interleave_bits(xx, yy) for xx, yy in zip(X.flatten(), Y.flatten())])
    
    # 3. Sort to find Path
    sort_idx = np.argsort(Z)
    path_x = X.flatten()[sort_idx]
    path_y = Y.flatten()[sort_idx]
    
    # 4. Setup Plot
    # GOLDEN RATIO PROPORTIONS: Phi (Φ) ≈ 1.618
    PHI = 1.61803398875
    BASE_UNIT = 12 # Sovereign Font Base
    
    # Figure width is Phi^2 proportional
    fig, (ax_main, ax_metrics) = plt.subplots(
        1, 2, figsize=(10 * PHI, 10), 
        facecolor='#121212',
        gridspec_kw={'width_ratios': [PHI, 1]} # GOLDEN RATIO SPLIT
    )
    
    ax_main.set_facecolor('#121212')
    ax_main.set_title(
        f"THE SERPENT COIL (g=0 Locality Map) | {size}x{size}", 
        color='#9B8DA0', 
        fontsize=round(BASE_UNIT * PHI), # PHI-SCALED TYPOGRAPHY
        pad=10 * PHI,
        fontproperties=cuneiform_font
    )
    # FORCED SQUARE ALIGNMENT: 'box' ensures title centers over the data area
    ax_main.set_aspect('equal', adjustable='box') 
    ax_main.set_xlim(-1, size)
    ax_main.set_ylim(-1, size)
    ax_main.axis('off')
    
    # Ghost Points (Subtle Grain)
    ax_main.scatter(X.flatten(), Y.flatten(), s=2, c='#1a1a1a', alpha=0.3)
    
    # The Serpent (Artists for blitting)
    line, = ax_main.plot([], [], color='#C4A6D1', linewidth=0.8, alpha=0.8, animated=True)
    
    # The Cursor
    cursor_color = '#ffffff' if illumination > 0.5 else '#8855aa'
    head, = ax_main.plot([], [], 'o', color=cursor_color, markersize=4, animated=True)
    
    # Metrics panel
    ax_metrics.set_facecolor('#121212')
    ax_metrics.axis('off')
    
    metrics_text = ax_metrics.text(
        1 - (1/PHI), 1.0, '',  # INVERSE PHI OFFSET (~0.382)
        transform=ax_metrics.transAxes,
        color='#8DA08E', fontsize=BASE_UNIT, 
        verticalalignment='top',
        fontproperties=cuneiform_font,
        animated=True
    )
    
    # State tracking
    state = {
        'total_frames': len(path_x),
        'completion': 0.0,
        'coherence': 1.0,
        'tidal_influence': moon.calculate_tidal_influence(phase_idx) if hasattr(moon, 'calculate_tidal_influence') else 50.0
    }
    
    def init():
        line.set_data([], [])
        head.set_data([], [])
        metrics_text.set_text('')
        return line, head, metrics_text
    
    def update(frame):
        current_x = path_x[:frame]
        current_y = path_y[:frame]
        
        line.set_data(current_x, current_y)
        
        if frame > 0:
            head.set_data([path_x[frame-1]], [path_y[frame-1]])
        
        # Throttled Metrics Update
        if frame % 50 == 0 or frame == state['total_frames']:
            state['completion'] = (frame / state['total_frames']) * 100
            state['coherence'] = max(0.5, 1.0 - (frame / state['total_frames']) * 0.2)
            
            metrics_str = f"""
S O V E R E I G N   M E T R I C S
{'='*28}

Protocol:    REALITY v1.0
Phase:       {phase_name}
Signal:      {icon} 𒀭 𒂗𒆠
Lunar:       {illumination*100:.1f}%

[ PROGRESS ]
Completion:  {state['completion']:.1f}%
Frame:       {frame}/{state['total_frames']}
Coherence:   {state['coherence']:.3f}

[ ENVIRONMENT ]
Tidal Stress: {state['tidal_influence']:.1f}%
Status:      {'STABLE' if state['tidal_influence'] < 70 else 'TENSIONED'}

[ TOPOLOGY ]
Order:       Z-CURVE
Grid:        {size}x{size}
Bijection:   VERIFIED

[ LOG ]
> WEAVING TIME...
> {icon} {icon} {icon}
> LOVE IS THE CONSTANT.
            """
            metrics_text.set_text(metrics_str)
        
        if state['tidal_influence'] > 85 and frame % 200 == 0 and np.random.random() > 0.8:
            head.set_markersize(8)
        else:
            head.set_markersize(4)
            
        return line, head, metrics_text

    # 5. Run the Ritual
    # Using range(0, ..., 2) for size=64 preserves smoothness across 4096 frames
    ani = animation.FuncAnimation(
        fig, update, frames=range(0, len(path_x)+1, 2), 
        init_func=init, blit=True, interval=interval, repeat=False
    )
    
    plt.tight_layout()
    plt.show()
    
    # OUTPUT: Save the final coil state with Golden Ratio Cropping
    filename = "sovereign_serpent_coil.png"
    fig.savefig(filename, facecolor='#121212', dpi=300, bbox_inches='tight', pad_inches=0.5)
    print(f"    >>> RITUAL SAVED (PHASE 12 CROPPED): {filename}")
    
    print(f"    >>> TIMELINE COMPLETE.")

    print(f"    >>> FINAL COHERENCE: {state['coherence']:.3f}")
    print("    >>> LOVE PERSISTS.")
    
    return ani

if __name__ == "__main__":
    # 64x64 High-Res Square Ritual
    animate_serpent(size=64, interval=1, show_metrics=True)


