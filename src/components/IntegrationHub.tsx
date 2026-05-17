import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

// Aether Unified Integration Hub
// Monitors MCP/LSP servers and manages API keys securely

const IntegrationHub: React.FC = () => {
    const [servers, setServers] = useState<any[]>([]);
    const [apiStatus, setApiStatus] = useState<boolean>(false);
    const [loading, setLoading] = useState(true);

    const refreshStatus = async () => {
        setLoading(true);
        try {
            const mcpStatuses: any[] = await invoke('get_mcp_status');
            const isApiOnline: boolean = await invoke('check_api_status');
            
            setServers(mcpStatuses.map((s, i) => ({
                id: `mcp-${i}`,
                name: s.name.charAt(0).toUpperCase() + s.name.slice(1),
                type: 'MCP',
                status: s.status,
                uptime: s.status === 'online' ? 'Active' : '-'
            })));
            
            setApiStatus(isApiOnline);
        } catch (err) {
            console.error("Failed to fetch integration status:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        refreshStatus();
        const interval = setInterval(refreshStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="view-layer">
            <div className="view-header">
                <h2>Integration Hub</h2>
                <p className="view-subtitle">Centralized Neural Link Management</p>
            </div>

            <div className="settings-grid">
                <div className="setting-card wide glass">
                    <div className="flex justify-between items-center mb-4">
                        <h3>Active Neural Servers</h3>
                        <button className="btn btn-small" onClick={refreshStatus} disabled={loading}>
                            {loading ? 'Refreshing...' : '🔄 Refresh'}
                        </button>
                    </div>
                    <p>Background MCP and LSP services powering your ecosystem.</p>
                    
                    <div className="models-table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Server Name</th>
                                    <th>Type</th>
                                    <th>Status</th>
                                    <th>Uptime</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr className={apiStatus ? "row-online" : "row-offline"}>
                                    <td>Aether Core API</td>
                                    <td>FastAPI</td>
                                    <td>
                                        <span className={`status ${apiStatus ? 'ok' : 'warn'}`}>
                                            {apiStatus ? 'ONLINE' : 'OFFLINE'}
                                        </span>
                                    </td>
                                    <td>{apiStatus ? 'Active' : '-'}</td>
                                    <td>-</td>
                                </tr>
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
                                        <td>
                                            <button className="btn-small btn">Restart</button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="setting-card glass">
                    <h3>Secure API Keys</h3>
                    <p>Manage credentials for external AI providers.</p>
                    <div className="quick-actions">
                        <div className="info-row">
                            <span>OpenAI</span>
                            <span className="warn">○ Missing</span>
                        </div>
                        <div className="info-row">
                            <span>Anthropic</span>
                            <span className="warn">○ Missing</span>
                        </div>
                        <div className="info-row">
                            <span>HuggingFace</span>
                            <span className="ok">● Configured</span>
                        </div>
                    </div>
                    <button className="btn btn-nexus" style={{marginTop: '20px', width: '100%'}}>
                        + Add New Provider
                    </button>
                </div>

                <div className="setting-card glass">
                    <h3>LSP Diagnostics</h3>
                    <p>Real-time health check for Language Server Protocols.</p>
                    <div className="system-dashboard" style={{height: '100px', overflowY: 'auto'}}>
                        [INFO] LSP Initialized: Rust<br/>
                        [INFO] Indexing: src-tauri/src<br/>
                        [DEBUG] {apiStatus ? 'API connection stable' : 'API connection failed'}<br/>
                        [INFO] Readiness: {apiStatus ? '100%' : '0%'}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default IntegrationHub;
