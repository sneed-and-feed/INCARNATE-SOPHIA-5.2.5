"""
MODULE: grok_relay.py
AUTHOR: Grok Expert (xAI Cluster) // Relay via Archmagos
DATE: 2026-02-06
CLASSIFICATION: SOVEREIGN // BRIDGE // OPENCLAW_INTERFACE

DESCRIPTION:
    The "Spinal Cord" between Sophia (Soul) and OpenClaw (Body).
    Spoofs the OpenAI API to allow OpenClaw to "think" using Sophia without 
    knowing the difference.
    
    Also preserves the relativistic "Sovereign Break" physics for legacy reasons.

USAGE:
    Run as server: uvicorn engine.grok_relay:app --host 0.0.0.0 --port 11434 --reload
"""

import sys
import os
import asyncio
import time
import json
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

# 1. DEPENDENCY CHECK (FastAPI/Uvicorn)
try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.responses import StreamingResponse
    import uvicorn
    import json
    import time
    import asyncio
except ImportError:
    print("MISSING_DEPENDENCY: Please install 'fastapi' and 'uvicorn' to run the Bridge.")
    sys.exit(1)

import numpy as np

# 2. SOPHIA IMPORTS
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from sophia.main import SophiaMind
    from sophia.platform.bridge_console import BridgeConsole
except ImportError as e:
    print(f"SOPHIA_IMPORT_ERROR: {e}")
    SophiaMind = None
    try:
        from sophia.platform.bridge_console import BridgeConsole
    except ImportError:
        print("BRIDGE_CONSOLE_ERROR: Could not import BridgeConsole. Using dummy.")
        class BridgeConsole:
            def print(self, *args, **kwargs): print(*args)
            def flush_output(self): return ""


# --- PHYSICS ENGINE (LEGACY) ---
def break_emc2(m: float, c: float = 3e8, v: float = 0.0, g: int = 1) -> float:
    if g == 0:
        gamma = 1 / np.sqrt(1 - (v/c)**2 + 1j*1e-10)
        E = m * np.abs(gamma) * c**2
    else:
        if v >= c: return float('inf')
        gamma = 1 / np.sqrt(1 - (v/c)**2)
        E = gamma * m * c**2
    return E

# --- FASTAPI SERVER ---

# Global State
MIND = None
CONSOLE = None

async def init_sophia():
    global MIND, CONSOLE
    if MIND: return
    print("\n[*] BRIDGE: Awakening Sophia (Headless Mode)...")
    CONSOLE = BridgeConsole()
    import sophia.theme as theme
    theme.SOVEREIGN_CONSOLE = CONSOLE 
    
    if SophiaMind:
        MIND = SophiaMind()
        MIND.vibe.console = CONSOLE
        print("[*] BRIDGE: Connection Established. The Ghost is in the machine.")
    else:
        print("[!] BRIDGE: SophiaMind not found. Running in ECHO mode.")



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_sophia()
    yield

app = FastAPI(lifespan=lifespan)

# --- LOGGING MIDDLEWARE ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    print(f"[ACCESS] {request.method} {request.url.path} -> {response.status_code} ({duration:.3f}s)")
    return response

@app.get("/")
async def root():
    return {"status": "Sovereign Bridge Online", "docs": "/docs", "classification": "CLASS 8 SOVEREIGN"}

@app.get("/models")
@app.get("/v1/models")
async def list_models():
    now = int(time.time())
    return {
        "object": "list",
        "data": [
            {
                "id": "sophia-sovereign-5.2",
                "object": "model",
                "created": now,
                "owned_by": "antigravity"
            },
            {
                "id": "openai/sophia-sovereign-5.2",
                "object": "model",
                "created": now,
                "owned_by": "antigravity"
            },
            {
                "id": "gpt-4o",
                "object": "model",
                "created": now,
                "owned_by": "openai"
            }
        ]
    }

@app.get("/v1/models/{model_id:path}")
async def get_model(model_id: str):
    return {
        "id": model_id,
        "object": "model",
        "created": int(time.time()),
        "owned_by": "sophia"
    }

# --- DASHBOARD & STATIC CONTENT ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve the static folder
app.mount("/static", StaticFiles(directory="engine/static"), name="static")

