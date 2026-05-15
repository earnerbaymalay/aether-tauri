use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{Read, Write};
use std::path::{Path, PathBuf};
use reqwest::blocking::get;
use sha2::{Sha256, Digest};
use tauri::Window;

#[derive(Deserialize, Serialize, Clone)]
pub struct ModelManifestEntry {
    pub name: String,
    pub url: String,
    pub hash: String,
    pub size: u64,
}

#[derive(Deserialize, Serialize)]
pub struct ModelManifest {
    pub models: Vec<ModelManifestEntry>,
}

pub fn download_model(window: Window, entry: ModelManifestEntry) -> Result<(), String> {
    let home = dirs::home_dir().ok_or("Could not find home directory")?;
    let download_dir = home.join(".aether").join("models");
    std::fs::create_dir_all(&download_dir).map_err(|e| e.to_string())?;

    let file_path = download_dir.join(&entry.name);

    // 1. Fetch from URL
    let mut response = get(&entry.url).map_err(|e| format!("Download request failed: {}", e))?;

    let mut file = File::create(&file_path).map_err(|e| format!("Failed to create file: {}", e))?;
    let mut buffer = Vec::new();
    response.read_to_end(&mut buffer).map_err(|e| format!("Failed to read response: {}", e))?;
    file.write_all(&buffer).map_err(|e| format!("Failed to write file: {}", e))?;

    // 2. Verify Hash
    let mut hasher = Sha256::new();
    hasher.update(&buffer);
    let result = hasher.finalize();
    let actual_hash = format!("{:x}", result);

    if actual_hash != entry.hash {
        std::fs::remove_file(&file_path).ok();
        return Err(format!("Hash mismatch! Expected {}, got {}", entry.hash, actual_hash));
    }

    Ok(())
}

#[tauri::command]
pub fn fetch_model_manifest(url: String) -> Result<ModelManifest, String> {
    let response = get(url).map_err(|e| e.to_string())?;
    let manifest: ModelManifest = response.json().map_err(|e| e.to_string())?;
    Ok(manifest)
}

#[tauri::command]
pub fn download_model_from_manifest(window: Window, entry: ModelManifestEntry) -> Result<(), String> {
    download_model(window, entry)
}
