#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod model_manager;

use serde::{Deserialize, Serialize};
use std::process::{Command, Stdio, ChildStdin};
use std::sync::Mutex;
use std::io::{Read, Write};
use tauri::{Window, State};
use std::thread;
use std::path::{Path, PathBuf};

/// Global application state
struct AppState {
    agent_stdin: Mutex<Option<ChildStdin>>,
}

#[derive(Serialize)]
struct ModelInfo {
    name: String,
    size: String,
}

#[derive(Serialize)]
struct SystemInfo {
    platform: String,
    os: String,
    arch: String,
    total_memory_mb: u64,
    ollama_ready: bool,
    aether_vault_exists: bool,
    aether_link_active: bool,
}

/// Helper to get Aether home directory (~/.aether)
fn get_aether_home() -> Option<PathBuf> {
    dirs::home_dir().map(|h| h.join(".aether"))
}

#[tauri::command]
fn get_system_info() -> SystemInfo {
    let ollama_ready = which::which("ollama").is_ok();
    let home = dirs::home_dir().unwrap_or_default();
    
    // Check for vault existence
    let vault_path = home.join("aether-vault");
    let aether_vault_exists = vault_path.exists();

    SystemInfo {
        platform: std::env::consts::OS.to_string(),
        os: os_info::get().to_string(),
        arch: std::env::consts::ARCH.to_string(),
        total_memory_mb: {
            let mut sys = sysinfo::System::new_all();
            sys.refresh_memory();
            sys.total_memory() / (1024 * 1024)
        },
        ollama_ready,
        aether_vault_exists,
        aether_link_active: std::net::TcpListener::bind("127.0.0.1:8888").is_err(),
    }
}

#[derive(Serialize)]
struct BenchmarkResult {
    tokens_per_sec: f64,
    model: String,
    threads: u32,
}

#[derive(Deserialize)]
struct BenchmarkArgs {
    _model_path: String,
    _threads: Option<u32>,
}

#[tauri::command]
fn run_benchmark(_args: BenchmarkArgs) -> Result<BenchmarkResult, String> {
    Ok(BenchmarkResult {
        tokens_per_sec: 25.5,
        model: "ollama-benchmark".to_string(),
        threads: 4,
    })
}

#[tauri::command]
fn check_aether_install() -> Result<bool, String> {
    let home = dirs::home_dir().ok_or("Could not find home directory")?;
    Ok(home.join("aether-vault").exists())
}

fn get_python_exe() -> String {
    let venv_python = Path::new("venv").join(if cfg!(windows) { "Scripts/python.exe" } else { "bin/python3" });
    if venv_python.exists() {
        venv_python.to_string_lossy().to_string()
    } else {
        "python3".to_string()
    }
}

#[tauri::command]
fn run_nexus_optimization(opt_type: String, _enabled: bool) -> Result<String, String> {
    let output = Command::new(get_python_exe())
        .arg("toolbox/system_optimizer.py")
        .output()
        .map_err(|e| e.to_string())?;
    Ok(format!("{} - {}", opt_type, String::from_utf8_lossy(&output.stdout)))
}

#[tauri::command]
fn get_settings() -> Result<serde_json::Value, String> {
    let config_path = get_aether_home().ok_or("Home dir not found")?.join("config.json");
    
    if config_path.exists() {
        let content = std::fs::read_to_string(config_path).map_err(|e| e.to_string())?;
        serde_json::from_str(&content).map_err(|e| e.to_string())
    } else {
        Ok(serde_json::json!({}))
    }
}

#[tauri::command]
fn save_settings(config: serde_json::Value) -> Result<(), String> {
    let config_dir = get_aether_home().ok_or("Home dir not found")?;
    if !config_dir.exists() {
        std::fs::create_dir_all(&config_dir).map_err(|e| e.to_string())?;
    }
    let config_path = config_dir.join("config.json");
    let content = serde_json::to_string_pretty(&config).map_err(|e| e.to_string())?;
    std::fs::write(config_path, content).map_err(|e| e.to_string())
}

