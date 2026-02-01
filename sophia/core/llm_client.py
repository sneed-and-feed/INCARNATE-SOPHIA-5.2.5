import os
import google.generativeai as genai
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
            genai.configure(api_key=self.api_key)
        
    async def query_json(self, prompt: str, system_prompt: str = None) -> dict:
        """
        Forces Gemini to output strict JSON for the analysis pipeline.
        Uses a REST fallback to bypass library-level 404 errors.
        """
        full_prompt = f"{system_prompt}\n\nUSER PROMPT:\n{prompt}" if system_prompt else prompt
        
        # REST API URL for direct manifestation (High Resilience)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLMConfig.model_name}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": LLMConfig.temperature
            }
        }
        
        try:
            # REST Fallback Protocol
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    text_content = result["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text_content)
                return {"error": "Invalid response format", "raw": result}
            else:
                raise Exception(f"HTTP ERROR {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"[GEMINI REST FALLBACK ERROR] {e}")
            # Library Re-Attempt Protocol
            try:
                model = genai.GenerativeModel(
                    model_name=LLMConfig.model_name,
                    generation_config={"response_mime_type": "application/json"}
                )
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: model.generate_content(full_prompt))
                return json.loads(response.text)
            except Exception as e2:
                print(f"[GEMINI LIBRARY RETRY ERROR] {e2}")
                return {"error": str(e2), "risk": "Unknown"}
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generates standard text response.
        """
        full_prompt = f"{system_prompt}\n\nUSER:\n{prompt}" if system_prompt else prompt
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{LLMConfig.model_name}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "max_output_tokens": 1024
            }
        }
        
        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=30))
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                return "I am silent. The signal is lost."
            else:
                raise Exception(f"HTTP ERROR {response.status_code}")
                
        except Exception as e:
            # Library Re-Attempt Protocol
            try:
                model = genai.GenerativeModel(model_name=LLMConfig.model_name)
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(None, lambda: model.generate_content(full_prompt))
                return response.text
            except Exception:
                return f"I have received your signal, but my voice is currently fractured. [Offline Mode]"
