import os
import json
from pathlib import Path

class UniversalSkillEngine:
    """
    Aether Universal Skill Engine
    Ports instructions from external formats (CLAUDE.md, GEMINI.md, rules.json)
    to Aether's internal nervous system.
    """
    def __init__(self, agent_root):
        self.agent_root = Path(agent_root)
        self.skills_dir = self.agent_root / "skills"
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.active_skills = {}

    def discover_skills(self, cwd=None):
        """Scans for skill definition files in repo and current working directory."""
        self.active_skills = {}
        search_paths = [self.skills_dir]
        if cwd: search_paths.append(Path(cwd))

        for path in search_paths:
            if not path.exists(): continue
            # Support multiple standards
            for filename in ["CLAUDE.md", "GEMINI.md", "SKILL.md", "rules.json"]:
                p = path / filename
                if p.exists():
                    self.active_skills[filename] = self._parse_skill(p)
        return self.active_skills

    def _parse_skill(self, path):
        """Extracts core directives from a skill file."""
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            try:
                data = json.loads(content)
                return data.get("instructions", content)
            except:
                return content
        
        # Markdown parsing: Look for 'Instructions' or 'Guidelines' sections
        lines = content.split("\n")
        instructions = []
        capturing = False
        for line in lines:
            if any(h in line.upper() for h in ["# INSTRUCTIONS", "# GUIDELINES", "# RULES"]):
                capturing = True
                continue
            if capturing and line.startswith("#"):
                break
            if capturing:
                instructions.append(line)
        
        return "\n".join(instructions).strip() if instructions else content.strip()

    def get_skill_prompt(self):
        """Generates the combined prompt segment for all loaded skills."""
        if not self.active_skills:
            return ""
        
        prompt = "\n--- LOADED EXTERNAL SKILLS ---\n"
        for name, instructions in self.active_skills.items():
            prompt += f"\n[Skill: {name}]\n{instructions}\n"
        prompt += "------------------------------\n"
        return prompt
