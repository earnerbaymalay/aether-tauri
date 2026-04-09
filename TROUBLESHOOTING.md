# Aether Desktop troubleshooting guide

Common issues and solutions.

---

## Installation and build issues

### Node.js or Rust not found
Ensure Node.js (version 18+) and Rust are installed and configured correctly in your system's PATH.

### Tauri build errors
- Check the Tauri documentation for specific error messages.
- Ensure all Rust dependencies are met.

---

## Runtime issues

### Ollama not connecting
- Verify Ollama is running (`ollama serve`).
- Confirm that the correct model is pulled (`ollama pull llama3.2`).
- Check firewall settings if necessary.
- Ensure the Ollama endpoint in Aether Desktop settings is correct.

### AI models slow or unresponsive
- Check Ollama or llama.cpp logs for errors.
- Reduce resource usage if running other intensive applications.
- Consider using smaller AI models.

---

[MIT License](LICENSE)
