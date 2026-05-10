import os
import sys
import json
import requests
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

def port_skill_from_url(url, output_dir):
    print(f"🌍 Accessing documentation at: {url}")
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Simple extraction logic - in real Aether, this would be sent to the Logic model
        title = soup.title.string if soup.title else "New Skill"
        text_content = soup.get_text()
        
        print(f"🧠 Synthesizing skill structure for: {title}")
        
        # Mocking the AI synthesis for the porter
        skill_name = title.lower().replace(" ", "-").split("|")[0].strip()
        skill_content = f"""---
name: {skill_name}
description: Autonomously ported from {url}
triggers: {skill_name}, help with {skill_name}
version: 1.0
---

# {title}

This skill was autonomously acquired from external documentation.

## Core Capabilities
- Automated extraction from {url}
- Integrated knowledge from source materials

## Workflow
1. Analyze user request in context of {skill_name}
2. Execute tools related to the documentation
3. Verify against source facts

## Tools Used
- web_read.ps1
- read_file.ps1
"""
        skill_dir = Path(output_dir) / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        with open(skill_dir / "SKILL.md", "w") as f:
            f.write(skill_content)
            
        print(f"✅ Skill '{skill_name}' successfully ported to {skill_dir}")
        return True
    except Exception as e:
        print(f"❌ Failed to port skill: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Aether Autonomous Skill Porter")
    parser.add_argument("--url", required=True, help="URL of the documentation to port")
    parser.add_argument("--out", default="agent/skills", help="Output directory for the skill")
    args = parser.parse_args()
    
    port_skill_from_url(args.url, args.out)

if __name__ == "__main__":
    main()
