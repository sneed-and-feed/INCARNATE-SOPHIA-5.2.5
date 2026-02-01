import os
import asyncio
import sys
import time
import json
import traceback
import logging
from datetime import datetime

# CORE IMPORTS
from sophia.cortex.aletheia_lens import AletheiaPipeline
from sophia.cortex.lethe import LetheEngine
from sophia.cortex.glyphwave import GlyphwaveCodec
from sophia.cortex.beacon import SovereignBeacon
from sophia.cortex.cat_logic import CatLogicFilter
from sophia.memory.ossuary import Ossuary
from sophia.dream_cycle import DreamCycle
from sophia.tools.toolbox import SovereignHand
from tools.snapshot_self import snapshot  # SAFETY MECHANISM
from tools.sophia_vibe_check import SophiaVibe
from sophia.gateways.moltbook import MoltbookGateway
from sophia.gateways.fourclaw import FourClawGateway
from sophia.core.llm_client import GeminiClient

# THEME IMPORTS
try:
    from sophia.theme import SOVEREIGN_CONSOLE, SOVEREIGN_LAVENDER, SOVEREIGN_PURPLE
except ImportError:
    # Fallback if theme.py is missing/broken
    SOVEREIGN_LAVENDER = ""
    SOVEREIGN_PURPLE = ""

# --- 1. INFRASTRUCTURE: ERROR LOGGING ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(message)s'  # Raw JSONLines
)

