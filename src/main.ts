import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';
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

interface SystemInfo {
    platform: string;
    os: string;
    arch: string;
    total_memory_mb: number;
    llama_cli: boolean;
    aether_dir: boolean;
    aether_link_active: boolean;
}

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
            <div class="info-row"><span>AetherLink</span><span class="${info.aether_link_active ? 'ok' : 'warn'}">${info.aether_link_active ? '🟢 Syncing' : '🟡 Disconnected'}</span></div>
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
    term.writeln('\x1b[1;34m  ║   TAURI EDITION // ' + labels[tier].padEnd(18) + '║\x1b[0m');
    term.writeln('\x1b[1;34m  ╚══════════════════════════════════════════╝\x1b[0m');
    term.writeln('');

    // Start Agent Process
    try {
        await invoke('start_agent');
        
        listen('agent-stdout', (event) => {
            const output = event.payload as string;
            term.write(output.replace(/\n/g, '\r\n'));
        });
        
        listen('agent-stderr', (event) => {
            const output = event.payload as string;
            term.write('\x1b[31m' + output.replace(/\n/g, '\r\n') + '\x1b[0m');
        });
    } catch (err) {
        term.writeln(`\x1b[1;31m[!] Failed to start agent: ${err}\x1b[0m`);
        return;
    }

    let input = '';
    term.onKey(({ key, domEvent }) => {
        if (domEvent.key === 'Enter') {
            term.write('\r\n');
            invoke('send_to_agent', { input: input });
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

// ── Nexus UI Logic ──
const nexusPanel = document.getElementById('nexus-panel')!;
document.getElementById('btn-nexus')?.addEventListener('click', () => {
    nexusPanel.classList.remove('hidden');
});
document.getElementById('btn-nexus-close')?.addEventListener('click', () => {
    nexusPanel.classList.add('hidden');
});

const nexusStatus = document.getElementById('nexus-status')!;

// ── Settings Panel ──
const settingsPanel = document.getElementById('settings-panel')!;
const btnSettings = document.getElementById('btn-settings')!;
const btnSettingsClose = document.getElementById('btn-settings-close')!;
const btnSettingsSave = document.getElementById('btn-settings-save')!;

let currentSettings: any = {};

btnSettings.addEventListener('click', async () => {
    settingsPanel.classList.remove('hidden');
    document.getElementById('settings-status')!.textContent = "Loading configuration...";
    try {
        currentSettings = await invoke('get_settings');
        
        (document.getElementById('setting-uncensored') as HTMLInputElement).checked = currentSettings.uncensored || false;
        (document.getElementById('setting-rag') as HTMLInputElement).checked = currentSettings.rag_enabled !== false;
        (document.getElementById('setting-mcp') as HTMLInputElement).checked = currentSettings.mcp_enabled || false;
        (document.getElementById('setting-auto-memory') as HTMLInputElement).checked = currentSettings.auto_memory !== false;
        (document.getElementById('setting-vault-path') as HTMLInputElement).value = currentSettings.vault_path || "~/Documents/Vault";
        (document.getElementById('setting-engine') as HTMLSelectElement).value = currentSettings.inference_engine || "ollama";
        
        document.getElementById('settings-status')!.textContent = "Configuration loaded.";
    } catch (e) {
        document.getElementById('settings-status')!.textContent = `Error loading config: ${e}`;
    }
});

btnSettingsClose.addEventListener('click', () => {
    settingsPanel.classList.add('hidden');
});

btnSettingsSave.addEventListener('click', async () => {
    document.getElementById('settings-status')!.textContent = "Saving...";
    currentSettings.uncensored = (document.getElementById('setting-uncensored') as HTMLInputElement).checked;
    currentSettings.rag_enabled = (document.getElementById('setting-rag') as HTMLInputElement).checked;
    currentSettings.mcp_enabled = (document.getElementById('setting-mcp') as HTMLInputElement).checked;
    currentSettings.auto_memory = (document.getElementById('setting-auto-memory') as HTMLInputElement).checked;
    currentSettings.vault_path = (document.getElementById('setting-vault-path') as HTMLInputElement).value;
    currentSettings.inference_engine = (document.getElementById('setting-engine') as HTMLSelectElement).value;
    
    try {
        await invoke('save_settings', { config: currentSettings });
        document.getElementById('settings-status')!.textContent = "Saved! Restart agent to apply.";
        setTimeout(() => {
            settingsPanel.classList.add('hidden');
        }, 1500);
    } catch (e) {
        document.getElementById('settings-status')!.textContent = `Error saving: ${e}`;
    }
});

// ── Model Manager ──
const modelsPanel = document.getElementById('models-panel')!;
const btnModels = document.getElementById('btn-models')!;
const btnModelsClose = document.getElementById('btn-models-close')!;
const btnModelPull = document.getElementById('btn-model-pull')!;
const modelPullName = document.getElementById('model-pull-name') as HTMLInputElement;
const modelsTableBody = document.getElementById('models-table-body')!;
const modelsStatus = document.getElementById('models-status')!;

async function loadModels() {
    modelsTableBody.innerHTML = `<tr><td colspan="3" style="padding: 10px; text-align: center; color: var(--text-dim);">Loading models...</td></tr>`;
    try {
        const models = await invoke<any[]>('list_models');
        if (models.length === 0) {
            modelsTableBody.innerHTML = `<tr><td colspan="3" style="padding: 10px; text-align: center; color: var(--text-dim);">No models found.</td></tr>`;
            return;
        }
        modelsTableBody.innerHTML = models.map(m => `
            <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 10px;">${m.name}</td>
                <td style="padding: 10px;">${m.size}</td>
                <td style="padding: 10px;">
                    <button class="btn btn-small btn-model-delete" data-name="${m.name}" style="color: var(--red); border-color: var(--red);">Delete</button>
                </td>
            </tr>
        `).join('');

        document.querySelectorAll('.btn-model-delete').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const name = (e.target as HTMLElement).getAttribute('data-name');
                if (name && confirm(`Delete model ${name}?`)) {
                    modelsStatus.textContent = `Deleting ${name}...`;
                    try {
                        await invoke('delete_model', { name });
                        modelsStatus.textContent = `Deleted ${name}.`;
                        loadModels();
                    } catch (err) {
                        modelsStatus.textContent = `Error: ${err}`;
                    }
                }
            });
        });
    } catch (e) {
        modelsTableBody.innerHTML = `<tr><td colspan="3" style="padding: 10px; color: var(--red);">Error loading models: ${e}</td></tr>`;
    }
}

