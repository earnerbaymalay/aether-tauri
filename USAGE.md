# Aether Desktop usage guide

Instructions for setup, first launch, and configuration.

---

## Installation

### Requirements

- Node.js (version 18 or higher)
- Rust programming language
- Ollama (running locally) or llama.cpp

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/earnerbaymalay/aether-desktop.git
   cd aether-desktop
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start development mode:
   ```bash
   npm run tauri dev
   ```

4. For a production build:
   ```bash
   npm run tauri build
   ```

---

## Configuration

### Ollama integration

1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

2. Pull a model (e.g., Llama 3.2):
   ```bash
   ollama pull llama3.2
   ```

3. Configure the Ollama endpoint within Aether Desktop's settings.

### llama.cpp integration

(Instructions for llama.cpp will be added here based on future development.)

---

## Troubleshooting

See the separate `TROUBLESHOOTING.md` for common issues and solutions.

---

[MIT License](LICENSE)
