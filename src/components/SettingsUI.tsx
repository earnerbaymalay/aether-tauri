import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

// Replacing the terminal-based /settings flow
const SettingsUI: React.FC = () => {
    const [config, setConfig] = useState<any>({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchConfig = async () => {
            try {
                const data = await invoke('get_settings');
                setConfig(data);
            } catch (e) {
                console.error("Failed to load settings:", e);
            } finally {
                setLoading(false);
            }
        };
        fetchConfig();
    }, []);

    const handleSave = async () => {
        try {
            await invoke('save_settings', { config });
            alert("Settings saved successfully.");
        } catch (e) {
            console.error("Failed to save settings:", e);
        }
    };

    if (loading) return <div>Loading settings...</div>;

    return (
        <div className="settings-panel glass">
            <h2>Aether Configuration</h2>
            
            <div className="setting-group">
                <label>
                    <input 
                        type="checkbox" 
                        checked={config.uncensored || false} 
                        onChange={(e) => setConfig({...config, uncensored: e.target.checked})} 
                    />
                    Enable Uncensored Mode
                </label>
                <p className="help-text">Disables safety system prompts. Use with caution.</p>
            </div>

            <div className="setting-group">
                <label>
                    <input 
                        type="checkbox" 
                        checked={config.auto_memory || false} 
                        onChange={(e) => setConfig({...config, auto_memory: e.target.checked})} 
                    />
                    Auto-Memory (Shadow Monitor)
                </label>
                <p className="help-text">Passively distills conversations into AetherVault fragments.</p>
            </div>
            
            <div className="setting-group">
                <label>
                    Theme:
                    <select 
                        value={config.theme || 'cyan'} 
                        onChange={(e) => setConfig({...config, theme: e.target.value})}
                    >
                        <option value="cyan">Cyan (Default)</option>
                        <option value="purple">Purple</option>
                        <option value="green">Hacker Green</option>
                    </select>
                </label>
            </div>

            <button className="btn btn-nexus" onClick={handleSave}>Save Configuration</button>

            <style>{`
                .settings-panel { padding: 20px; }
                .setting-group { margin-bottom: 20px; }
                .setting-group label { display: block; font-weight: bold; margin-bottom: 5px; color: var(--text); }
                .help-text { font-size: 12px; color: var(--text-dim); }
            `}</style>
        </div>
    );
};

export default SettingsUI;
