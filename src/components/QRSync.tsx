import React from 'react';

const QRSync: React.FC = () => {
    return (
        <div className="nexus-card" style={{ textAlign: 'center', padding: '40px' }}>
            <h3>Neural Link // Mobile Sync</h3>
            <p style={{ color: 'var(--text-dim)', marginBottom: '20px' }}>
                Scan to handoff your session to the Aether mobile node.
            </p>
            
            <div className="qr-container" style={{ 
                background: 'white', 
                padding: '20px', 
                display: 'inline-block', 
                borderRadius: '12px',
                marginBottom: '20px'
            }}>
                {/* Mock QR Code using CSS Grid */}
                <div style={{ 
                    display: 'grid', 
                    gridTemplateColumns: 'repeat(10, 15px)', 
                    gridTemplateRows: 'repeat(10, 15px)',
                    gap: '2px',
                    background: 'white'
                }}>
                    {Array.from({ length: 100 }).map((_, i) => (
                        <div key={i} style={{ 
                            background: Math.random() > 0.5 ? 'black' : 'white',
                            width: '15px',
                            height: '15px'
                        }} />
                    ))}
                </div>
            </div>
            
            <div className="sync-info" style={{ fontSize: '12px', color: 'var(--teal)', fontFamily: 'monospace' }}>
                P2P Link: ACTIVE<br/>
                Node ID: AETHER-UX-77
            </div>
        </div>
    );
};

export default QRSync;
