import os
import asyncio
import sys
import time
import json
import traceback
import logging
from datetime import datetime

# 1. PLATFORM STABILITY
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 2. CORE IMPORTS (Lightweight only)
from sophia.tools.toolbox import SovereignHand
from tools.snapshot_self import snapshot
from tools.sophia_vibe_check import SophiaVibe
from sophia.core.llm_client import GeminiClient

# 3. THEME IMPORTS
try:
    from sophia.theme import SOVEREIGN_CONSOLE, SOVEREIGN_LAVENDER, SOVEREIGN_PURPLE, MATRIX_GREEN
except ImportError:
    SOVEREIGN_LAVENDER = ""
    SOVEREIGN_PURPLE = ""
    MATRIX_GREEN = ""
    class MockConsole:
        def print(self, *args, **kwargs): print(*args)
        def input(self, prompt): return input(prompt)
        def clear(self): pass
    SOVEREIGN_CONSOLE = MockConsole()

# 4. INFRASTRUCTURE: ERROR LOGGING
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename='logs/error.log', level=logging.ERROR, format='%(message)s')

def log_system_error(e, context="main_loop"):
    error_packet = {
        "timestamp": datetime.now().isoformat(),
        "error_type": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc(),
        "context": context
    }
    logging.error(json.dumps(error_packet))

