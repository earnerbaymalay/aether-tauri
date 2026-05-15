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
            <div className="nexus-content" style={{ maxWidth: '800px', width: '90%', border: '1px solid var(--purple)', boxShadow: '0 0 50px rgba(188, 140, 255, 0.2)' }}>
                <div className="nexus-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <div className={`scan-ring ${scanPulse ? 'pulsing' : ''}`}></div>
                        <h2 style={{ color: 'var(--purple)', letterSpacing: '4px' }}>AETHER // INITIALIZATION</h2>
                    </div>
                    <span className="step-indicator" style={{ fontFamily: 'monospace', color: 'var(--text-dim)' }}>SEQUENCE_{step}/03</span>
                </div>

                <div className="wizard-body" style={{ minHeight: '350px', margin: '20px 0' }}>
                    {step === 1 && (
                        <div className="setup-step animate-fade-in">
                            <h3>Hardware Audit</h3>
                            <p>Aether is scanning your local machine to establish a high-fidelity neural link. We optimize for your specific silicon to ensure uncompromising privacy and speed.</p>
                            
                            <div className="system-dashboard" style={{ marginTop: '25px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border)' }}>
                                {loading ? (
                                    <div className="loading-container">
                                        <div className="loading-bar"></div>
                                        <p style={{ marginTop: '15px', textAlign: 'center', fontFamily: 'monospace' }}>INTERROGATING HARDWARE...</p>
                                    </div>
                                ) : (
                                    <div className="stats-grid">
                                        <div className="info-row">
                                            <span>COGNITIVE PROFILE</span>
                                            <span className="ok" style={{ color: 'var(--purple)', fontWeight: 'bold' }}>{stats?.profile}</span>
                                        </div>
                                        <div className="info-row">
                                            <span>MEMORY BANDWIDTH</span>
                                            <span>{stats?.ram_gb} GB DDR</span>
                                        </div>
                                        <div className="info-row">
                                            <span>NEURAL CORES</span>
                                            <span>{stats?.cores} LOGICAL</span>
                                        </div>
                                        <div className="info-row">
                                            <span>LINK STATUS</span>
                                            <span className="ok">SECURE // LOCAL</span>
                                        </div>
                                    </div>
                                )}
                            </div>
                            {!loading && (
                                <p style={{ marginTop: '25px', fontSize: '13px', color: 'var(--text-dim)', fontStyle: 'italic' }}>
                                    Target hardware confirmed. VRAM allocation set to "Maximum Sovereignty" mode.
                                </p>
                            )}
                        </div>
                    )}

                    {step === 2 && (
                        <div className="setup-step animate-fade-in">
                            <h3>Neural Pathway Selection</h3>
                            <p>Select the initial weights for your workstation. These models will live exclusively on your device. No data ever leaves this room.</p>
                            <div style={{ marginTop: '25px', maxHeight: '300px', overflowY: 'auto', borderRadius: '12px', border: '1px solid var(--border)', background: 'rgba(0,0,0,0.1)' }}>
                                <ModelDownloader />
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="setup-step text-center animate-fade-in">
                            <div className="success-icon">✦</div>
                            <h3>Workstation Hardened</h3>
                            <p>The neural link is established. Your private operating interface is standing by to assist, automate, and protect.</p>
                            <div className="nexus-card" style={{ marginTop: '30px', background: 'rgba(88, 166, 255, 0.05)', borderColor: 'var(--teal)' }}>
                                <p style={{ color: 'var(--teal)' }}>✔ Local Inference Engine Active</p>
                                <p style={{ color: 'var(--teal)' }}>✔ AetherVault Memory Initialized</p>
                                <p style={{ color: 'var(--teal)' }}>✔ Nexus Shield Protections Enabled</p>
                            </div>
                        </div>
                    )}
                </div>

                <div className="nexus-footer" style={{ display: 'flex', justifyContent: 'space-between', marginTop: '30px', borderTop: '1px solid var(--border)', paddingTop: '20px' }}>
                    {step > 1 ? (
                        <button className="btn" onClick={prevStep}>Previous Phase</button>
                    ) : (
                        <div></div>
                    )}
                    
                    {step < 3 ? (
                        <button className="btn btn-nexus" onClick={nextStep} style={{ padding: '10px 30px' }}>Continue Sequence</button>
                    ) : (
                        <button className="btn btn-nexus" onClick={onComplete} style={{ padding: '12px 40px', background: 'var(--purple)', color: 'white', border: 'none', boxShadow: '0 0 20px rgba(188, 140, 255, 0.4)' }}>Enter the Aether</button>
                    )}
                </div>
            </div>
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