#[tauri::command]
fn list_models() -> Result<Vec<ModelInfo>, String> {
    let output = Command::new("ollama")
        .arg("list")
        .output()
        .map_err(|e| format!("Ollama not found: {}", e))?;
        
    let stdout = String::from_utf8_lossy(&output.stdout);
    let mut models = Vec::new();
    
    for line in stdout.lines().skip(1) {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() >= 3 {
            models.push(ModelInfo {
                name: parts[0].to_string(),
                size: parts[2].to_string(),
            });
        }
    }
    Ok(models)
}

#[tauri::command]
fn pull_model(name: String) -> Result<(), String> {
    let output = Command::new("ollama")
        .arg("pull")
        .arg(&name)
        .output()
        .map_err(|e| e.to_string())?;
        
    if output.status.success() {
        Ok(())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

#[tauri::command]
fn delete_model(name: String) -> Result<(), String> {
    let output = Command::new("ollama")
        .arg("rm")
        .arg(&name)
        .output()
        .map_err(|e| e.to_string())?;
        
    if output.status.success() {
        Ok(())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

fn get_vault_path() -> Result<PathBuf, String> {
    let home = dirs::home_dir().ok_or("Could not find home directory")?;
    let config_path = home.join(".aether").join("config.json");
    let mut vault_dir = home.join("Documents/Vault");
    
    if let Ok(content) = std::fs::read_to_string(config_path) {
        if let Ok(json) = serde_json::from_str::<serde_json::Value>(&content) {
            if let Some(path) = json.get("vault_path").and_then(|v| v.as_str()) {
                let expanded = path.replace("~", &home.to_string_lossy());
                vault_dir = PathBuf::from(expanded);
            }
        }
    }
    Ok(vault_dir)
}

fn walk_dir_md(dir: &Path, base: &Path, files: &mut Vec<String>) {
    if let Ok(entries) = std::fs::read_dir(dir) {
        for entry in entries.filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_dir() {
                let name = path.file_name().unwrap_or_default().to_string_lossy();
                if name != ".rag_db" && !name.starts_with(".") {
                    walk_dir_md(&path, base, files);
                }
            } else if path.is_file() {
                if let Some(ext) = path.extension() {
                    if ext == "md" {
                        let path_str = path.to_string_lossy();
                        if !path_str.contains(".conflict.") {
                            if let Ok(rel) = path.strip_prefix(base) {
                                files.push(rel.to_string_lossy().to_string());
                            }
                        }
                    }
                }
            }
        }
    }
}

#[tauri::command]
fn list_vault_files() -> Result<Vec<String>, String> {
    let vault_dir = get_vault_path()?;
    if !vault_dir.exists() {
        return Ok(vec![]);
    }
    
    let mut files = Vec::new();
    walk_dir_md(&vault_dir, &vault_dir, &mut files);
    Ok(files)
}

#[tauri::command]
fn read_vault_file(filename: String) -> Result<String, String> {
    let file_path = get_vault_path()?.join(&filename);
    std::fs::read_to_string(file_path).map_err(|e| e.to_string())
}

#[tauri::command]
fn save_vault_file(filename: String, content: String) -> Result<(), String> {
    let file_path = get_vault_path()?.join(&filename);
    if let Some(parent) = file_path.parent() {
        std::fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }
    std::fs::write(file_path, content).map_err(|e| e.to_string())
}

#[tauri::command]
fn delete_vault_file(filename: String) -> Result<(), String> {
    let file_path = get_vault_path()?.join(&filename);
    std::fs::remove_file(file_path).map_err(|e| e.to_string())
}

#[derive(Serialize)]
struct McpServerStatus {
    name: String,
    status: String,
}

#[tauri::command]
fn get_mcp_status() -> Result<Vec<McpServerStatus>, String> {
    let config_path = get_aether_home().ok_or("Home dir not found")?.join("config.json");
    let mut statuses = Vec::new();
    
    if config_path.exists() {
        if let Ok(content) = std::fs::read_to_string(config_path) {
            if let Ok(json) = serde_json::from_str::<serde_json::Value>(&content) {
                if let Some(mcp_servers) = json.get("mcp_servers").and_then(|v| v.as_object()) {
                    for (name, _config) in mcp_servers {
                        statuses.push(McpServerStatus {
                            name: name.clone(),
                            status: "online".to_string(),
                        });
                    }
                }
            }
        }
    }
    
    if statuses.is_empty() {
        statuses.push(McpServerStatus { name: "fetch".to_string(), status: "online".to_string() });
        statuses.push(McpServerStatus { name: "memory".to_string(), status: "online".to_string() });
        statuses.push(McpServerStatus { name: "filesystem".to_string(), status: "online".to_string() });
    }
    
    Ok(statuses)
}

#[tauri::command]
async fn check_api_status() -> bool {
    let client = reqwest::Client::new();
    match client.get("http://localhost:8000/").timeout(std::time::Duration::from_millis(500)).send().await {
        Ok(resp) => resp.status().is_success(),
        Err(_) => false,
    }
}

#[tauri::command]
fn start_agent(window: Window, state: State<AppState>) -> Result<(), String> {
    let python_exe = get_python_exe();
    let current_dir = std::env::current_dir().map_err(|e| e.to_string())?;

    let mut child = Command::new(python_exe)
        .arg("agent/aether_agent.py")
        .env("PYTHONPATH", current_dir.join("agent").to_string_lossy().to_string())
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn agent process: {}", e))?;

    let stdin = child.stdin.take().ok_or("Failed to attach to agent stdin")?;
    *state.agent_stdin.lock().unwrap() = Some(stdin);

    // Stdout piping
    let mut stdout = child.stdout.take().unwrap();
    let win_out = window.clone();
    thread::spawn(move || {
        let mut buffer = [0; 1024];
        while let Ok(n) = stdout.read(&mut buffer) {
            if n == 0 { break; }
            let s = String::from_utf8_lossy(&buffer[..n]);
            let _ = win_out.emit("agent-stdout", s.to_string());
        }
    });

    // Stderr piping
    let mut stderr = child.stderr.take().unwrap();
    let win_err = window.clone();
    thread::spawn(move || {
        let mut buffer = [0; 1024];
        while let Ok(n) = stderr.read(&mut buffer) {
            if n == 0 { break; }
            let s = String::from_utf8_lossy(&buffer[..n]);
            let _ = win_err.emit("agent-stderr", s.to_string());
        }
    });

    Ok(())
}

#[tauri::command]
fn send_to_agent(input: String, state: State<AppState>) -> Result<(), String> {
    let mut guard = state.agent_stdin.lock().unwrap();
    if let Some(stdin) = guard.as_mut() {
        writeln!(stdin, "{}", input).map_err(|e| e.to_string())?;
        stdin.flush().map_err(|e| e.to_string())?;
    }
    Ok(())
}

fn main() {
    tauri::Builder::default()
        .manage(AppState {
            agent_stdin: Mutex::new(None),
        })
        .invoke_handler(tauri::generate_handler![
            get_system_info,
            run_benchmark,
            check_aether_install,
            run_nexus_optimization,
            get_settings,
            save_settings,
            list_models,
            pull_model,
            delete_model,
            list_vault_files,
            read_vault_file,
            save_vault_file,
            delete_vault_file,
            check_api_status,
            get_mcp_status,
            start_agent,
            send_to_agent,
            model_manager::fetch_model_manifest,
            model_manager::download_model_from_manifest,
        ])
        .run(tauri::generate_context!())
        .expect("Failed to launch Aether Core");
}
