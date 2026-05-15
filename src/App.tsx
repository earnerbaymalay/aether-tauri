import React, { useState } from 'react';
import SetupWizard from './components/SetupWizard';
import DiagnosticDashboard from './components/DiagnosticDashboard';
import QRSync from './components/QRSync';
import IntegrationHub from './components/IntegrationHub';

type View = 'PATHWAYS' | 'DIAGNOSTICS' | 'INTEGRATION' | 'SYNC' | 'SETTINGS';
type LayoutMode = 'mission-control' | 'neural-link';

const App: React.FC = () => {
    const [showSetup, setShowSetup] = useState(true);
    const [view, setView] = useState<View>('PATHWAYS');
    const [layoutMode, setLayoutMode] = useState<LayoutMode>('mission-control');

    if (showSetup) {
        return <SetupWizard onComplete={() => setShowSetup(false)} />;
    }

    return (
        <div className={`neural-shell ${layoutMode}`}>
            <nav className="sidebar">
                <div className="nav-top">
                    <div className="nav-brand">
                        <span className="logo">🌌</span>
                        <div className="brand-text">
                            <span className="brand-name">AETHER</span>
                            <span className="brand-subtitle">NEURAL OS</span>
                        </div>
                    </div>
                </div>

                <div className="nav-group">
                    <button 
                        className={`nav-btn ${view === 'PATHWAYS' ? 'active' : ''}`} 
                        onClick={() => setView('PATHWAYS')}
                    >
                        <span className="nav-icon">🌌</span>
                        <span className="nav-label">Pathways</span>
                    </button>
                    <button 
                        className={`nav-btn ${view === 'DIAGNOSTICS' ? 'active' : ''}`} 
                        onClick={() => setView('DIAGNOSTICS')}
                    >
                        <span className="nav-icon">🩺</span>
                        <span className="nav-label">Diagnostics</span>
                    </button>
                    <button 
                        className={`nav-btn ${view === 'INTEGRATION' ? 'active' : ''}`} 
                        onClick={() => setView('INTEGRATION')}
                    >
                        <span className="nav-icon">🔌</span>
                        <span className="nav-label">Integrations</span>
                    </button>
                    <button 
                        className={`nav-btn ${view === 'SYNC' ? 'active' : ''}`} 
                        onClick={() => setView('SYNC')}
                    >
                        <span className="nav-icon">📱</span>
                        <span className="nav-label">Neural Link</span>
                    </button>
                </div>

                <div className="nav-bottom">
                    <button className="nav-btn" onClick={() => setLayoutMode(prev => prev === 'mission-control' ? 'neural-link' : 'mission-control')}>
                        <span className="nav-icon">🌓</span>
                        <span className="nav-label">{layoutMode === 'mission-control' ? 'Neural Link' : 'Mission Control'}</span>
                    </button>
                    <button className="nav-btn" onClick={() => setView('SETTINGS')}>
                        <span className="nav-icon">⚙️</span>
                        <span className="nav-label">Settings</span>
                    </button>
                </div>
            </nav>

            <div className="workspace">
                <main className="synapse">
                    {view === 'PATHWAYS' && (
                        <div className="view-layer">
                            <div className="view-header">
                                <h2>Neural Pathways</h2>
                                <p className="view-subtitle">Select a cognitive specialist.</p>
                            </div>
                            <div className="pathway-grid">
                                <div className="pathway-card">
                                    <div className="pathway-icon">🤖</div>
                                    <h3 className="pathway-title">AGENT</h3>
                                    <p className="pathway-model">Hermes-3-8B</p>
                                    <p className="pathway-desc">General intelligence and tool use.</p>
                                </div>
                                <div className="pathway-card">
                                    <div className="pathway-icon">⚡</div>
                                    <h3 className="pathway-title">TURBO</h3>
                                    <p className="pathway-model">Llama-3.2-3B</p>
                                    <p className="pathway-desc">High-speed conversational output.</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {view === 'DIAGNOSTICS' && <DiagnosticDashboard />}
                    {view === 'INTEGRATION' && <IntegrationHub />}
                    {view === 'SYNC' && <QRSync />}
                    {view === 'SETTINGS' && (
                        <div className="view-layer">
                            <div className="view-header">
                                <h2>System Settings</h2>
                            </div>
                            <p>Global configuration and neural link parameters.</p>
                        </div>
                    )}
                </main>

                <aside className="peripheral">
                    <div className="peripheral-section">
                        <h3 className="section-label">SYSTEM STATUS</h3>
                        <div className="system-dashboard">
                            <div className="info-row"><span>Status</span><span className="ok">NOMINAL</span></div>
                            <div className="info-row"><span>Mode</span><span>{layoutMode.toUpperCase()}</span></div>
                        </div>
                    </div>
                    <div className="peripheral-section">
                        <h3 className="section-label">QUICK ACTIONS</h3>
                        <div className="quick-actions">
                            <button className="btn btn-small btn-nexus" onClick={() => setView('SYNC')}>Sync Mobile</button>
                            <button className="btn btn-small" onClick={() => setView('DIAGNOSTICS')}>Run Health Check</button>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default App;
