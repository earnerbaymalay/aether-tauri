import os
import json
import time
from pathlib import Path

class RalphLoop:
    """
    The Ralph Loop: Autonomous Recursive ReAct Engine.
    Plan -> Act -> Verify -> Repeat until Done.
    """
    def __init__(self, agent_instance):
        self.agent = agent_instance
        self.history = []
        self.max_iterations = 10

    def execute(self, high_level_task):
        print(f"🌀 [RALPH] Initializing Autonomous Loop for task: {high_level_task}")
        
        # Step 1: Initial Planning
        plan = self.agent.generate_response(f"Create a multi-step plan to: {high_level_task}. Output only the plan steps.")
        print(f"📋 [RALPH] Plan formulated.")
        
        for i in range(self.max_iterations):
            print(f"🔄 [RALPH] Iteration {i+1}/{self.max_iterations}")
            
            # Step 2: Determine next action
            context = "\n".join(self.history[-3:]) # Recent context
            action_request = f"Based on the plan and history, what is the single next terminal command to run? Current task: {high_level_task}\nHistory: {context}"
            command = self.agent.generate_response(action_request).strip()
            
            if "DONE" in command.upper() or "TASK COMPLETE" in command.upper():
                print("✨ [RALPH] Task confirmed as complete.")
                break
                
            # Step 3: Execute Action
            print(f"🛠️  [RALPH] Executing: {command}")
            result = self.agent.execute_command(command)
            self.history.append(f"Command: {command}\nResult: {result}")
            
            # Step 4: Verification
            verify_request = f"Did the last command succeed and move us closer to the goal? Task: {high_level_task}\nResult: {result}"
            verification = self.agent.generate_response(verify_request)
            
            if "CRITICAL ERROR" in verification.upper():
                print("❌ [RALPH] Critical failure detected. Aborting.")
                break
                
        print("🏁 [RALPH] Autonomous sequence ended.")

# Mock Agent for testing if imported directly
class MockAgent:
    def generate_response(self, prompt):
        if "next terminal command" in prompt:
            return "ls -la"
        return "Plan: 1. Check files. 2. Finish."
    def execute_command(self, cmd):
        return "file1.txt, file2.py"

if __name__ == "__main__":
    ralph = RalphLoop(MockAgent())
    ralph.execute("Analyze current directory structure")
