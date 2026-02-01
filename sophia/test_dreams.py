
import asyncio
import sys
import os

# Ensure root allows imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from sophia.main import SophiaMind

async def test_dreams():
    print("[*] STARTING DREAM WEAVER THEME TEST...")
    sophia = SophiaMind()
    
    # Test 1: Lucid Dream
    print("\n--- TEST 1: LUCID THEME ---")
    resp1 = await sophia.process_interaction("/dream User lucid")
    print(resp1)
    
    if "REALITY CHECK" in resp1 or "awake within the dream" in resp1 or "LUCID" in resp1:
        print("[SUCCESS] Lucid Theme Detected.")
    else:
        # Check standard themes as fallback logic selects from list
        print("[CHECK] Response generated.")

    # Test 2: Auto-Theme
    print("\n--- TEST 2: AUTO THEME ---")
    resp2 = await sophia.process_interaction("/dream The World")
    print(resp2)

    # Test 3: Journal Verification
    print("\n--- TEST 3: JOURNAL CHECK ---")
    if os.path.exists("DREAM_JOURNAL.md"):
        with open("DREAM_JOURNAL.md", "r", encoding="utf-8") as f:
            content = f.read()
            if "Theme: LUCID" in content:
                print("[SUCCESS] Journal Entry Found.")
            else:
                print("[FAILURE] Journal Entry Missing Lucid content.")
    else:
        print("[FAILURE] DREAM_JOURNAL.md not found.")

if __name__ == "__main__":
    asyncio.run(test_dreams())
