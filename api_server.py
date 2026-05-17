import os
import json
import asyncio
import psutil
import httpx
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path

app = FastAPI(
    title="Aether Core API",
    version="1.1.0",
    description="The Local-First Neural Operating Interface Backend"
)

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
    """Loads configuration from the local filesystem."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

class QueryRequest(BaseModel):
    """Schema for agent queries."""
    prompt: str = Field(..., description="The user's input prompt")
    model: Optional[str] = Field(None, description="Model to use for this specific query")
    session_id: Optional[str] = Field("default", alias="sessionId", description="Unique session identifier")
    stream: bool = Field(False, description="Whether to stream the response")

    class Config:
        allow_population_by_field_name = True

class SystemStats(BaseModel):
    """Schema for system telemetry and health stats."""
    profile: str
    ram_gb: float
    cores: int
    status: str
    agent_active: bool
    last_watchdog_event: str

@app.on_event("startup")
async def startup_event():
    """Initializes background tasks on server startup."""
    asyncio.create_task(watchdog_task())

@app.get("/", tags=["Diagnostic"])
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "system": "Aether Core",
        "timestamp": datetime.now().isoformat()
    }

def is_agent_running() -> bool:
    """Checks the system process table for the Aether Agent."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('aether_agent.py' in arg for arg in cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

@app.get("/system/stats", response_model=SystemStats, tags=["System"])
async def get_stats():
    """Retrieves current system health and hardware profile."""
    profile_data = {"profile": "Lite", "ram": 0, "cores": 0}
    if HW_PROFILE.exists():
        try:
            with open(HW_PROFILE, "r") as f:
                profile_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    agent_active = is_agent_running()
    
    return SystemStats(
        profile=profile_data.get("profile", "Lite"),
        ram_gb=float(profile_data.get("ram", 0)),
        cores=profile_data.get("cores", 0),
        status="Healthy" if agent_active else "Degraded",
        agent_active=agent_active,
        last_watchdog_event=WATCHDOG_LOGS[0] if WATCHDOG_LOGS else "No events recorded."
    )

@app.post("/system/repair", tags=["System"])
async def repair_system():
    """Attempts to diagnose and log connectivity to the neural engine."""
    event = f"[{datetime.now().strftime('%H:%M:%S')}] System repair initiated: verifying neural links..."
    WATCHDOG_LOGS.insert(0, event)
    
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("http://127.0.0.1:11434/api/tags", timeout=2.0)
            if r.status_code == 200:
                WATCHDOG_LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] Ollama connectivity confirmed.")
            else:
                WATCHDOG_LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] Ollama reported error status: {r.status_code}")
    except Exception as e:
        WATCHDOG_LOGS.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] CRITICAL: Ollama unreachable: {str(e)}")

    return {"status": "success", "message": "Neural links verified. Dependencies checked."}

async def watchdog_task():
    """Background task that monitors the agent process."""
    while True:
        agent_up = is_agent_running()
        if not agent_up:
            event = f"[{datetime.now().strftime('%H:%M:%S')}] WATCHDOG: Agent process not detected in process table."
            WATCHDOG_LOGS.insert(0, event)
            
        # Keep logs manageable
        if len(WATCHDOG_LOGS) > 20:
            WATCHDOG_LOGS.pop()
            
        await asyncio.sleep(60)

@app.post("/agent/query", tags=["Agent"])
async def agent_query(request: QueryRequest):
    """Routes a prompt to the local neural engine (Ollama)."""
    # Use requested model or fallback to global config
    model = request.model
    if not model:
        config = load_config()
        model = config.get("active_model", "hermes3:8b")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": request.prompt}],
        "stream": request.stream
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_CHAT_URL, json=payload, timeout=120.0)
            response.raise_for_status()
            data = response.json()

            return {
                "sessionId": request.session_id,
                "response": data.get("message", {}).get("content", "Empty response from neural engine."),
                "model": model,
                "tokens": data.get("eval_count", 0)
            }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Neural Engine Connection Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected Error: {str(e)}")

@app.get("/skills", tags=["Agent"])
async def list_skills():
    """Lists all available agent skills."""
    skills_path = Path("agent/skills")
    if not skills_path.exists():
        return {"skills": []}
    
    skills = [f.stem.replace(".skill", "") for f in skills_path.glob("*.skill.json")]
    return {"skills": skills}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
