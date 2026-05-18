import React, { useState, useEffect } from 'react';

interface AuditLog {
    timestamp: string;
    type: string;
    details: any;
}

const SecurityDashboard: React.FC = () => {
    const [logs, setLogs] = useState<AuditLog[]>([]);
    const [sandboxStatus, setSandboxStatus] = useState('ACTIVE');

    useEffect(() => {
        // Mock audit logs based on the recently implemented python backend
        setLogs([
            { timestamp: new Date().toISOString(), type: 'SANDBOX_BLOCK', details: { command: 'rm -rf /', reason: 'Blocked destructive operator' } },
            { timestamp: new Date().toISOString(), type: 'AUDIT_INIT', details: { status: 'Secure log chain started' } },
            { timestamp: new Date().toISOString(), type: 'SESSION_RESTORE', details: { id: 'c87-a21' } }
        ]);
    }, []);

    return (
        <div className="view-layer">
            <div className="view-header">
                <h2>Nexus Shield // Security</h2>
                <p className="view-subtitle">Heuristic protection and immutable audit logging.</p>
            </div>

            <div className="settings-grid">
                <div className="setting-card wide glass">
                    <h3>Command Sandbox</h3>
                    <div className="info-row">
                        <span>STATUS</span>
                        <span className="ok">HEURISTIC ANALYSIS ACTIVE</span>
                    </div>
                    <p style={{marginTop: '15px'}}>All tool executions are passed through a recursive parser to prevent prompt injection and unauthorized system access.</p>
                </div>

                <div className="setting-card wide glass">
                    <h3>Immutable Audit Log</h3>
                    <div className="system-dashboard" style={{maxHeight: '200px', overflowY: 'auto', fontSize: '11px', fontFamily: 'monospace'}}>
                        {logs.map((log, i) => (
                            <div key={i} style={{marginBottom: '5px', borderBottom: '1px solid var(--border)', paddingBottom: '5px'}}>
                                <span style={{color: 'var(--text-dim)'}}>[{log.timestamp}]</span> 
                                <span style={{color: log.type.includes('BLOCK') ? 'var(--red)' : 'var(--teal)', fontWeight: 'bold'}}> {log.type}</span>
                                <br/>
                                <span style={{color: 'var(--text)'}}>{JSON.stringify(log.details)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SecurityDashboard;
