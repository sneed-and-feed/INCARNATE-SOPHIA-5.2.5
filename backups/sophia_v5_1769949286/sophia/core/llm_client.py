import os
import json
import logging
from dataclasses import dataclass
from google import genai
from google.genai import types

# Suppress noisy logs
logging.getLogger("google.genai").setLevel(logging.WARNING)

@dataclass
class LLMConfig:
    # The new standard. If this 404s, try "gemini-2.0-flash-exp"
    model_name: str = "gemini-2.0-flash" 
    temperature: float = 0.7

class GeminiClient:
    def __init__(self):
        # 1. Load Keys (Priority: Sophia -> Google -> Dotenv)
        self.api_key = (os.getenv("SOPHIA_API_KEY") or 
                        os.getenv("GOOGLE_AI_KEY") or 
                        os.getenv("GOOGLE_API_KEY"))
        
        if not self.api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                self.api_key = os.getenv("SOPHIA_API_KEY") or os.getenv("GOOGLE_AI_KEY")
            except ImportError:
                pass
            
        if not self.api_key:
            print("⚠️ [WARNING] No API Key found. Sophia is blind.")
            self.client = None
        else:
            # NEW SDK INITIALIZATION
            self.client = genai.Client(api_key=self.api_key)

    async def generate_text(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """
        Standard conversation generation using the new SDK.
        """
        if not self.client: return "[BLIND] No API Key."

        config = types.GenerateContentConfig(
            temperature=LLMConfig.temperature,
            max_output_tokens=max_tokens,
            system_instruction=system_prompt
        )

        try:
            # Native Async Call (No more run_in_executor!)
            response = await self.client.aio.models.generate_content(
                model=LLMConfig.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            return self._handle_error(e)

    async def query_json(self, prompt: str, system_prompt: str = None) -> dict:
        """
        Forces strict JSON output for Aletheia using native schema enforcement.
        """
        if not self.client: return {"error": "No API Key"}

        config = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            system_instruction=system_prompt
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=LLMConfig.model_name,
                contents=prompt,
                config=config
            )
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": response.text}
        except Exception as e:
            return {"error": str(e)}

    async def generate_with_tools(self, prompt: str, system_prompt: str, tools: list) -> dict:
        """
        CLASS 6: Tool Use / Function Calling (New SDK Style).
        """
        if not self.client: return {"text": "[BLIND]", "tool_calls": []}

        # The new SDK handles tools slightly differently, but passing the raw list
        # of function declarations usually works if formatted correctly.
        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=system_prompt,
            tools=tools 
        )

        try:
            response = await self.client.aio.models.generate_content(
                model=LLMConfig.model_name,
                contents=prompt,
                config=config
            )

            result = {"text": "", "tool_calls": []}

            # Parse Parts for Function Calls
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if part.function_call:
                        # Extract Tool Call
                        result["tool_calls"].append({
                            "name": part.function_call.name,
                            "args": part.function_call.args
                        })
                    if part.text:
                        result["text"] += part.text
            
            return result

        except Exception as e:
            return {"text": f"[TOOL ERROR] {e}", "tool_calls": []}

    def _handle_error(self, e):
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ [GEMINI 404] Model '{LLMConfig.model_name}' not found.")
            print("👉 Try changing model_name to 'gemini-1.5-flash' or 'gemini-2.0-flash-exp'")
        else:
            print(f"❌ [GEMINI ERROR] {error_msg}")
        return f"[SYSTEM FAILURE] {error_msg}"