import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

interface ModelEntry {
  name: string;
  url: string;
  hash: string;
  size: number;
}

interface ModelManifest {
  models: ModelEntry[];
}

const ModelDownloader: React.FC = () => {
  const [manifest, setManifest] = useState<ModelManifest | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string>('');
  const [downloading, setDownloading] = useState<string | null>(null);

  const MANIFEST_URL = 'https://raw.githubusercontent.com/earnerbaymalay/aether-tauri/main/agent/models.json';

  useEffect(() => {
    fetchManifest();
  }, []);

  const fetchManifest = async () => {
    setLoading(true);
    try {
      const data: ModelManifest = await invoke('fetch_model_manifest', { url: MANIFEST_URL });
      setManifest(data);
    } catch (err) {
      setStatus(`Error fetching manifest: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  const downloadModel = async (entry: ModelEntry) => {
    setDownloading(entry.name);
    setStatus(`Downloading ${entry.name}...`);
    try {
      await invoke('download_model_from_manifest', { entry });
      setStatus(`${entry.name} downloaded and verified successfully!`);
    } catch (err) {
      setStatus(`Error downloading ${entry.name}: ${err}`);
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="setting-card glass">
      <h3>Model Registry</h3>
      <p>Curated neural models optimized for Aether's hardware tiers.</p>

      {loading && <p className="animate-pulse">Loading manifest from registry...</p>}

      {status && (
        <div className={`mb-4 p-2 rounded text-sm ${status.includes('Error') ? 'bg-red-900/50' : 'bg-teal-900/50'}`}>
          {status}
        </div>
      )}

      {!loading && manifest && (
        <div className="space-y-3 mt-4">
          {manifest.models.map((model) => (
            <div key={model.name} className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
              <div>
                <span className="font-medium text-white">{model.name}</span>
                <div className="text-xs text-slate-400">{(model.size / 1024 / 1024).toFixed(2)} MB</div>
              </div>
              <button
                onClick={() => downloadModel(model)}
                disabled={downloading === model.name}
                className="btn btn-small"
              >
                {downloading === model.name ? 'Downloading...' : 'Pull'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModelDownloader;