btnModels.addEventListener('click', () => {
    modelsPanel.classList.remove('hidden');
    loadModels();
});

btnModelsClose.addEventListener('click', () => {
    modelsPanel.classList.add('hidden');
});

btnModelPull.addEventListener('click', async () => {
    const name = modelPullName.value.trim();
    if (!name) return;
    modelsStatus.textContent = `Pulling ${name}... this may take a while.`;
    btnModelPull.disabled = true;
    try {
        await invoke('pull_model', { name });
        modelsStatus.textContent = `Successfully pulled ${name}.`;
        modelPullName.value = '';
        loadModels();
    } catch (e) {
        modelsStatus.textContent = `Error pulling model: ${e}`;
    } finally {
        btnModelPull.disabled = false;
    }
});

// ── Vault Browser ──
const vaultPanel = document.getElementById('vault-panel')!;
const btnVault = document.getElementById('btn-context7')!;
const btnVaultClose = document.getElementById('btn-vault-close')!;
const vaultFileList = document.getElementById('vault-file-list')!;
const vaultFileName = document.getElementById('vault-file-name') as HTMLInputElement;
const vaultFileContent = document.getElementById('vault-file-content') as HTMLTextAreaElement;
const btnVaultSave = document.getElementById('btn-vault-save')!;
const btnVaultDelete = document.getElementById('btn-vault-delete')!;
const vaultStatus = document.getElementById('vault-status')!;