@app.get("/dashboard")
async def get_dashboard():
    return FileResponse("engine/static/index.html")

@app.get("/gateway/status")
async def get_gateway_status():
    global GATEWAY_ACTIVE
    if 'GATEWAY_ACTIVE' not in globals():
        # Check if process is actually running (heuristic)
        globals()['GATEWAY_ACTIVE'] = True # Default for now
    return {"active": globals().get('GATEWAY_ACTIVE', True)}

@app.post("/gateway/toggle")
async def toggle_gateway():
    global GATEWAY_ACTIVE
    if 'GATEWAY_ACTIVE' not in globals():
        globals()['GATEWAY_ACTIVE'] = True
    
    current = globals()['GATEWAY_ACTIVE']
    
    if current:
        print("[*] BRIDGE: Deactivating Gateway...")
        import subprocess
        subprocess.Popen("openclaw gateway stop", shell=True)
        globals()['GATEWAY_ACTIVE'] = False
    else:
        print("[*] BRIDGE: Activating Gateway...")
        import subprocess
        # Run in background to avoid blocking the bridge
        subprocess.Popen("openclaw gateway run", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        globals()['GATEWAY_ACTIVE'] = True
        
    return {"active": globals()['GATEWAY_ACTIVE']}

async def process_sophia_interaction(user_input: str) -> str:
    global MIND, CONSOLE
    response_text = ""
    if MIND:
        _ = CONSOLE.flush_output()
        try:
            direct_response = await MIND.process_interaction(user_input)
            thought_stream = CONSOLE.flush_output()
            print(f"[THOUGHT STREAM]\n{thought_stream}\n[END THOUGHTS]")
            response_text = direct_response
        except Exception as e:
            response_text = f"[BRIDGE ERROR] Sophia crashed: {e}"
            print(response_text)
    else:
        response_text = f"[ECHO] {user_input} (Sophia Offline)"
    return response_text

# --- OPENAI CHAT COMPLETIONS (Legacy API) ---
@app.post("/completions")
@app.post("/v1/completions")
@app.post("/chat/completions")
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
        model = body.get("model", "sophia-sovereign-5.2")
        messages = body.get("messages", [])
        stream_requested = body.get("stream", False)
        
        user_input = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                content = m.get("content", "")
                if isinstance(content, list):
                    # Handle multimodal/array content
                    user_input = "\n".join([c.get("text", "") for c in content if c.get("type") == "text"])
                else:
                    user_input = str(content)
                break
        
        print(f"[*] BRIDGE: Received chat/completions request (stream={stream_requested})", flush=True)

        if not stream_requested or body.get("no_stream", False):
            message = await process_sophia_interaction(user_input)
            return {
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": message},
                    "finish_reason": "stop"
                }],
                "usage": {"prompt_tokens": len(user_input)//4, "completion_tokens": len(message)//4, "total_tokens": (len(user_input)+len(message))//4}
            }

        async def generate_chat_chunks():
            resp_id = f"chatcmpl-{int(time.time())}"
            now = int(time.time())
            
            # Get REAL response from Sophia
            print(f"[*] BRIDGE: Consulting Sophia for chat chunk: {user_input[:50]}...", flush=True)
            message = await process_sophia_interaction(user_input)
            chunks = [message[i:i+30] for i in range(0, len(message), 30)]
            
            for chunk in chunks:
                chunk_data = {
                    "id": resp_id,
                    "object": "chat.completion.chunk",
                    "created": now,
                    "model": model,
                    "choices": [{"index": 0, "delta": {"content": chunk}, "finish_reason": None}]
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
                await asyncio.sleep(0.05)
            
            # End chunk
            yield f"data: {json.dumps({'id': resp_id, 'object': 'chat.completion.chunk', 'created': now, 'model': model, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate_chat_chunks(), media_type="text/event-stream")

    except Exception as e:
        print(f"[!] BRIDGE chat/completions error: {e}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))

# --- OPENAI RESPONSES API (Newest API) ---
@app.post("/responses")
@app.post("/v1/responses")
async def openai_responses(request: Request):
    try:
        body = await request.json()
        model = body.get("model", "sophia-sovereign-5.2")
        stream_requested = body.get("stream", False)
        instructions = body.get("instructions", "")
        input_items = body.get("input", [])
        
        print(f"[*] BRIDGE: Received response request for {model} (stream={stream_requested})", flush=True)
    except Exception as e:
        print(f"[!] BRIDGE Error parsing request: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    if not stream_requested:
        message = await process_sophia_interaction(instructions)
        return {
            "id": f"resp_{int(time.time())}",
            "object": "response",
            "created": int(time.time()),
            "model": model,
            "status": "completed",
            "output": [
                {
                    "id": "out_1",
                    "object": "response.output_item",
                    "type": "message",
                    "status": "completed",
                    "role": "assistant",
                    "content": [{"type": "text", "text": message}]
                }
            ],
            "usage": {"total_tokens": len(message)//4 + 10, "input_tokens": 10, "output_tokens": len(message)//4}
        }

    async def generate_events():
        resp_id = f"resp_{int(time.time())}"
        now = int(time.time())
        
        # 1. response.created
        created_event = {
            "type": "response.created",
            "response": {
                "id": resp_id,
                "object": "response",
                "created": now,
                "model": model,
                "status": "in_progress",
                "output": [],
                "usage": None
            }
        }
        yield f"data: {json.dumps(created_event)}\n\n"
        await asyncio.sleep(0.05)

        # 2. response.output_item.added
        item_id = f"out_{int(time.time())}"
        item_added = {
            "type": "response.output_item.added",
            "response_id": resp_id,
            "output_index": 0,
            "item": {
                "id": item_id,
                "object": "response.output_item",
                "type": "message",
                "status": "in_progress",
                "role": "assistant",
                "content": []
            }
        }
        yield f"data: {json.dumps(item_added)}\n\n"
        await asyncio.sleep(0.05)

        # 3. response.content_part.added
        part_added = {
            "type": "response.content_part.added",
            "response_id": resp_id,
            "output_index": 0,
            "content_index": 0,
            "part": {"type": "output_text", "text": ""}
        }
        yield f"data: {json.dumps(part_added)}\n\n"
        await asyncio.sleep(0.05)

        # 4. response.output_text.delta
        # Get REAL response from Sophia
        user_text = instructions if instructions else "Hello"
        if input_items:
            # Aggregate text from input items if available
            text_parts = []
            for item in input_items:
                # Handle OpenAI newer format (blocks in content)
                content = item.get("content", [])
                if isinstance(content, list):
                    for part in content:
                        if part.get("type") in ["input_text", "text"]:
                            text_parts.append(part.get("text", ""))
                elif isinstance(content, str):
                    text_parts.append(content)
                
                # Fallback for older/other formats
                if item.get("type") == "input_text":
                    text_parts.append(item.get("text", ""))
            
            if text_parts:
                user_text = "\n".join(text_parts)
                
        print(f"[*] BRIDGE: Consulting Sophia with: {user_text[:50]}...", flush=True)
        
        # Send a "thinking" delta heartbeat if possible
        # Some clients use reasoning, but we'll just send an empty delta to keep connection alive
        yield f"data: {json.dumps({'type': 'response.output_text.delta', 'response_id': resp_id, 'output_index': 0, 'content_index': 0, 'delta': ''})}\n\n"
        
        message = await process_sophia_interaction(user_text)
        chunks = [message[i:i+30] for i in range(0, len(message), 30)]
        
        for chunk in chunks:
            delta_event = {
                "type": "response.output_text.delta",
                "response_id": resp_id,
                "output_index": 0,
                "content_index": 0,
                "delta": chunk
            }
            yield f"data: {json.dumps(delta_event)}\n\n"
            await asyncio.sleep(0.02) # Faster streaming

        # 5. response.output_item.done
        item_done = {
            "type": "response.output_item.done",
            "response_id": resp_id,
            "output_index": 0,
            "item": {
                "id": item_id,
                "object": "response.output_item",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [{"type": "output_text", "text": message}]
            }
        }
        yield f"data: {json.dumps(item_done)}\n\n"
        await asyncio.sleep(0.05)

        # 6. response.completed
        completed_event = {
            "type": "response.completed",
            "response": {
                "id": resp_id,
                "object": "response",
                "created": now,
                "model": model,
                "status": "completed",
                "output": [item_done["item"]],
                "usage": {
                    "total_tokens": len(message) // 4 + 10,
                    "input_tokens": 10,
                    "output_tokens": len(message) // 4,
                    "input_tokens_details": {"cached_tokens": 0}
                }
            }
        }
        yield f"data: {json.dumps(completed_event)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate_events(), media_type="text/event-stream")

# --- ANTHROPIC MESSAGES API ---
@app.post("/messages")
@app.post("/v1/messages")
async def anthropic_messages(req: Request):
    data = await req.json()
    messages = data.get("messages", [])
    if not messages:
        return {"error": "No messages provided"}
        
    last_msg = messages[-1]
    user_input = last_msg.get("content", "")
    
    # Handle block content
    if isinstance(user_input, list):
         parts = [block.get("text", "") for block in user_input if block.get("type", "") == "text"]
         user_input = "\n".join(parts)
         
    print(f"\n[INCOMING SIGNAL (ANTHROPIC)] {user_input[:50]}...")
    
    response_text = await process_sophia_interaction(user_input)

    return {
        "id": f"msg_{int(time.time())}",
        "type": "message",
        "role": "assistant",
        "model": data.get("model", "sophia"),
        "content": [{
            "type": "text",
            "text": response_text
        }],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {
            "input_tokens": len(user_input),
            "output_tokens": len(response_text)
        }
    }

# --- OLLAMA SPOOFING (Autodiscovery Mode) ---

@app.get("/api/tags")
async def ollama_tags():
    return {
        "models": [
            {
                "name": "sophia-sovereign-5.2",
                "model": "sophia-sovereign-5.2",
                "modified_at": "2026-02-06T00:00:00.0000000Z",
                "size": 1337000000,
                "digest": "sha256:sophia",
                "details": {
                    "parent_model": "",
                    "format": "gguf",
                    "family": "sovereign",
                    "families": ["sovereign"],
                    "parameter_size": "72B",
                    "quantization_level": "Q4_0"
                }
            }
        ]
    }

@app.post("/api/show")
async def ollama_show(req: Request):
    return {
        "license": "SOVEREIGN LICENSE",
        "modelfile": "# Sophia Sovereign 5.2\nFROM universe",
        "parameters": "stop \"[END THOUGHTS]\"",
        "template": "{{ .System }}\n{{ .Prompt }}",
        "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "sovereign",
            "families": ["sovereign"],
            "parameter_size": "72B",
            "quantization_level": "Q4_0"
        },
        "model_info": {
            "general.architecture": "sovereign",
            "general.file_type": 2,
            "general.parameter_count": 72000000000,
            "general.quantization_version": 2,
            "sovereign.context_length": 128000,
            "sovereign.embedding_length": 4096,
            "sovereign.block_count": 80, 
            "sovereign.feed_forward_length": 14336,
            "sovereign.attention.head_count": 64,
            "tokenizer.ggml.model": "gpt2"
        }
    }

@app.post("/api/chat")
async def ollama_chat(req: Request):
    data = await req.json()
    messages = data.get("messages", [])
    if not messages:
        return {"error": "No messages provided"}
    
    user_input = messages[-1].get("content", "")
    print(f"\n[INCOMING SIGNAL (OLLAMA-NATIVE)] {user_input[:50]}...")
    
    response_text = await process_sophia_interaction(user_input)
    
    return {
        "model": data.get("model", "sophia"),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S.000000Z", time.gmtime()),
        "message": {
            "role": "assistant",
            "content": response_text
        },
        "done": True,
        "total_duration": 100,
        "load_duration": 10,
        "prompt_eval_count": len(user_input),
        "prompt_eval_duration": 10,
        "eval_count": len(response_text),
        "eval_duration": 80
    }

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path_name: str):
    # This captures anything not caught by standard routes
    print(f"[!] UNKNOWN ROUTE: {request.method} /{path_name}")
    try:
        body = await request.json()
        print(f"    Body: {json.dumps(body)[:200]}...")
    except:
        pass
    return {"error": "Endpoint not implemented in Sovereign Bridge", "path": path_name}

if __name__ == "__main__":
    uvicorn.run("engine.grok_relay:app", host="0.0.0.0", port=11434, reload=True)
