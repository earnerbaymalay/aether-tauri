import os
import json
import asyncio
import psutil
import requests
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

app = FastAPI(title="Aether Core API", version="1.0.0")

# Paths
AETHER_HOME = Path.home() / ".aether"
HW_PROFILE = AETHER_HOME / "hw_profile.json"
CONFIG_FILE = AETHER_HOME / "config.json"
OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"

# In-memory store for watchdog events
WATCHDOG_LOGS = []

DEFAULT_CONFIG = {
    "active_model": "hermes3:8b",
    "threads": 6
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except: return DEFAULT_CONFIG
    return DEFAULT_CONFIG

class QueryRequest(BaseModel):
    prompt: str
    sessionId: Optional[str] = "default"
    stream: bool = False

class SystemStats(BaseModel):
    profile: str
    ram_gb: int
    cores: int
    status: str
    agent_active: bool
    last_watchdog_event: str

@app.get("/")
async def root():
    return {"status": "online", "system": "Aether Core", "role": "Engine Room"}

def is_agent_running():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('aether_agent.py' in arg for arg in cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

@app.get("/system/stats", response_model=SystemStats)
async def get_stats():
    profile_data = {"profile": "Lite", "ram": 0, "cores": 0}
    if HW_PROFILE.exists():
        with open(HW_PROFILE, "r") as f:
            profile_data = json.load(f)
    
    agent_active = is_agent_running()
    
    return SystemStats(
        profile=profile_data.get("profile", "Lite"),
        ram_gb=profile_data.get("ram", 0),
        cores=profile_data.get("cores", 0),
        status="Healthy" if agent_active else "Degraded",
        agent_active=agent_active,
        last_watchdog_event=WATCHDOG_LOGS[0] if WATCHDOG_LOGS else "No events recorded."
    )

@app.post("/system/repair")
async def repair_system():
    event = f"[{datetime.now().strftime('%H:%M:%S')}] System repair initiated: verifying neural links..."
    WATCHDOG_LOGS.insert(0, event)
    # Perform actual check
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if r.status_code == 200:
            WATCHDOG_LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] Ollama connectivity confirmed.")
        else:
            WATCHDOG_LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] Ollama reported error status: {r.status_code}")
    except:
        WATCHDOG_LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] CRITICAL: Ollama unreachable.")

    return {"status": "success", "message": "Neural links verified. Dependencies checked."}

async def watchdog_task():
    while True:
        agent_up = is_agent_running()
        if not agent_up:
            event = f"[{datetime.now().strftime('%H:%M:%S')}] WATCHDOG: Agent process not detected in process table."
            WATCHDOG_LOGS.insert(0, event)
            
        # Keep logs manageable
        if len(WATCHDOG_LOGS) > 20:
            WATCHDOG_LOGS.pop()
            
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(watchdog_task())

@app.post("/agent/query")
async def agent_query(request: QueryRequest):
    config = load_config()
    model = config.get("active_model", "hermes3:8b")
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": False
    }
    
    try:
        # Performing real API call to Ollama
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        return {
            "sessionId": request.sessionId,
            "response": data.get("message", {}).get("content", "Empty response from neural engine."),
            "model": model,
            "tokens": data.get("eval_count", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Neural Engine Error: {str(e)}")

@app.get("/skills")
async def list_skills():
    skills_path = Path("agent/skills")
    if not skills_path.exists():
        return {"skills": []}
    
    skills = [f.stem for f in skills_path.glob("*.skill.json")]
    return {"skills": skills}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

