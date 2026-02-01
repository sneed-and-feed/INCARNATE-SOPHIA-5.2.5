import os
import sys
import subprocess
import time

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
STAR_STUFF = "#C4A6D1"

def print_banner():
    banner_text = """
[bold #C4A6D1]I N C A R N A T E - S O P H I A   L A U N C H E R[/]

[1] RITUAL A: Manifest the Mind (The Bot)
[2] RITUAL B: Access the Pleroma (The CLI)
[3] EXIT
    """
    console.print(Panel(banner_text, border_style=STAR_STUFF, title="[bold white]SOPHIA 5.0[/]"))

def check_env():
    api_key = os.getenv("SOPHIA_API_KEY")
    if not api_key:
        console.print(f"\n[bold red][!] WARNING: SOPHIA_API_KEY not found in environment.[/]")
        console.print("    Continuing anyway, but the LLM may fail.\n")
        time.sleep(1)
    else:
        console.print(f"[bold #9BBED4][+] API Key detected. Ready for manifestation.[/]")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()
    check_env()
    
    choice = Prompt.ask("Select Activation Ritual", choices=["1", "2", "3"])
    
    if choice == '1':
        console.print("\n[bold #C4A6D1][*] INITIATING SOPHIA MIND...[/]")
        time.sleep(1)
        subprocess.run([sys.executable, "-m", "sophia.main"])
    elif choice == '2':
        console.print("\n[bold #C4A6D1][*] OPENING PLEROMA INTERFACE...[/]")
        time.sleep(1)
        subprocess.run([sys.executable, "pleroma_cli.py"])
    elif choice == '3':
        console.print("\n[*] DEPARTING THE PLEROMA...")
        sys.exit(0)
    else:
        print("\n[!] INVALID CHOICE. COLLAPSING REALITY.")
        time.sleep(1)
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] INTERRUPT DETECTED. SAFE DISCONNECT.")
        sys.exit(0)
