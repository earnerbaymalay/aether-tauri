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

  const MANIFEST_URL = 'https://example.com/models.json'; // Replace with actual curated manifest URL

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
    <div className="model-downloader p-4 border rounded-lg bg-slate-900 text-white">
      <h2 className="text-xl font-bold mb-4">Model Downloader</h2>

      {loading && <p>Loading manifest...</p>}

      {status && (
        <div className="mb-4 p-2 bg-blue-600 rounded text-sm">
          {status}
        </div>
      )}

      {!loading && manifest && (
        <div className="space-y-2">
          {manifest.models.map((model) => (
            <div key={model.name} className="flex items-center justify-between p-2 bg-slate-800 rounded">
              <div>
                <span className="font-medium">{model.name}</span>
                <span className="text-xs text-slate-400 ml-2">({(model.size / 1024 / 1024).toFixed(2)} MB)</span>
              </div>
              <button
                onClick={() => downloadModel(model)}
                disabled={downloading === model.name}
                className="px-3 py-1 bg-blue-500 hover:bg-blue-600 disabled:bg-slate-600 rounded text-sm transition"
              >
                {downloading === model.name ? 'Downloading...' : 'Download'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModelDownloader;
