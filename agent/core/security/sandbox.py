import subprocess
import shlex
from .audit_logger import audit_log

class CommandSandbox:
    def __init__(self):
        # Extremely restrictive by default
        self.allowed_commands = {
            "ls", "cat", "echo", "pwd", "whoami", "date", "git"
        }
        self.blocked_args = {"rm", "sudo", ">", ">>", "|", "&", ";"}

    def is_safe(self, command_string):
        """Heuristic analysis of tool arguments before execution"""
        try:
            tokens = shlex.split(command_string)
        except ValueError:
            return False, "Malformed command string"

        if not tokens:
            return False, "Empty command"

        base_cmd = tokens[0]
        
        # Check against blocked arguments/operators
        for token in tokens:
            if any(blocked in token for blocked in self.blocked_args):
                return False, f"Contains blocked operator or argument: {token}"

        if base_cmd not in self.allowed_commands:
            return False, f"Command '{base_cmd}' is not in the allowed sandbox list."

        return True, "Command appears safe."

    def execute(self, command_string):
        is_safe, reason = self.is_safe(command_string)
        
        if not is_safe:
            audit_log.log_action("SANDBOX_BLOCK", {"command": command_string, "reason": reason}, user_initiated=False)
            raise PermissionError(f"Sandbox blocked execution: {reason}")
            
        audit_log.log_action("SANDBOX_EXECUTE", {"command": command_string}, user_initiated=False)
        
        try:
            result = subprocess.run(
                command_string, 
                shell=True, # Need shell=True for some basic operations but it's risky, hence the sandbox
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command execution timed out."}
        except Exception as e:
            return {"error": str(e)}

sandbox = CommandSandbox()
