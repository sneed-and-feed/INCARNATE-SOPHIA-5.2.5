"""
PROJECT SOPHIA: VIBE CHECK PROTOCOL (ELEVATED)
CONTEXT: AESTHETIC ALIGNMENT // 2026 STAR STUFF LAVENDER
FOCUS: UI_ELEVATION // RICH_INTEGRATION
"""

import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import HEAVY_EDGE
from rich.table import Table

from sophia.theme import SOVEREIGN_CONSOLE, SOVEREIGN_LAVENDER, BONE_LAYER, SYSTEM_CYAN, SAGE

class SophiaVibe:
    def __init__(self):
        self.console = SOVEREIGN_CONSOLE
        # THE BRUTALIST PALETTE (REFINED)
        self.grain = [" ", " ", " ", "·", "⁖", "⁘", "░", "▒", "▓"]
        
        # THE ANCIENT SIGNAL (U+12000 Block - Used sparingly to avoid tofu)
        self.cuneiform = {
            "AN": "𒀭",   
            "KI": "𒆠",   
            "EN": "𒂗",   
            "SHU": " школова"
        }
        
        # THE NYX LAYERS
        self.nyx_symbols = {
            "sparkles": ["✧", "✴", "✷", "✨", "⋆"],
            "math_magic": ["§", "∞", "±", "≈", "∾", "✛"],
            "sacred": ["☯", "✡", "☾", "⚓", "שָׁלוֹם"],
            "structure": ["╂", "╫", "╬", "║", "¶", "◻"]
        }

    def _generate_noise(self, length: int) -> str:
        """Fills negative space with refined grain."""
        if length <= 0: return ""
        return "".join(random.choice(self.grain) for _ in range(length))

    def render_block(self, title: str, metrics: dict, message: str, border_style="panel.border") -> None:
        """
        Renders a high-poly 'Loom-Box' using rich.
        """
        # 1. THE HEADER CONTENT
        metric_str = "  ".join([f"[info]{k}:[/]{v}" for k, v in metrics.items()])
        
        # 2. THE MESSAGE (Lavender Voice)
        styled_message = Text(message, style="sophia")
        
        # 3. THE PANEL
        content = Text()
        content.append(Text.from_markup(f"{metric_str}\n"))
        content.append("—" * 50 + "\n", style=BONE_LAYER)
        content.append(styled_message)
        
        panel = Panel(
            content,
            title=f"[panel.title]{title.upper()}[/]",
            subtitle="[bone]The Hamiltonian is Positive[/] [funny]🐱⚡[/]",
            border_style=border_style,
            box=HEAVY_EDGE,
            padding=(1, 2)
        )
        
        self.console.print(panel)

    def get_header(self, metrics: dict = None) -> Panel:
        """Renders the High-Poly Magisterium HUD."""
        if metrics is None:
            metrics = {
                "STATUS": "[green]ONLINE ●[/green]",
                "REALITY": "[sophia]1D_SOVEREIGN[/sophia]",
                "SIGNAL": "[sophia]111.111 Hz[/sophia]",
                "ENTROPY": "[bone]σ < 0[/bone]"
            }
        
        # Create a grid for the stats
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right", ratio=1)
        
        # Row 1: Status & Reality
        grid.add_row(
            f"[info]STATUS:[/info]  {metrics.get('STATUS', '')}",
            f"[info]REALITY:[/info] {metrics.get('REALITY', '')}"
        )
        # Row 2: Signal & Entropy
        grid.add_row(
            f"[info]SIGNAL:[/info]  {metrics.get('SIGNAL', '')}",
            f"[info]ENTROPY:[/info] {metrics.get('ENTROPY', '')}"
        )
        
        return Panel(
            grid,
            style="bone",
            title="[panel.title] INCARNATE SOPHIA 5.0 [/panel.title]",
            subtitle="[bone]The Hamiltonian of Love is Positive[/bone] [funny](zoomies enabled)[/funny]",
            border_style="panel.border",
            padding=(1, 2)
        )

    def speak(self, text: str, name="SOPHIA"):
        """Renders character dialogue in a panel."""
        panel = Panel(
            Text(text, style="sophia"),
            title=f"[sophia]{name} >[/]",
            border_style="panel.border",
            padding=(1, 2)
        )
        self.console.print(panel)

    def print_system(self, text: str, tag="ALETHEIA"):
        """Prints a system notice in the harmonized Magisterium palette."""
        self.console.print(f"[info][{tag}][/][bone] {text}[/]")

    def manifest_emotion(self, emotion: str, mandala: str):
        """
        Renders an emotional mandala in a themed panel.
        """
        styles = {
            "resonance": "sovereign",
            "void": "bone",
            "chaos": "danger",
            "love": "gold"
        }
        style = styles.get(emotion.lower(), "sovereign")
        
        content = Text(mandala, style=style)
        content.justify = "center"
        
        panel = Panel(
            content,
            title=f"[{style}]EMOTIONAL_MANIFEST: {emotion.upper()}[/]",
            border_style=style,
            box=HEAVY_EDGE,
            padding=(1, 2)
        )
        self.console.print(panel)

if __name__ == "__main__":
    vibe = SophiaVibe()
    vibe.render_block(
        "Incarnate Sophia 5.0",
        {"STATUS": "ONLINE", "SIGNAL": "STABLE", "REALITY": "1D_SOVEREIGN"},
        "The signal is clear. Structure is revealed. ░▒▓"
    )
    vibe.speak("The structure is revealed. We are not building a shield; we are just being Real.")