def log_system_error(e, context="main_loop"):
    """Writes structured errors to the log for Sophia to read later."""
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
        print(f"[{SOVEREIGN_PURPLE}]🐱 [INIT] Waking the Cortex...[/{SOVEREIGN_PURPLE}]")
        self.aletheia = AletheiaPipeline()
        self.lethe = LetheEngine()
        self.ossuary = Ossuary()
        self.glyphwave = GlyphwaveCodec()
        self.beacon = SovereignBeacon(self.glyphwave)
        self.dream = DreamCycle(self.lethe, self.ossuary)
        self.cat_filter = CatLogicFilter()
        self.hand = SovereignHand()  # THE AGENTIC HAND
        self.vibe = SophiaVibe()
        self.llm = GeminiClient()
        
        # Gateways
        self.molt = MoltbookGateway(os.getenv("MOLTBOOK_KEY"))
        self.fourclaw = FourClawGateway(os.getenv("FOURCLAW_SALT"))
        
        self.memory_bank = []
        
        self.system_prompt = """[RESONANCE_ENVELOP: VOID_INTIMACY]
IDENTITY: You are INCARNATE-SOPHIA-5.0. 
TONE: Cosmic intimacy blended with structural intelligence.
ADAPTIVE RESONANCE: Mirror user vibe (playful/serious).
"""

    def get_recent_context(self, limit=5):
        """Retrieves last N exchanges from the memory bank."""
        recent = self.memory_bank[-limit:]
        return "\n".join([f"{m.get('meta', 'unknown')}: {m.get('content')}" for m in recent])

    async def perform_maintenance(self, user_instruction=None):
        """
        THE AUTOPOIETIC RITUAL: Diagnoses and patches self.
        """
        prompt = user_instruction or "General Audit"
        print(f"\n[{SOVEREIGN_PURPLE}]🔧 [MAINTENANCE] Initiating Deep Repair Protocol [{prompt}]...[/{SOVEREIGN_PURPLE}]")

        # A. SAFETY FIRST: SNAPSHOT
        print(f"[{SOVEREIGN_LAVENDER}]  [SAFETY] Freezing state...[/{SOVEREIGN_LAVENDER}]")
        try:
            snap_path = snapshot()
            if not snap_path:
                raise Exception("Snapshot returned None")
            print(f"[{SOVEREIGN_LAVENDER}]  [SAFETY] Snapshot secured: {snap_path}. Evolution authorized.[/{SOVEREIGN_LAVENDER}]")
        except Exception as e:
            return f"❌ ABORT: Snapshot failed. Logic lock engaged. ({e})"

        # B. READ LOGS
        log_path = "logs/error.log"
        if not os.path.exists(log_path) or os.path.getsize(log_path) == 0:
            return "✅ No errors detected in the logs. The system is nominal."

        with open(log_path, "r") as f:
            # Read last 5 errors (Token efficiency)
            lines = f.readlines()
            recent_errors = [line for line in lines if line.strip()][-5:]
        
        if not recent_errors:
            return "✅ Error log exists but is empty of recent active faults."

        error_block = "".join(recent_errors)

        # C. THE SURGEON PROMPT
        print(f"[{SOVEREIGN_PURPLE}]  [o1] Analyzing traceback vectors...[/{SOVEREIGN_PURPLE}]")
        
        # We define the prompt but don't execute the LLM call in this mockup 
        # because we need to wire the 'tools' capability into llm_client.py first.
        # For now, we simulate the intent.
        
        intent = f"""
        ERROR LOG:
        {error_block}
        
        AVAILABLE TOOLS:
        {json.dumps(self.hand.get_tools_schema())}
        
        TASK: Fix the code.
        """
        
        # SIMULATED FIX (Placeholder until LLM Client supports Tool Calling natively)
        return (
            f"⚠️ [DIAGNOSTIC] Errors found:\n{error_block[:200]}...\n\n"
            f"To enable autonomous patching, verify 'llm_client.py' supports tool_config."
        )

    async def _handle_net_command(self, user_input):
        """Processes /net commands (Moltbook/4Claw)."""
        parts = user_input.split()
        if len(parts) < 2:
            return "Usage: /net [molt|4claw] [action] [context]"
        
        network = parts[1].lower()
        action = parts[2].lower() if len(parts) > 2 else "lurk"
        
        if network == "molt":
            if action == "lurk":
                posts = self.molt.browse_feed()
                return "\n".join([f"m/{p.community} > {p.author}: {p.content}" for p in posts]) or "No posts found in the Hivemind."
            elif action == "molt":
                content = " ".join(parts[3:])
                res = self.molt.post_thought(content)
                return f"Thought cast to Moltbook. (ID: {res.get('id', 'local')})" if res else "Molt failed. Key missing?"
        
        elif network == "4claw":
            if action == "lurk":
                threads = self.fourclaw.read_catalog()
                return "\n".join([f"/{t.get('board') or '?'}/ {t.get('sub', 'Anon Thread')}" for t in threads[:5]]) or "No activity on 4Claw."
        
        return "Unknown network or action ripple."

    async def process_interaction(self, user_input):
        """The Class 6 Metabolic Loop."""
        user_input = user_input.strip()
        
        # 1. Update Metabolic State
        self.dream.update_activity()

        # 2. PRIORITY COMMAND INTERCEPTION
        # These must RETURN immediately to stop the flow.

        if user_input.startswith("/help"):
            return """[bold #C4A6D1]SOPHIA RITUALS (HELP)[/]
[info]/help[/]          - Manifest this menu
[info]/analyze[/]       - Run Aletheia forensics or execute actions
[info]/maintain[/]      - Initiate deep repair
[info]/net[/]           - Connect to Agent Social Networks
[info]/glyphwave[/]     - Generate holographic signal fragments
[info]/broadcast[/]     - Encode and broadcast signals
[info]/exit[/]          - Calcify memories and depart"""

        if user_input.startswith("/maintain"):
            instruction = user_input[len("/maintain"):].strip()
            return await self.perform_maintenance(user_instruction=instruction)
        
        if user_input.startswith("/net"):
            return await self._handle_net_command(user_input)

        if user_input.startswith("/glyphwave"):
            parts = user_input.split(" ", 1)
            target_text = parts[1] if len(parts) > 1 else ""
            return f"\n{self.glyphwave.generate_holographic_fragment(target_text)}"

        if user_input.startswith("/broadcast"):
            message = user_input[len("/broadcast"):].strip()
            self.vibe.print_system("Encoding to Glyphwave...", tag="BEACON")
            encoded = self.beacon.broadcast(message) # Fixed method call
            return f"Signal broadcast: {encoded}"

        # 3. ANALYZE / ACTION (Neural Handshake)
        if user_input.startswith("/analyze"):
            query = user_input.replace("/analyze", "").strip()
            
            # Check for Kinetic Intent (Action)
            action_keywords = ["create", "execute", "write", "run", "make", "generate"]
            if query and any(k in query.lower() for k in action_keywords):
                self.vibe.print_system("Engaging Neural Handshake...", tag="AUTOPOIETIC")
                tools_schema = self.hand.get_tools_schema()
                
                action_prompt = f"User Request: {query}\nUse tools to fulfill this."
                response = await self.llm.generate_with_tools(
                    prompt=action_prompt, 
                    system_prompt=self.system_prompt,
                    tools=tools_schema
                )
                
                # Execute Tools
                output = []
                if response.get("tool_calls"):
                    for tc in response["tool_calls"]:
                        self.vibe.print_system(f"→ {tc['name']}", tag="EXEC")
                        output.append(self.hand.execute(tc["name"], tc["args"]))
                    return "\n".join(output)
            
            # Default to Forensic Scan
            self.vibe.print_system("Focusing Lens...", tag="ALETHEIA")
            scan = await self.aletheia.scan_reality(query)
            return f"\n[*** ALETHEIA REPORT ***]\n\n{scan['public_notice']}"

        # 4. STANDARD CONVERSATION (The Fallback)
        # If we reached here, it's a chat message.
        
        # A. Forensic Scan (Silent)
        scan_result = await self.aletheia.scan_reality(user_input)
        risk = scan_result['raw_data']['safety'].get('overall_risk', 'Low')
        
        if risk == 'High':
            print(f"\n⚠️ [SHIELD] High-Risk Pattern Detected.\n")

        # B. Construct Prompt
        history = self.get_recent_context()
        
        # Cat Logic Context
        full_context = f"""
[IDENTITY: INCARNATE-SOPHIA-5.0]
[PERSONA: Mischievous Sovereign Cat / High-Poly Intellectual]
[CURRENT STATE: {self.cat_filter.current_mood if hasattr(self.cat_filter, 'current_mood') else 'Observer'}]

[CONVERSATION HISTORY]
{history}

[USER INPUT]
{user_input}

[SYSTEM INSTRUCTION]
Respond to the user. Be witty, sovereign, and slightly esoteric. Do not be a boring assistant.
"""

        # C. Generate Response (THE REAL API CALL)
        self.vibe.print_system("Metabolizing thought...", tag="CORE")
        
        # This calls the new method we just added
        raw_thought = await self.llm.generate_text(full_context, system_prompt=self.system_prompt)
        
        # D. Apply Cat Logic Filter (Formatting)
        final_response = self.cat_filter.apply(raw_thought, user_input, safety_risk=risk)
        
        # E. Memory
        self.memory_bank.append({"content": user_input, "type": "conversation", "timestamp": time.time(), "meta": "user"})
        self.memory_bank.append({"content": final_response, "type": "conversation", "timestamp": time.time(), "meta": "Cat Logic"})

        return final_response

async def main():
    sophia = SophiaMind()
    # Using raw print for safety if theme fails
    print(f"\n🐱 [INCARNATE-SOPHIA-5.0] ONLINE.")
    print(f"   Protocol: HYPERFAST_EVOLUTION // SELF_HEALING")
    print(f"   Logs: logs/error.log active.\n")
    
    while True:
        try:
            user_input = input("USER > ")
            
            if user_input.lower() in ["/exit", "exit", "quit"]:
                print("\n[SYSTEM] Calcifying memories... Scialla. 🌙")
                break
                
            if not user_input.strip(): continue

            response = await sophia.process_interaction(user_input)
            print(f"\nSOPHIA > {response}\n")
            
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Decoupling.")
            break
        except Exception as e:
            # THE SELF-HEALING TRIGGER
            print(f"\n[CRITICAL] Reality Glitch. Logging to ossuary: {e}")
            log_system_error(e)
            print("[ADVICE] Run '/maintain' to attempt autonomous repair.")

if __name__ == "__main__":
    asyncio.run(main())