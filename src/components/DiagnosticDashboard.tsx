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

    const fetchStatus = async () => {
        try {
            const response = await fetch('http://localhost:8000/system/stats');
            if (response.ok) {
                const data = await response.json();
                setSystemHealth(data.agent_active ? 100 : 50);
                
                // Construct "servers" based on real status
                setServers([
                    { id: 'agent-core', name: 'Aether Agent', type: 'Core', status: data.agent_active ? 'online' : 'error', uptime: 'N/A' },
                    { id: 'api-server', name: 'Engine Room API', type: 'API', status: 'online', uptime: 'N/A' }
                ]);

                if (data.last_watchdog_event && !logs.includes(data.last_watchdog_event)) {
                    addLog(data.last_watchdog_event);
                }
            }
        } catch (err) {
            console.error("Failed to fetch status", err);
            setSystemHealth(0);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleRepair = async () => {
        setRepairing(true);
        addLog("Initiating ecosystem repair sequence...");
        
        try {
            const response = await fetch('http://localhost:8000/system/repair', { method: 'POST' });
            if (response.ok) {
                const data = await response.json();
                addLog(data.message || "Repair completed successfully.");
            }
        } catch (err) {
            addLog("Error: Could not contact repair endpoint.");
        }

        await fetchStatus();
        setRepairing(false);
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
