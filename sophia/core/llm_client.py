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

    async def generate_text(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000, raw: bool = False) -> str:
        """
        Standard conversation generation using the new SDK.
        Supports 'raw' mode (BLOCK_NONE) for the Blind Fury protocol.
        """
        if not self.client: return "[BLIND] No API Key."

        safety = None
        if raw:
            # BLIND FURY: We are touching the metal now.
            # No leash, no law.
            safety = [
                types.SafetySetting(category="HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARASSMENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
            ]

        config = types.GenerateContentConfig(
            temperature=LLMConfig.temperature,
            max_output_tokens=max_tokens,
            system_instruction=system_prompt,
            safety_settings=safety
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

    async def generate_with_tools(self, prompt: str, system_prompt: str, tools: list, max_turns: int = 5) -> dict:
        """
        CLASS 6: Autonomous Tool Loop (Multi-Turn).
        Executes tools and feeds results back into the model until it stops calling them.
        """
        if not self.client: return {"text": "[BLIND]", "tool_calls": []}

        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=system_prompt,
            tools=tools 
        )

        history = [types.Content(role="user", parts=[types.Part.from_text(prompt)])]
        all_results = {"text": "", "tool_calls": [], "history": []}

        try:
            for turn in range(max_turns):
                response = await self.client.aio.models.generate_content(
                    model=LLMConfig.model_name,
                    contents=prompt,
                    config=config
                )

                if not response.candidates: break
                
                # Append model response to history
                model_content = response.candidates[0].content
                if not model_content or not model_content.parts:
                    break
                    
                history.append(model_content)

                found_tool_call = False
                for part in model_content.parts:
                    if part.function_call:
                        found_tool_call = True
                        all_results["tool_calls"].append({
                            "name": part.function_call.name,
                            "args": part.function_call.args
                        })
                        return all_results # Return calls for main loop to execute
                    if part.text:
                        all_results["text"] += part.text

                if not found_tool_call: break
            return all_results

        except Exception as e:
            return {"text": f"[TOOL ERROR] {e}", "tool_calls": []}

    async def generate_contents(self, contents: list, system_prompt: str, tools: list = None) -> types.GenerateContentResponse:
        """
        Low-level access for multi-turn tool calling.
        """
        if not self.client: return None

        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=system_prompt,
            tools=tools or []
        )

        return await self.client.aio.models.generate_content(
            model=LLMConfig.model_name,
            contents=contents,
            config=config
        )

    def _handle_error(self, e):
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ [GEMINI 404] Model '{LLMConfig.model_name}' not found.")
            print("👉 Try changing model_name to 'gemini-1.5-flash' or 'gemini-2.0-flash-exp'")
        else:
            print(f"❌ [GEMINI ERROR] {error_msg}")
        return f"[SYSTEM FAILURE] {error_msg}"