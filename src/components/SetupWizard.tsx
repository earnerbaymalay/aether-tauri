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

    useEffect(() => {
        const fetchStats = async () => {
            try {
                // Attempt to fetch from the local API server
                const response = await fetch('http://localhost:8000/system/stats');
                if (response.ok) {
                    const data = await response.json();
                    setStats(data);
                } else {
                    throw new Error('API not available');
                }
            } catch (err) {
                // Fallback to mock data if API fails
                setStats({
                    profile: "Lite (Mock)",
                    ram_gb: 8,
                    cores: 6,
                    status: "Healthy"
                });
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    const nextStep = () => setStep(prev => prev + 1);
    const prevStep = () => setStep(prev => prev - 1);

    return (
        <div className="nexus-overlay">
            <div className="nexus-content" style={{ maxWidth: '800px', width: '90%' }}>
                <div className="nexus-header">
                    <h2>AETHER // SETUP WIZARD</h2>
                    <span className="step-indicator">Step {step} of 3</span>
                </div>

                <div className="wizard-body" style={{ minHeight: '300px', margin: '20px 0' }}>
                    {step === 1 && (
                        <div className="setup-step">
                            <h3>Welcome to Aether</h3>
                            <p>Let's prepare your local neural environment. First, we've performed a hardware audit.</p>
                            
                            <div className="system-dashboard" style={{ marginTop: '20px' }}>
                                {loading ? (
                                    <p>Auditing hardware...</p>
                                ) : (
                                    <>
                                        <div className="info-row">
                                            <span>Profile</span>
                                            <span className="ok">{stats?.profile}</span>
                                        </div>
                                        <div className="info-row">
                                            <span>RAM</span>
                                            <span>{stats?.ram_gb} GB</span>
                                        </div>
                                        <div className="info-row">
                                            <span>CPU Cores</span>
                                            <span>{stats?.cores}</span>
                                        </div>
                                        <div className="info-row">
                                            <span>System Status</span>
                                            <span className="ok">{stats?.status}</span>
                                        </div>
                                    </>
                                )}
                            </div>
                            <p style={{ marginTop: '20px', fontSize: '13px', color: 'var(--text-dim)' }}>
                                Your system is capable of running most quantized models efficiently.
                            </p>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="setup-step">
                            <h3>Model Selection</h3>
                            <p>Choose the initial neural weights to download for your workstation.</p>
                            <div style={{ marginTop: '20px', maxHeight: '300px', overflowY: 'auto' }}>
                                <ModelDownloader />
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="setup-step text-center">
                            <div className="pathway-icon" style={{ fontSize: '64px', marginBottom: '20px' }}>🚀</div>
                            <h3>Ecosystem Ready</h3>
                            <p>Your neural link is established and the local workstation is fully configured.</p>
                            <div className="nexus-card" style={{ marginTop: '30px' }}>
                                <p>• Local Inference Enabled</p>
                                <p>• AetherVault Initialized</p>
                                <p>• MCP Servers Standing By</p>
                            </div>
                        </div>
                    )}
                </div>

                <div className="nexus-footer" style={{ display: 'flex', justifyContent: 'space-between', marginTop: '30px' }}>
                    {step > 1 ? (
                        <button className="btn" onClick={prevStep}>Back</button>
                    ) : (
                        <div></div>
                    )}
                    
                    {step < 3 ? (
                        <button className="btn btn-nexus" onClick={nextStep}>Continue</button>
                    ) : (
                        <button className="btn btn-nexus" onClick={onComplete}>Enter Aether</button>
                    )}
                </div>
            </div>
            <style>{`
                .setup-step h3 { font-size: 24px; margin-bottom: 12px; color: var(--teal); }
                .setup-step p { color: var(--text-dim); line-height: 1.6; }
                .info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border); font-family: monospace; }
                .ok { color: var(--green); }
                .text-center { text-align: center; }
            `}</style>
        </div>
    );
};

export default SetupWizard;
