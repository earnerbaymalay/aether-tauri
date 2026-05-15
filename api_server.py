import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

app = FastAPI(title="Aether Core API", version="1.0.0")

# Paths
AETHER_HOME = Path.home() / ".aether"
HW_PROFILE = AETHER_HOME / "hw_profile.json"

class QueryRequest(BaseModel):
    prompt: str
    sessionId: Optional[str] = "default"
    stream: bool = False

class SystemStats(BaseModel):
    profile: str
    ram_gb: int
    cores: int
    status: str

@app.get("/")
async def root():
    return {"status": "online", "system": "Aether Core", "role": "Engine Room"}

@app.get("/system/stats", response_model=SystemStats)
async def get_stats():
    if not HW_PROFILE.exists():
        return SystemStats(profile="Unknown", ram_gb=0, cores=0, status="Audit Required")
    
    with open(HW_PROFILE, "r") as f:
        data = json.load(f)
    
    return SystemStats(
        profile=data.get("profile", "Lite"),
        ram_gb=data.get("ram", 0),
        cores=data.get("cores", 0),
        status="Healthy"
    )

@app.post("/agent/query")
async def agent_query(request: QueryRequest):
    # This would normally interface with aether_agent.py
    # Simulating a response for the prototype
    await asyncio.sleep(1) # Simulate thinking
    return {
        "sessionId": request.sessionId,
        "response": f"Acknowledged. Processing your request in {request.sessionId} synapse...",
        "tokens": 42
    }

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
