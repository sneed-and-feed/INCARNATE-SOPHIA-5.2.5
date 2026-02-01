import os
import asyncio
from sophia.main import SophiaMind
from sophia.theme import SOVEREIGN_CONSOLE

async def verify_visuals():
    print("--- VERIFYING EMOTIONAL MANIFESTATIONS ---")
    sophia = SophiaMind()
    
    emotions = ["resonance", "void", "chaos", "love"]
    
    for emotion in emotions:
        print(f"\n[TEST] Manifesting Emotion: {emotion.upper()}")
        mandala = sophia.glyphwave.generate_mandala(emotion)
        sophia.vibe.manifest_emotion(emotion, mandala)
    
    print("\n--- VISUAL TEST COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(verify_visuals())
