import { invoke } from '@tauri-apps/api/tauri';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';

// ── Initialize Terminal ──
const term = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
    theme: {
        background: '#0d1117',
        foreground: '#e6edf3',
        cursor: '#58a6ff',
        selectionBackground: '#58a6ff40',
        black: '#0d1117',
        red: '#ff7b72',
        green: '#3fb950',
        yellow: '#ffa657',
        blue: '#58a6ff',
        magenta: '#bc8cff',
        cyan: '#79c0ff',
        white: '#e6edf3',
    },
});

const fitAddon = new FitAddon();
term.loadAddon(fitAddon);

// ── State ──
let currentTier: string | null = null;

// ── System Info ──
async function loadSystemInfo() {
    try {
        const info = await invoke<SystemInfo>('get_system_info');
        document.getElementById('system-info')!.innerHTML = `
            <div class="info-row"><span>Platform</span><span>${info.platform}</span></div>
            <div class="info-row"><span>OS</span><span>${info.os}</span></div>
            <div class="info-row"><span>Arch</span><span>${info.arch}</span></div>
            <div class="info-row"><span>Memory</span><span>${(info.total_memory_mb / 1024).toFixed(1)} GB</span></div>
            <div class="info-row"><span>llama-cli</span><span class="${info.llama_cli ? 'ok' : 'warn'}">${info.llama_cli ? '✓ Found' : '✗ Not found'}</span></div>
            <div class="info-row"><span>Aether dir</span><span class="${info.aether_dir ? 'ok' : 'warn'}">${info.aether_dir ? '✓ Found' : '✗ Not found'}</span></div>
        `;
        document.getElementById('system-status')!.textContent = info.llama_cli ? '🟢 Ready' : '🟡 Setup needed';
    } catch (err) {
        document.getElementById('system-info')!.innerHTML = `<p class="error">Failed to load: ${err}</p>`;
    }
}

// ── Pathway Selection ──
document.querySelectorAll('.pathway-card').forEach(card => {
    card.addEventListener('click', () => {
        const tier = card.getAttribute('data-tier');
        if (tier) selectTier(tier);
    });
});

async function selectTier(tier: string) {
    currentTier = tier;
    const models: Record<string, string> = {
        agent: 'hermes-3-8b.gguf',
        turbo: 'llama-3.2-3b.gguf',
        code: 'qwen-coder-3b.gguf',
        logic: 'deepseek-r1-1.5b.gguf',
    };
    const labels: Record<string, string> = {
        agent: 'AGENT (Hermes-8B)',
        turbo: 'TURBO (Llama-3B)',
        code: 'CODE (Qwen-3B)',
        logic: 'LOGIC (DeepSeek)',
    };

    document.getElementById('pathway-selector')!.classList.add('hidden');
    document.getElementById('terminal-container')!.classList.remove('hidden');
    document.getElementById('tier-label')!.textContent = labels[tier];

    // Open terminal
    const terminalContainer = document.getElementById('terminal')!;
    terminalContainer.innerHTML = '';
    term.open(terminalContainer);
    fitAddon.fit();

    // Boot message
    term.writeln('\x1b[1;34m  ╔══════════════════════════════════════════╗\x1b[0m');
    term.writeln('\x1b[1;34m  ║       🌌  A E T H E R  🌌              ║\x1b[0m');
    term.writeln('\x1b[1;34m  ║   DESKTOP EDITION // ' + labels[tier].padEnd(16) + '║\x1b[0m');
    term.writeln('\x1b[1;34m  ╚══════════════════════════════════════════╝\x1b[0m');
    term.writeln('');

    // Check for model
    const home = await invoke<string>('path_home_dir');
    const modelPath = `${home}/aether/models/${models[tier]}`;

    // Try to run llama-cli (in real implementation, use Tauri shell API)
    term.writeln('\x1b[1;32m[●]\x1b[0m Loading model: ' + models[tier]);
    term.writeln('\x1b[1;32m[●]\x1b[0m Threads: ' + navigator.hardwareConcurrency);
    term.writeln('');

    if (!currentTier) return;
    term.write('\x1b[1;34mYou:\x1b[0m ');

    // Handle user input
    let input = '';
    term.onKey(({ key, domEvent }) => {
        if (domEvent.key === 'Enter') {
            term.writeln('');
            if (input.trim()) {
                term.writeln(`\x1b[1;35mAI:\x1b[0m [Processing: "${input}"]`);
                term.writeln('');
                term.write('\x1b[1;34mYou:\x1b[0m ');
            }
            input = '';
        } else if (domEvent.key === 'Backspace') {
            if (input.length > 0) {
                input = input.slice(0, -1);
                term.write('\b \b');
            }
        } else if (key.length === 1) {
            input += key;
            term.write(key);
        }
    });
}

// ── Back button ──
document.getElementById('btn-back')?.addEventListener('click', () => {
    term.dispose();
    document.getElementById('terminal-container')!.classList.add('hidden');
    document.getElementById('pathway-selector')!.classList.remove('hidden');
    currentTier = null;
});

// ── Benchmark ──
document.getElementById('btn-benchmark')?.addEventListener('click', async () => {
    const home = await invoke<string>('path_home_dir');
    const modelPath = `${home}/aether/models/llama-3.2-3b.gguf`;

    term.writeln('\x1b[1;33m[*]\x1b[0m Running benchmark...');
    try {
        const result = await invoke<BenchmarkResult>('run_benchmark', {
            args: { model_path: modelPath, threads: 4 }
        });
        term.writeln(`\x1b[1;32m[+]\x1b[0m ${result.tokens_per_sec.toFixed(1)} tokens/sec`);
    } catch (err) {
        term.writeln(`\x1b[1;31m[!]\x1b[0m Benchmark failed: ${err}`);
    }
});

// ── Init ──
loadSystemInfo();
