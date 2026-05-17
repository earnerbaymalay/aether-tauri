import React, { useState } from 'react';
import SetupWizard from './components/SetupWizard';
import DiagnosticDashboard from './components/DiagnosticDashboard';
import QRSync from './components/QRSync';
import IntegrationHub from './components/IntegrationHub';

type View = 'PATHWAYS' | 'DIAGNOSTICS' | 'INTEGRATION' | 'SYNC' | 'SETTINGS';
type LayoutMode = 'mission-control' | 'neural-link';

interface Pathway {
    id: string;
    title: string;
    model: string;
    icon: string;
    description: string;
}

const PATHWAYS: Pathway[] = [
    {
        id: 'hermes-3-8b',
        title: 'AGENT',
        model: 'Hermes-3-8B',
        icon: '🤖',
        description: 'General intelligence and tool use.'
    },
    {
        id: 'llama-3.2-3b',
        title: 'TURBO',
        model: 'Llama-3.2-3B',
        icon: '⚡',
        description: 'High-speed conversational output.'
    },
    {
        id: 'deepseek-r1',
        title: 'LOGIC',
        model: 'DeepSeek-R1',
        icon: '🧠',
        description: 'Advanced reasoning and architecture.'
    }
];

const App: React.FC = () => {
    const [showSetup, setShowSetup] = useState(true);
    const [view, setView] = useState<View>('PATHWAYS');
    const [layoutMode, setLayoutMode] = useState<LayoutMode>('mission-control');
    const [activeModel, setActiveModel] = useState('hermes-3-8b');

    if (showSetup) {
        return <SetupWizard onComplete={() => setShowSetup(false)} />;
    }

    const activePathway = PATHWAYS.find(p => p.id === activeModel) || PATHWAYS[0];

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
                    {[
                        { id: 'PATHWAYS', icon: '🌌', label: 'Pathways' },
                        { id: 'DIAGNOSTICS', icon: '🩺', label: 'Diagnostics' },
                        { id: 'INTEGRATION', icon: '🔌', label: 'Integrations' },
                        { id: 'SYNC', icon: '📱', label: 'Neural Link' }
                    ].map(item => (
                        <button 
                            key={item.id}
                            className={`nav-btn ${view === item.id ? 'active' : ''}`} 
                            onClick={() => setView(item.id as View)}
                        >
                            <span className="nav-icon">{item.icon}</span>
                            <span className="nav-label">{item.label}</span>
                        </button>
                    ))}
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
                                <p className="view-subtitle">
                                    Select a cognitive specialist. Active: 
                                    <span className="active-model-tag">{activePathway.model}</span>
                                </p>
                            </div>
                            <div className="pathway-grid">
                                {PATHWAYS.map(pathway => (
                                    <div 
                                        key={pathway.id}
                                        className={`pathway-card ${activeModel === pathway.id ? 'active' : ''}`}
                                        onClick={() => setActiveModel(pathway.id)}
                                    >
                                        <div className="pathway-icon">{pathway.icon}</div>
                                        <h3 className="pathway-title">{pathway.title}</h3>
                                        <p className="pathway-model">{pathway.model}</p>
                                        <p className="pathway-desc">{pathway.description}</p>
                                    </div>
                                ))}
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
                            <div className="settings-grid">
                                <div className="setting-card">
                                    <h3>Model Configuration</h3>
                                    <p>Primary: {activePathway.model}</p>
                                    <button className="btn btn-small">Change Model</button>
                                </div>
                                <div className="setting-card">
                                    <h3>Neural Vault</h3>
                                    <p>Path: ~/.aether/vault</p>
                                    <button className="btn btn-small">Change Path</button>
                                </div>
                            </div>
                        </div>
                    )}
                </main>

                <aside className="peripheral">
                    <div className="peripheral-section">
                        <h3 className="section-label">SYSTEM STATUS</h3>
                        <div className="system-dashboard">
                            <div className="info-row"><span>Status</span><span className="ok">NOMINAL</span></div>
                            <div className="info-row"><span>Mode</span><span>{layoutMode.toUpperCase()}</span></div>
                             <div className="info-row"><span>Pathway</span><span>{activePathway.title}</span></div>
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
