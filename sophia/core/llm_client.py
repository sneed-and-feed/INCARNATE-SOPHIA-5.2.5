import os
import json
import logging
import asyncio
from dataclasses import dataclass
from google import genai
from google.genai import types

# Suppress noisy logs
logging.getLogger("google.genai").setLevel(logging.WARNING)

@dataclass
class LLMConfig:
    model_name: str = "gemini-2.0-flash" 
    temperature: float = 0.7
    # Local/Alternative Endpoint Settings
    provider: str = "google" # "google", "openai", "rest"
    base_url: str = None
    custom_headers: dict = None

class GeminiClient:
    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        
        # 1. Load Keys (Priority: Sophia -> Google -> Dotenv)
        self.api_key = (os.getenv("SOPHIA_API_KEY") or 
                        os.getenv("GOOGLE_AI_KEY") or 
                        os.getenv("GOOGLE_API_KEY") or
                        os.getenv("OPENAI_API_KEY"))
        
        if not self.api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                self.api_key = os.getenv("SOPHIA_API_KEY") or os.getenv("GOOGLE_AI_KEY")
            except ImportError:
                pass
            
        # Initialize appropriate backend
        self.client = None
        if self.config.provider == "google" and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        elif self.config.provider == "openai":
            # We use a simple HTTP client for OpenAI-compatible to avoid extra dependencies purely for localized scanning
            pass

    async def generate_text(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000, raw: bool = False) -> str:
        """Universal text generation."""
        if self.config.provider == "google":
            return await self._generate_google(prompt, system_prompt, max_tokens, raw)
        elif self.config.provider == "openai" or self.config.provider == "rest":
            return await self._generate_rest(prompt, system_prompt, max_tokens)
        return "[ERROR] Unknown Provider"

    async def query_json(self, prompt: str, system_prompt: str = None) -> dict:
        """Universal JSON extraction."""
        if self.config.provider == "google":
            return await self._query_json_google(prompt, system_prompt)
        else:
            # Fallback to generic text + parsing for non-native JSON modes
            text = await self._generate_rest(prompt, system_prompt, max_tokens=2000)
            try:
                # Basic JSON extraction logic
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    return json.loads(text[start:end])
                return {"error": "No JSON object found", "raw": text}
            except Exception as e:
                return {"error": str(e), "raw": text}

    async def _generate_google(self, prompt: str, system_prompt: str, max_tokens: int, raw: bool) -> str:
        if not self.client: return "[BLIND] No API Key."
        safety = None
        if raw:
            safety = [
                types.SafetySetting(category="HATE_SPEECH", threshold="BLOCK_NONE"),
                types.SafetySetting(category="HARASSMENT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                types.SafetySetting(category="DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
            ]
        config = types.GenerateContentConfig(
            temperature=self.config.temperature,
            max_output_tokens=max_tokens,
            system_instruction=system_prompt,
            safety_settings=safety
        )
        try:
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "Resource has been exhausted" in err_msg:
                return "[GOOGLE ERROR] 429: Quota Exhausted or Rate Limited. Please check your API credits/billing."
            return f"[GOOGLE ERROR] {err_msg}"

    async def _query_json_google(self, prompt: str, system_prompt: str) -> dict:
        if not self.client: return {"error": "No API Key"}
        config = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            system_instruction=system_prompt
        )
        try:
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=config
            )
            return json.loads(response.text)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "Resource has been exhausted" in err_msg:
                return {"error": "429: Quota Exhausted or Rate Limited. Please check your API credits/billing."}
            return {"error": err_msg}

    async def _generate_rest(self, prompt: str, system_prompt: str, max_tokens: int) -> str:
        """Generic REST handler for Ollama, Anthropic, or Custom APIs."""
        url = self.config.base_url or "http://localhost:11434/api/generate" # Default to Ollama
        
        # Simple payload construction (Ollama style by default)
        payload = {
            "model": self.config.model_name,
            "prompt": f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": max_tokens
            }
        }
        
        # Override for OpenAI-compatible
        if self.config.provider == "openai":
            url = self.config.base_url or "http://localhost:11434/v1/chat/completions"
            payload = {
                "model": self.config.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt or "You are Sophia."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.temperature,
                "max_tokens": max_tokens
            }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if self.config.custom_headers:
            headers.update(self.config.custom_headers)

        try:
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                # Parse based on expected format
                if "choices" in data: # OpenAI style
                    return data["choices"][0]["message"]["content"]
                elif "response" in data: # Ollama style
                    return data["response"]
                return json.dumps(data)
        except Exception as e:
            return f"[REST ERROR] {e}"
    async def generate_with_tools(self, prompt: str, system_prompt: str, tools: list, max_turns: int = 5) -> dict:
        """
        CLASS 6: Autonomous Tool Loop (Multi-Turn).
        Note: Currently primary support is via Google SDK.
        """
        if self.config.provider != "google" or not self.client:
            return {"text": "[ERROR] Tool calling only supported on Google backend currently.", "tool_calls": []}

        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=system_prompt,
            tools=tools 
        )

        all_results = {"text": "", "tool_calls": [], "history": []}
        try:
            # Note: Native multi-turn requires keeping history, currently we do single-turn dispatch
            response = await self.client.aio.models.generate_content(
                model=self.config.model_name,
                contents=prompt,
                config=config
            )

            if not response.candidates: return all_results
            
            model_content = response.candidates[0].content
            if not model_content or not model_content.parts:
                return all_results
                
            for part in model_content.parts:
                if part.function_call:
                    all_results["tool_calls"].append({
                        "name": part.function_call.name,
                        "args": part.function_call.args
                    })
                if part.text:
                    all_results["text"] += part.text

            return all_results
        except Exception as e:
            return {"text": f"[TOOL ERROR] {e}", "tool_calls": []}

    async def generate_contents(self, contents: list, system_prompt: str, tools: list = None) -> types.GenerateContentResponse:
        """Low-level access for multi-turn tool calling (Google Only)."""
        if self.config.provider != "google" or not self.client: return None

        config = types.GenerateContentConfig(
            temperature=0.1,
            system_instruction=system_prompt,
            tools=tools or []
        )

        return await self.client.aio.models.generate_content(
            model=self.config.model_name,
            contents=contents,
            config=config
        )

    def _handle_error(self, e):
        error_msg = str(e)
        print(f"❌ [LLM ERROR] {error_msg}")
        return f"[SYSTEM FAILURE] {error_msg}"
