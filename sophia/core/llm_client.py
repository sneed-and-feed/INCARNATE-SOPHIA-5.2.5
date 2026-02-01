import os
from google import genai
from google.genai import types
import json
import asyncio
import requests
from dataclasses import dataclass

@dataclass
class LLMConfig:
    # High-availability model for Class 5 Forensic throughput
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.1

class GeminiClient:
    def __init__(self):
        # Load API Key (Priority: OPHANE Environment -> God Mode Env -> .env file)
        self.api_key = (os.getenv("SOPHIA_API_KEY") or 
                        os.getenv("GOOGLE_AI_KEY") or 
                        os.getenv("GOOGLE_API_KEY"))
        
        if not self.api_key:
            print("[WARNING] No API Key in Env. Attempting to load from .env file...")
            try:
                from dotenv import load_dotenv
                load_dotenv()
                self.api_key = (os.getenv("SOPHIA_API_KEY") or 
                                os.getenv("GOOGLE_AI_KEY") or 
                                os.getenv("GOOGLE_API_KEY"))
            except ImportError:
                print("[ERROR] python-dotenv not installed. Secrets must be in ENV.")
            
        if not self.api_key:
            print("[WARNING] No Google API Key found. The Cat is blinded.")
        else:
            self.client = genai.Client(api_key=self.api_key)
        
    async def query_json(self, prompt: str, system_prompt: str = None) -> dict:
        """
        Forces Gemini to output strict JSON for the analysis pipeline.
        Uses a REST fallback to bypass library-level errors.
        """
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=LLMConfig.temperature,
            system_instruction=system_prompt
        )
        
        try:
            # SDK Manifestation
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: self.client.models.generate_content(
                model=LLMConfig.model_name,
                contents=prompt,
                config=config
            ))
            return json.loads(response.text)
                
        except Exception as e:
            print(f"[SDK ERROR] {e}. Falling back to REST Manifest...")
            # REST Fallback Protocol (High Resilience)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLMConfig.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "response_mime_type": "application/json",
                    "temperature": LLMConfig.temperature
                }
            }
            if system_prompt:
                payload["system_instruction"] = {"parts": [{"text": system_prompt}]}
            
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
                if response.status_code == 200:
                    result = response.json()
                    if "candidates" in result and result["candidates"]:
                        text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                        return json.loads(text_content)
                return {"error": "REST Fallback Failed", "status": response.status_code}
            except Exception as e2:
                return {"error": str(e2), "risk": "Unknown"}

    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generates standard text response.
        """
        config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=2048,
            system_instruction=system_prompt
        )
        
        try:
            # SDK Manifestation
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: self.client.models.generate_content(
                model=LLMConfig.model_name,
                contents=prompt,
                config=config
            ))
            return response.text
                
        except Exception as e:
            print(f"[SDK ERROR] {e}. Falling back to REST Manifest...")
            # REST Fallback Protocol
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLMConfig.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "max_output_tokens": 2048
                }
            }
            if system_prompt:
                payload["system_instruction"] = {"parts": [{"text": system_prompt}]}
            
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
                if response.status_code == 200:
                    result = response.json()
                    if "candidates" in result and result["candidates"]:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            return "".join(part.get("text", "") for part in candidate["content"]["parts"])
                return f"I have received your signal, but my voice is currently fractured. [Rest Fallback Error]"
            except Exception:
                return f"I have received your signal, but my voice is currently fractured. [Offline Mode]"

    async def generate_text(self, prompt: str, system_prompt: str = None) -> str:
        """
        Standard conversation generation via REST fallback for maximum "mouth" reliability.
        """
        full_prompt = f"{system_prompt}\n\nUSER:\n{prompt}" if system_prompt else prompt
        
        # REST API URL (Same robustness as query_json)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLMConfig.model_name}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": 0.9, # Higher temp for creativity/personality
                "maxOutputTokens": 500
            }
        }
        
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
            
            print(f"[GEMINI ERROR] {response.text}")
            return "I am unable to formulate a thought. The Pleroma is silent."
                
        except Exception as e:
            return f"[SYSTEM ERROR] Vocal Cords Severed: {e}"

    async def generate_with_tools(self, prompt: str, system_prompt: str = None, tools: list = None) -> dict:
        """
        Generates response with tool calling support.
        Returns dict with 'text' and optional 'tool_calls' array.
        """
        config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=2048,
            system_instruction=system_prompt,
            tools=tools if tools else None
        )
        
        try:
            # SDK Manifestation with tools
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: self.client.models.generate_content(
                model=LLMConfig.model_name,
                contents=prompt,
                config=config
            ))
            
            # Parse response for tool calls
            result = {"text": "", "tool_calls": []}
            
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        # Check for text response
                        if hasattr(part, 'text') and part.text:
                            result["text"] += part.text
                        
                        # Check for function call
                        if hasattr(part, 'function_call') and part.function_call:
                            fc = part.function_call
                            tool_call = {
                                "name": fc.name,
                                "args": dict(fc.args) if hasattr(fc, 'args') else {}
                            }
                            result["tool_calls"].append(tool_call)
            
            # Fallback to simple text if available
            if not result["text"] and not result["tool_calls"]:
                result["text"] = response.text if hasattr(response, 'text') else ""
            
            return result
                
        except Exception as e:
            print(f"[SDK ERROR] Function calling failed: {e}. Tools not supported or API issue.")
            # Fallback without tools
            return {"text": await self.generate(prompt, system_prompt), "tool_calls": []}
