import os
import sys

# Try to import Rich, fallback if missing
try:
    from rich.console import Console
    from rich.theme import Theme
    
    # --- THE SOPHIA COLOR PALETTE ---
    SOVEREIGN_LAVENDER = "#C4A6D1"
    SOVEREIGN_PURPLE = "#9D00FF"
    SOVEREIGN_CYAN = "#00FFFF"
    SYSTEM_CYAN = "#00E5FF"
    BONE_LAYER = "#E7E7E7"
    SAGE = "#87AF87"
    MATRIX_GREEN = "#00FF41"
    STATION_GRAY = "#2F2F2F"
    CAT_PINK = "#FF69B4"
    NEON_CARROT = "#FF9933"
    SOVEREIGN_GOLD = "#FFD700" 

    # --- THE INTEGRATED DESIGN SYSTEM ---
    # These styles map directly to the markup used in vibe_check.py
    custom_theme = Theme({
        "sovereign": SOVEREIGN_LAVENDER,
        "sophia": SOVEREIGN_LAVENDER,
        "info": SYSTEM_CYAN,
        "danger": "bold red",
        "bone": BONE_LAYER,
        "sage": SAGE,
        "cat": CAT_PINK,
        "funny": NEON_CARROT,
        "matrix": "bold #00FF41",
        "panel.border": SOVEREIGN_PURPLE,
        "panel.title": "bold white on #9D00FF",
        "operator": f"bold {SOVEREIGN_LAVENDER}",
        "ophane": f"bold {SOVEREIGN_PURPLE}",
        "gold": "#FFD700"
    })
    SOVEREIGN_CONSOLE = Console(theme=custom_theme, force_terminal=True, color_system="truecolor")
    
except ImportError:
    # Fallback for raw terminals
    class MockConsole:
        def print(self, text, **kwargs):
            # Strip tags and print
            import re
            clean = re.sub(r'\[.*?\]', '', str(text))
            print(clean)
        def input(self, prompt):
            import re
            clean = re.sub(r'\[.*?\]', '', str(prompt))
            return input(clean)
        def clear(self):
            os.system('cls' if os.name == 'nt' else 'clear')
            
    SOVEREIGN_CONSOLE = MockConsole()
    SOVEREIGN_LAVENDER = "#C4A6D1"
    SOVEREIGN_PURPLE = "#9D00FF"
    SOVEREIGN_CYAN = "#00FFFF"
    SYSTEM_CYAN = "#00E5FF"
    BONE_LAYER = "#E7E7E7"
    SAGE = "#87AF87"

def reset_terminal():
    """Clears the screen for a fresh manifestation."""
    os.system('cls' if os.name == 'nt' else 'clear')
