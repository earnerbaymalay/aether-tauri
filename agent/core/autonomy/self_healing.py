import time

class SelfHealer:
    def __init__(self):
        self.max_retries = 3

    def execute_with_healing(self, tool_func, *args, **kwargs):
        """
        Aether automatically retries failed tool calls with alternate strategies.
        """
        attempts = 0
        last_error = None
        
        while attempts < self.max_retries:
            try:
                # Attempt to execute the tool
                return True, tool_func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                last_error = str(e)
                print(f"[Self-Heal] Tool execution failed (Attempt {attempts}/{self.max_retries}): {last_error}")
                
                # Alternate strategy logic could go here based on the error type
                # For now, simple exponential backoff
                time.sleep(2 ** attempts)
                
        return False, f"Execution failed after {self.max_retries} attempts. Last error: {last_error}"

healer = SelfHealer()
