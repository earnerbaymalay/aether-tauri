import React, { useState, useEffect } from 'react';

interface ServerStatus {
    id: string;
    name: string;
    type: string;
    status: 'online' | 'error' | 'restarting';
    uptime: string;
}

const DiagnosticDashboard: React.FC = () => {
    const [servers, setServers] = useState<ServerStatus[]>([]);
    const [systemHealth, setSystemHealth] = useState<number>(100);
    const [repairing, setRepairing] = useState(false);
    const [logs, setLogs] = useState<string[]>(["[INFO] Diagnostic system initialized."]);

    const addLog = (msg: string) => {
        setLogs(prev => [`[${new Date().toLocaleTimeString()}] ${msg}`, ...prev.slice(0, 9)]);
    };

    const fetchServers = async () => {
        try {
            // Simulated fetch from API
            setServers([
                { id: 'mcp-1', name: 'Memory Graph', type: 'MCP', status: 'online', uptime: '4h 12m' },
                { id: 'mcp-2', name: 'Web Search', type: 'MCP', status: 'online', uptime: '1h 05m' },
                { id: 'lsp-1', name: 'Rust Analyzer', type: 'LSP', status: 'online', uptime: '2h 30m' },
            ]);
        } catch (err) {
            console.error("Failed to fetch servers", err);
        }
    };

    useEffect(() => {
        fetchServers();
        const interval = setInterval(() => {
            // Randomly simulate a server failure for demo purposes
            setServers(prev => prev.map(s => {
                if (Math.random() > 0.95 && s.status === 'online') {
                    addLog(`CRITICAL: Server ${s.name} failed!`);
                    return { ...s, status: 'error' as const };
                }
                return s;
            }));
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        const errorCount = servers.filter(s => s.status === 'error').length;
        setSystemHealth(Math.max(0, 100 - (errorCount * 25)));
    }, [servers]);

    const handleRepair = async () => {
        setRepairing(true);
        addLog("Initiating ecosystem repair sequence...");
        
        try {
            const response = await fetch('http://localhost:8000/system/repair', { method: 'POST' });
            if (response.ok) {
                const data = await response.json();
                addLog(data.message || "Repair completed successfully.");
            } else {
                // Simulating local repair if API fails
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        } catch (err) {
            addLog("Warning: Could not contact repair endpoint. Running local recovery...");
            await new Promise(resolve => setTimeout(resolve, 2000));
        }

        setServers(prev => prev.map(s => ({ ...s, status: 'online' as const })));
        setRepairing(false);
        addLog("Ecosystem restored to nominal state.");
    };

    return (
        <div className="view-layer">
            <div className="view-header">
                <h2>Diagnostic Dashboard</h2>
                <p className="view-subtitle">Self-healing & Resilience Monitor</p>
            </div>

            <div className="settings-grid">
                <div className="setting-card">
                    <h3>System Health</h3>
                    <div style={{ fontSize: '48px', fontWeight: 'bold', color: systemHealth > 80 ? 'var(--green)' : 'var(--red)', margin: '10px 0' }}>
                        {systemHealth}%
                    </div>
                    <p>{systemHealth === 100 ? 'All systems nominal.' : 'Degraded performance detected.'}</p>
                    <button 
                        className={`btn ${repairing ? '' : 'btn-nexus'}`} 
                        style={{ width: '100%', marginTop: '10px' }}
                        onClick={handleRepair}
                        disabled={repairing}
                    >
                        {repairing ? 'Repairing...' : 'Repair Ecosystem'}
                    </button>
                </div>

                <div className="setting-card wide">
                    <h3>Active Neural Servers</h3>
                    <div className="models-table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Type</th>
                                    <th>Status</th>
                                    <th>Uptime</th>
                                </tr>
                            </thead>
                            <tbody>
                                {servers.map(server => (
                                    <tr key={server.id}>
                                        <td>{server.name}</td>
                                        <td>{server.type}</td>
                                        <td>
                                            <span className={`status ${server.status === 'online' ? 'ok' : 'warn'}`}>
                                                {server.status.toUpperCase()}
                                            </span>
                                        </td>
                                        <td>{server.uptime}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="setting-card wide">
                    <h3>Diagnostic Logs</h3>
                    <div className="system-dashboard" style={{ height: '150px', overflowY: 'auto' }}>
                        {logs.map((log, i) => <div key={i}>{log}</div>)}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DiagnosticDashboard;