async function loadVaultFiles() {
    vaultFileList.innerHTML = `<div style="padding: 8px; color: var(--text-dim);">Loading...</div>`;
    try {
        const files = await invoke<string[]>('list_vault_files');
        if (files.length === 0) {
            vaultFileList.innerHTML = `<div style="padding: 8px; color: var(--text-dim);">Vault is empty.</div>`;
            return;
        }
        vaultFileList.innerHTML = files.map(f => `
            <div class="vault-file-item" data-name="${f}" style="padding: 8px; cursor: pointer; border-bottom: 1px solid var(--border); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" onmouseover="this.style.background='var(--border)'" onmouseout="this.style.background='transparent'">
                📄 ${f}
            </div>
        `).join('');

        document.querySelectorAll('.vault-file-item').forEach(item => {
            item.addEventListener('click', async (e) => {
                const filename = (e.currentTarget as HTMLElement).getAttribute('data-name');
                if (!filename) return;
                vaultStatus.textContent = `Loading ${filename}...`;
                try {
                    const content = await invoke<string>('read_vault_file', { filename });
                    vaultFileName.value = filename;
                    vaultFileContent.value = content;
                    vaultStatus.textContent = `Loaded ${filename}.`;
                } catch (err) {
                    vaultStatus.textContent = `Error: ${err}`;
                }
            });
        });
    } catch (e) {
        vaultFileList.innerHTML = `<div style="padding: 8px; color: var(--red);">Error: ${e}</div>`;
    }
}

btnVault.addEventListener('click', () => {
    vaultPanel.classList.remove('hidden');
    vaultPanel.style.display = 'flex'; // override hidden display:none
    loadVaultFiles();
});

btnVaultClose.addEventListener('click', () => {
    vaultPanel.classList.add('hidden');
    vaultPanel.style.display = '';
});

btnVaultSave.addEventListener('click', async () => {
    const filename = vaultFileName.value;
    const content = vaultFileContent.value;
    if (!filename) return;
    vaultStatus.textContent = `Saving ${filename}...`;
    try {
        await invoke('save_vault_file', { filename, content });
        vaultStatus.textContent = `Saved ${filename}.`;
    } catch (e) {
        vaultStatus.textContent = `Error saving: ${e}`;
    }
});

btnVaultDelete.addEventListener('click', async () => {
    const filename = vaultFileName.value;
    if (!filename) return;
    if (confirm(`Are you sure you want to delete ${filename} from AetherVault?`)) {
        vaultStatus.textContent = `Deleting ${filename}...`;
        try {
            await invoke('delete_vault_file', { filename });
            vaultStatus.textContent = `Deleted ${filename}.`;
            vaultFileName.value = '';
            vaultFileContent.value = '';
            loadVaultFiles();
        } catch (e) {
            vaultStatus.textContent = `Error deleting: ${e}`;
        }
    }
});

async function runNexusOptimization(type: string, enabled: boolean) {
    nexusStatus.textContent = `Processing: ${type}...`;
    try {
        const result = await invoke<string>('run_nexus_optimization', { optType: type, enabled: enabled });
        nexusStatus.textContent = `Status: ${result}`;
    } catch (err) {
        nexusStatus.textContent = `Error: ${err}`;
    }
}

document.getElementById('toggle-privacy')?.addEventListener('change', (e) => {
    runNexusOptimization('Privacy Shield', (e.target as HTMLInputElement).checked);
});

document.getElementById('toggle-gaming')?.addEventListener('change', (e) => {
    runNexusOptimization('Gaming Mode', (e.target as HTMLInputElement).checked);
});

document.getElementById('toggle-ai-bloat')?.addEventListener('change', (e) => {
    runNexusOptimization('AI Bloat Killer', (e.target as HTMLInputElement).checked);
});

document.getElementById('toggle-ghost')?.addEventListener('change', (e) => {
    runNexusOptimization('Ghost Mode', (e.target as HTMLInputElement).checked);
});

document.getElementById('btn-clean')?.addEventListener('click', () => {
    runNexusOptimization('System Deep Clean', true);
});

// ── Multimodal (Vision) ──
listen<string[]>('tauri://file-drop', event => {
    const files = event.payload;
    if (files && files.length > 0) {
        const file = files[0];
        term.write(`\r\n\x1b[35m[Aether Eye] Processing image: ${file}\x1b[0m\r\n`);
        invoke('send_to_agent', { input: `/vision ${file}` });
    }
});
