import React, { useState, useEffect } from 'react';

interface Skill {
    id: string;
    name: string;
    author: string;
    tier: 'free' | 'pro';
    description: string;
}

const Marketplace: React.FC = () => {
    const [skills, setSkills] = useState<Skill[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Simulating fetch from marketplace logic implemented in python
        setTimeout(() => {
            setSkills([
                { id: "git-tools", name: "Git Operations", author: "core", tier: "free", description: "Manage git repositories locally." },
                { id: "advanced-search", name: "Deep Web Search", author: "community", tier: "free", description: "Search the web using SearxNG." },
                { id: "cloud-relay", name: "AetherLink Cloud Relay", author: "official", tier: "pro", description: "Sync vault across non-LAN networks. Requires Aether Pro." },
                { id: "vision-pro", name: "Enhanced Aether Eye", author: "official", tier: "pro", description: "High-resolution screen analysis and multi-monitor support." }
            ]);
            setLoading(false);
        }, 1000);
    }, []);

    return (
        <div className="view-layer">
            <div className="view-header">
                <h2>Skill Marketplace</h2>
                <p className="view-subtitle">Expand your agent's capabilities with verified local tools.</p>
            </div>

            <div className="grid">
                {skills.map(skill => (
                    <div key={skill.id} className={`card ${skill.tier === 'pro' ? 'pro-tier' : ''}`}>
                        <div className="tag">{skill.author.toUpperCase()} // {skill.tier.toUpperCase()}</div>
                        <h3>{skill.name}</h3>
                        <p>{skill.description}</p>
                        <button className={`btn btn-small ${skill.tier === 'pro' ? 'btn-nexus' : ''}`} style={{marginTop: '20px'}}>
                            {skill.tier === 'pro' ? 'Upgrade to Install' : 'Install Skill'}
                        </button>
                    </div>
                ))}
            </div>

            <style>{`
                .pro-tier { border-color: var(--purple) !important; box-shadow: 0 0 15px rgba(188, 140, 255, 0.1); }
                .pro-tier .tag { color: var(--purple); }
            `}</style>
        </div>
    );
};

export default Marketplace;
