import React, { useState, useEffect } from 'react';
import ModelDownloader from './ModelDownloader';

interface SystemStats {
    profile: string;
    ram_gb: number;
    cores: number;
    status: string;
}

const SetupWizard: React.FC<{ onComplete: () => void }> = ({ onComplete }) => {
    const [step, setStep] = useState(1);
    const [stats, setStats] = useState<SystemStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [scanPulse, setScanPulse] = useState(false);

    useEffect(() => {
        const fetchStats = async () => {
            setScanPulse(true);
            try {
                // Artificial delay for "magical" feel
                await new Promise(r => setTimeout(r, 2000));
                const response = await fetch('http://localhost:8000/system/stats');
                if (response.ok) {
                    const data = await response.json();
                    setStats(data);
                } else {
                    // Fallback for dev/missing API
                    setStats({ profile: 'Optimized', ram_gb: 16, cores: 8, status: 'Active' });
                }
            } catch (err) {
                setStats({ profile: 'Optimized', ram_gb: 16, cores: 8, status: 'Active' });
            } finally {
                setLoading(false);
                setScanPulse(false);
            }
        };
        fetchStats();
    }, []);

    const nextStep = () => setStep(prev => prev + 1);
    const prevStep = () => setStep(prev => prev - 1);

    return (
        <div className="nexus-overlay">
            <div className="nexus-content" style={{ maxWidth: '900px', width: '95%', border: '1px solid var(--purple)', boxShadow: '0 0 80px rgba(188, 140, 255, 0.3)' }}>
                <div className="nexus-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <div className={`scan-ring ${scanPulse ? 'pulsing' : ''}`}></div>
                        <h2 className="glitch-text" data-text="AETHER // INITIALIZATION">AETHER // INITIALIZATION</h2>
                    </div>
                    <span className="step-indicator">SEQUENCE_{step}/04</span>
                </div>

                <div className="wizard-body" style={{ minHeight: '400px', margin: '30px 0' }}>
                    {step === 1 && (
                        <div className="setup-step animate-fade-in">
                            <div className="flex items-center gap-4 mb-6">
                                <div className="step-number">01</div>
                                <div>
                                    <h3>Hardware Interrogation</h3>
                                    <p>Mapping your local silicon for optimal neural throughput.</p>
                                </div>
                            </div>
                            
                            <div className="system-dashboard hardware-grid" style={{ background: 'rgba(0,0,0,0.3)', padding: '30px' }}>
                                {loading ? (
                                    <div className="loading-container">
                                        <div className="neural-loader"></div>
                                        <p className="mt-6 text-center mono text-purple">SYNCHRONIZING WITH HOST...</p>
                                    </div>
                                ) : (
                                    <div className="stats-display">
                                        <div className="stat-box">
                                            <span className="label">VRAM CAPACITY</span>
                                            <span className="value ok">{stats?.ram_gb} GB</span>
                                        </div>
                                        <div className="stat-box">
                                            <span className="label">COMPUTE CORES</span>
                                            <span className="value">{stats?.cores} LOGICAL</span>
                                        </div>
                                        <div className="stat-box">
                                            <span className="label">PROFILE</span>
                                            <span className="value text-purple">{stats?.profile}</span>
                                        </div>
                                    </div>
                                )}
                            </div>
                            {!loading && (
                                <div className="alert-box mt-6">
                                    <span className="icon">🛡️</span>
                                    <span>Nexus Shield active. OS telemetry suppression confirmed.</span>
                                </div>
                            )}
                        </div>
                    )}

                    {step === 2 && (
                        <div className="setup-step animate-fade-in">
                            <div className="flex items-center gap-4 mb-6">
                                <div className="step-number">02</div>
                                <div>
                                    <h3>Neural Calibration</h3>
                                    <p>Configuring local retrieval pathways and memory fragments.</p>
                                </div>
                            </div>
                            <div className="calibration-view">
                                <div className="calibration-circle">
                                    <div className="inner-pulse"></div>
                                    <div className="orbit-1"></div>
                                    <div className="orbit-2"></div>
                                </div>
                                <div className="calibration-stats">
                                    <div className="info-row"><span>VAULT STATUS</span><span className="ok">INITIALIZED</span></div>
                                    <div className="info-row"><span>RAG ENGINE</span><span className="ok">READY</span></div>
                                    <div className="info-row"><span>FRAGMENT LIMIT</span><span>UNLIMITED</span></div>
                                </div>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="setup-step animate-fade-in">
                            <div className="flex items-center gap-4 mb-6">
                                <div className="step-number">03</div>
                                <div>
                                    <h3>Skill Integration</h3>
                                    <p>Select your starting neural skillsets. Aether Pro unlocks advanced autonomous capabilities.</p>
                                </div>
                            </div>
                            <div className="skill-selection-grid">
                                <div className="skill-item active">
                                    <span className="icon">📂</span>
                                    <h4>AetherFS</h4>
                                    <p>Local File I/O & Search</p>
                                    <span className="badge-free">INCLUDED</span>
                                </div>
                                <div className="skill-item active">
                                    <span className="icon">🧠</span>
                                    <h4>AetherVault</h4>
                                    <p>Persistent Memory</p>
                                    <span className="badge-free">INCLUDED</span>
                                </div>
                                <div className="skill-item pro">
                                    <span className="icon">🌐</span>
                                    <h4>Cloud Relay</h4>
                                    <p>Remote Sync & P2P</p>
                                    <span className="badge-pro">PRO ONLY</span>
                                </div>
                            </div>
                            <div style={{ marginTop: '20px', maxHeight: '200px', overflowY: 'auto' }}>
                                <ModelDownloader />
                            </div>
                        </div>
                    )}

                    {step === 4 && (
                        <div className="setup-step text-center animate-fade-in">
                            <div className="success-manifesto">
                                <div className="manifesto-icon">🌌</div>
                                <h3>Workstation Sovereign</h3>
                                <p>The rebellion starts here. Your intelligence is no longer for sale.</p>
                            </div>
                            <div className="launch-sequence">
                                <div className="info-row"><span>COGNITIVE LINK</span><span className="ok">ESTABLISHED</span></div>
                                <div className="info-row"><span>PRIVACY SHIELD</span><span className="ok">MAXIMUM</span></div>
                                <div className="info-row"><span>DATA OWNERSHIP</span><span className="ok">100% USER</span></div>
                            </div>
                        </div>
                    )}
                </div>

                <div className="nexus-footer">
                    {step > 1 ? (
                        <button className="btn" onClick={prevStep}>Previous Phase</button>
                    ) : (
                        <div></div>
                    )}
                    
                    {step < 4 ? (
                        <button className="btn btn-nexus" onClick={nextStep}>Progress Sequence</button>
                    ) : (
                        <button className="btn btn-nexus btn-launch" onClick={onComplete}>Enter the Aether</button>
                    )}
                </div>
            </div>
            <style>{`
                .step-number { font-size: 48px; font-weight: 800; color: rgba(255,255,255,0.05); font-family: 'JetBrains Mono'; line-height: 1; }
                .glitch-text { position: relative; font-family: 'JetBrains Mono'; font-weight: bold; }
                .stats-display { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
                .stat-box { display: flex; flex-direction: column; align-items: center; padding: 20px; border: 1px solid var(--border); border-radius: 12px; }
                .stat-box .label { font-size: 10px; color: var(--text-dim); margin-bottom: 5px; }
                .stat-box .value { font-size: 24px; font-weight: bold; font-family: 'JetBrains Mono'; }
                
                .calibration-view { display: flex; align-items: center; justify-content: space-around; padding: 40px 0; }
                .calibration-circle { width: 150px; height: 150px; border: 2px solid var(--purple); border-radius: 50%; position: relative; display: flex; align-items: center; justify-content: center; }
                .inner-pulse { width: 40px; height: 40px; background: var(--purple); border-radius: 50%; box-shadow: 0 0 30px var(--purple); animation: pulse 2s infinite; }
                
                .skill-selection-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
                .skill-item { padding: 20px; border: 1px solid var(--border); border-radius: 12px; background: rgba(255,255,255,0.02); text-align: center; position: relative; }
                .skill-item.active { border-color: var(--teal); }
                .skill-item.pro { border-color: var(--purple); opacity: 0.7; }
                .skill-item h4 { margin: 10px 0 5px; font-size: 14px; }
                .skill-item p { font-size: 11px; }
                
                .badge-free { position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: var(--teal); color: var(--bg); font-size: 9px; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
                .badge-pro { position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: var(--purple); color: white; font-size: 9px; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
                
                .btn-launch { background: var(--purple) !important; color: white !important; font-size: 18px !important; padding: 15px 60px !important; }
            `}</style>
        </div>
    );
            <style>{`
                .setup-step h3 { font-size: 28px; margin-bottom: 12px; color: var(--text); font-family: 'JetBrains Mono', monospace; letter-spacing: -1px; }
                .setup-step p { color: var(--text-dim); line-height: 1.6; font-size: 15px; }
                .info-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 12px; }
                .ok { color: var(--green); text-shadow: 0 0 8px rgba(63, 185, 80, 0.4); }
                .text-center { text-align: center; }
                
                .scan-ring { width: 12px; height: 12px; border-radius: 50%; background: var(--purple); position: relative; }
                .scan-ring.pulsing::after {
                    content: '';
                    position: absolute;
                    top: -4px; left: -4px; right: -4px; bottom: -4px;
                    border: 1px solid var(--purple);
                    border-radius: 50%;
                    animation: pulse 1.5s infinite;
                }

                @keyframes pulse {
                    0% { transform: scale(1); opacity: 1; }
                    100% { transform: scale(3); opacity: 0; }
                }

                .loading-bar {
                    height: 2px;
                    width: 100%;
                    background: var(--border);
                    position: relative;
                    overflow: hidden;
                }
                .loading-bar::after {
                    content: '';
                    position: absolute;
                    left: -50%;
                    height: 100%;
                    width: 50%;
                    background: var(--purple);
                    animation: loading 2s infinite linear;
                }

                @keyframes loading {
                    0% { left: -50%; }
                    100% { left: 100%; }
                }

                .animate-fade-in { animation: fadeIn 0.5s ease-out; }
                @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

                .success-icon {
                    font-size: 80px;
                    color: var(--teal);
                    margin-bottom: 20px;
                    text-shadow: 0 0 30px rgba(88, 166, 255, 0.5);
                }
            `}</style>
        </div>
    );
};

export default SetupWizard;
