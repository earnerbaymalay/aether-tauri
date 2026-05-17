---
name: file-io
description: Read and write files to the local filesystem.
triggers: read file, write file, save file, open file, create file
version: 1.0
---

# File I/O Skill

This skill provides the agent with the ability to read from and write to the local filesystem.

## Core Functions

This skill exposes two primary tool functions. The agent should use the appropriate function based on the user's request.

### 1. `read_file(path: str)`
- **Purpose**: Reads the entire content of a file at the specified path.
- **Usage**: The agent should use this when it needs to understand the content of an existing file for context or analysis.
- **Output**: Returns the raw string content of the file. If the file is not found, it returns an error message.

**Example Agent Thought Process:**
> The user wants me to review `main.py`. I need to read the file first. I will call `read_file('path/to/main.py')`.

### 2. `write_file(path: str, content: str)`
- **Purpose**: Writes the provided content to a file at the specified path. If the file exists, it will be **overwritten**. If it does not exist, it will be created.
- **Usage**: The agent should use this when asked to create a new file, save code, or modify an existing file. **The agent must always ask for user confirmation before overwriting an existing file.**
- **Output**: Returns a success or error message.

**Example Agent Thought Process:**
> The user has approved the new Python script. I will now save it. I will call `write_file('path/to/new_script.py', '... a lot of python code ...')`.

## Rules & Safety
- The agent MUST always resolve relative paths or ask the user for the full path if ambiguous.
- The agent MUST ask for confirmation before using `write_file` on a path that it suspects may already exist, to prevent accidental data loss.
- The agent should handle file I/O errors gracefully and report them back to the user.