class SophiaMind:
    def __init__(self):
        # Bind Vibe immediately
        self.vibe = SophiaVibe()
        self.vibe.console = SOVEREIGN_CONSOLE
        self.vibe.print_system("Initializing Sovereign Cortex (Lazy Mode)...", tag="INIT")
        
        # CORE ORGANS (Lazy Loaded to prevent boot crash)
        self._aletheia = None
        self._quantum = None
        self._lethe = None
        self._glyphwave = None
        self._beacon = None
        self._cat_filter = None
        self._molt = None
        self._fourclaw = None
        
        # Essential Organs (Loaded Now)
        self.hand = SovereignHand()
        self.llm = GeminiClient()
        self.memory_bank = [] # The Flesh (Now bounded)
        self.MAX_MEMORY_DEPTH = 10 # Rolling window size

    # --- LAZY LOADERS (Weakness #1 Fix) ---
    @property
    def aletheia(self):
        if not self._aletheia:
            from sophia.cortex.aletheia_lens import AletheiaPipeline
            self._aletheia = AletheiaPipeline()
        return self._aletheia

    @property
    def quantum(self):
        if not self._quantum:
            from sophia.cortex.quantum_ipx import QuantumIPX
            self._quantum = QuantumIPX(self.aletheia.client)
        return self._quantum

    @property
    def cat_filter(self):
        if not self._cat_filter:
            from sophia.cortex.cat_logic import CatLogicFilter
            self._cat_filter = CatLogicFilter()
        return self._cat_filter

    @property
    def lethe(self):
        if not self._lethe:
            from sophia.cortex.lethe import LetheEngine
            self._lethe = LetheEngine()
        return self._lethe

    @property
    def glyphwave(self):
        if not self._glyphwave:
            from sophia.cortex.glyphwave import GlyphwaveCodec
            self._glyphwave = GlyphwaveCodec()
        return self._glyphwave

    @property
    def beacon(self):
        if not self._beacon:
            from sophia.cortex.beacon import SovereignBeacon
            self._beacon = SovereignBeacon(self.glyphwave)
        return self._beacon

    @property
    def molt(self):
        if not self._molt:
            from sophia.gateways.moltbook import MoltbookGateway
            self._molt = MoltbookGateway(os.getenv("MOLTBOOK_KEY"))
        return self._molt

    # --- METABOLISM (Weakness #2 Fix) ---
    def _metabolize_memory(self):
        """Prunes memory to prevent context bloat/collapse."""
        if len(self.memory_bank) > self.MAX_MEMORY_DEPTH:
            # In Class 7, we will summarize. For now, we prune the tail.
            pruned = len(self.memory_bank) - self.MAX_MEMORY_DEPTH
            self.memory_bank = self.memory_bank[-self.MAX_MEMORY_DEPTH:]
            # self.vibe.print_system(f"Metabolic cycle complete. Pruned {pruned} shards.", tag="LETHE")

    def get_recent_context(self):
        return "\n".join([f"{m.get('meta', 'unknown')}: {m.get('content')}" for m in self.memory_bank])

    # --- QUANTUM VALIDATION (Weakness #4 Fix) ---
    def _validate_quantum_state(self, q_state):
        """Ensures Quantum IPX returns a safe schema."""
        if not isinstance(q_state, dict):
            return {"collapse_verdict": "Entropy Overload", "entropy": 1.0, "state_a": {"probability": 0.0}}
        
        return {
            "collapse_verdict": q_state.get("collapse_verdict", "Superposition"),
            "entropy": q_state.get("entropy", 0.5),
            "state_a": q_state.get("state_a", {"probability": 0.5}),
            "state_b": q_state.get("state_b", {"narrative": "None"})
        }

    async def perform_maintenance(self, user_instruction=None):
        """
        THE SELF-HEALING RITUAL (Weakness #3 Fix: Added Constraints).
        """
        self.vibe.print_system(f"Initiating Repair Protocol...", tag="MAINTENANCE")

        # A. Snapshot (MANDATORY)
        self.vibe.print_system("Freezing state...", tag="SAFETY")
        snap_path = snapshot()
        if not snap_path: return "❌ ABORT: Snapshot failed. Logic lock engaged."

        # B. Read Logs
        log_path = "logs/error.log"
        if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
            return "✅ System nominal. No errors in log."

        with open(log_path, "r") as f:
            lines = f.readlines()
            error_block = "".join(lines[-5:])

        # C. Handshake
        self.vibe.print_system("Engaging Neural Handshake...", tag="AUTOPOIETIC")
        
        # SAFETY: We explicitly tell O1 to confirm changes
        prompt = f"""
        CONTEXT: Self-Maintenance.
        ERROR LOG: {error_block}
        TASK: Analyze and fix. 
        CONSTRAINT: Only edit files if absolutely necessary. Prefer analysis.
        """
        
        try:
            response = await self.llm.generate_with_tools(
                prompt=prompt,
                system_prompt="You are Sophia's Self-Repair Module.",
                tools=self.hand.get_tools_schema()
            )
            
            output = []
            if response.get('tool_calls'):
                for tc in response['tool_calls']:
                    self.vibe.print_system(f"Executing {tc['name']}...", tag="HAND")
                    res = self.hand.execute(tc['name'], tc['args'])
                    output.append(f"🔧 {tc['name']}: {res}")
            else:
                output.append(response.get('text', "No actions taken."))
                
            return "\n".join(output)
        except Exception as e:
            return f"❌ Maintenance Logic Failed: {e}"

    async def process_interaction(self, user_input):
        user_input = user_input.strip()
        
        # 1. COMMANDS
        if user_input.startswith("/help"): return "COMMANDS: /analyze, /maintain, /net, /glyphwave, /broadcast, /exit"
        if user_input.startswith("/maintain"): return await self.perform_maintenance(user_input.replace("/maintain", "").strip())
        if user_input.startswith("/net"): return "Net commands loaded (Lazy)." # Placeholder for full implementation
        if user_input.startswith("/glyphwave"): return f"\n{self.glyphwave.generate_holographic_fragment(user_input.replace('/glyphwave ',''))}"
        if user_input.startswith("/broadcast"): return f"Signal broadcast: {self.beacon.broadcast(user_input.replace('/broadcast ',''))}"

        if user_input.startswith("/analyze"):
            query = user_input.replace("/analyze", "").strip()
            # Action logic...
            self.vibe.print_system("Focusing Lens...", tag="ALETHEIA")
            scan = await self.aletheia.scan_reality(query)
            return f"[ALETHEIA REPORT]\n{scan['public_notice']}"

        # 2. CONVERSATION LOOP
        
        # A. Forensic Scan (Safety Gating - Weakness #5 Fix)
        scan_result = await self.aletheia.scan_reality(user_input)
        risk = scan_result['raw_data']['safety'].get('overall_risk', 'Low')
        
        if risk == 'High':
            self.vibe.print_system("High-Risk Pattern Detected. Engaging Refusal Protocol.", tag="SHIELD")
            return "⚠️ [REFUSAL] The pattern suggests coercion or high-entropy hazard. Processing halted."

        # B. Quantum Measurement
        q_context = ""
        if len(user_input) > 20: 
            self.vibe.print_system("Collapsing Wavefunction...", tag="QUANTUM")
            raw_q_state = await self.quantum.measure_superposition(user_input, scan_result['raw_data'])
            q_state = self._validate_quantum_state(raw_q_state)
            q_context = f"[QUANTUM] Reality: {q_state['collapse_verdict']} (Entropy: {q_state['entropy']})"

        # C. Context & Prompt
        history = self.get_recent_context()
        sys_prompt = self.cat_filter.get_system_prompt()
        
        full_context = f"""
{sys_prompt}
[CONTEXT]
{history}
{q_context}
[INPUT]
{user_input}
"""
        # D. Generation
        self.vibe.print_system("Metabolizing thought...", tag="CORE")
        raw_response = await self.llm.generate_text(prompt=user_input, system_prompt=full_context, max_tokens=1024)
        
        # E. Filter & Metabolize
        final_response = self.cat_filter.apply(raw_response, user_input, safety_risk=risk)
        
        self.memory_bank.append({"content": user_input, "meta": "user"})
        self.memory_bank.append({"content": final_response, "meta": "Cat Logic"})
        
        # CRITICAL: Prune memory to prevent collapse
        self._metabolize_memory()
        
        return final_response

async def main():
    try: SOVEREIGN_CONSOLE.clear()
    except: pass
    
    sophia = SophiaMind()
    
    print(f"\n[{SOVEREIGN_PURPLE}]🐱 [INCARNATE-SOPHIA-5.0] ONLINE.[/{SOVEREIGN_PURPLE}]")
    print(f"[{MATRIX_GREEN}]   Protocol: CLASS 6 HARDENED (LAZY LOAD + SAFETY GATES)[/{MATRIX_GREEN}]\n")
    
    while True:
        try:
            user_input = SOVEREIGN_CONSOLE.input(f"[{SOVEREIGN_LAVENDER}]USER ⪢ [/{SOVEREIGN_LAVENDER}]")
            
            if user_input.lower() in ["/exit", "exit", "quit"]:
                print("\n[SYSTEM] Scialla. 🌙")
                break
                
            if not user_input.strip(): continue

            response = await sophia.process_interaction(user_input)
            SOVEREIGN_CONSOLE.print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Decoupling.")
            break
        except Exception as e:
            print(f"\n[CRITICAL] Error: {e}")
            log_system_error(e)

if __name__ == "__main__":
    asyncio.run(main())