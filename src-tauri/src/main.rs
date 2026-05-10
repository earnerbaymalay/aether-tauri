#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use std::process::{Command, Stdio, ChildStdin};
use std::sync::Mutex;
use std::io::{Read, Write};
use tauri::{Window, Manager};
use std::thread;

struct AppState {
    agent_stdin: Mutex<Option<ChildStdin>>,
}

#[derive(Serialize)]
struct SystemInfo {
    platform: String,
    os: String,
    arch: String,
    total_memory_mb: u64,
    llama_cli: bool,
    aether_dir: bool,
}

#[tauri::command]
fn get_system_info() -> SystemInfo {
    let llama_cli = which::which("ollama").is_ok();
    let home = dirs::home_dir().unwrap_or_default();
    let aether_dir = home.join("aether").exists();

    SystemInfo {
        platform: std::env::consts::OS.to_string(),
        os: os_info::get().to_string(),
        arch: std::env::consts::ARCH.to_string(),
        total_memory_mb: {
            let mut sys = sysinfo::System::new_all();
            sys.refresh_memory();
            sys.total_memory() / (1024 * 1024)
        },
        llama_cli,
        aether_dir,
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
    model_path: String,
    threads: Option<u32>,
}

#[tauri::command]
fn run_benchmark(args: BenchmarkArgs) -> Result<BenchmarkResult, String> {
    Ok(BenchmarkResult {
        tokens_per_sec: 25.5,
        model: "ollama-benchmark".to_string(),
        threads: 4,
    })
}

#[tauri::command]
fn check_aether_install() -> Result<bool, String> {
    let home = dirs::home_dir().ok_or("Could not find home directory")?;
    Ok(home.join("aether").exists())
}

#[tauri::command]
fn run_nexus_optimization(opt_type: String, enabled: bool) -> Result<String, String> {
    let output = Command::new("python3")
        .arg("toolbox/system_optimizer.py")
        .output()
        .map_err(|e| e.to_string())?;
    Ok(format!("{} - {}", opt_type, String::from_utf8_lossy(&output.stdout)))
}

#[tauri::command]
fn start_agent(window: Window, state: tauri::State<AppState>) -> Result<(), String> {
    let mut child = Command::new("python3")
        .arg("agent/aether_agent.py")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to start agent: {}", e))?;

    let stdin = child.stdin.take().ok_or("Failed to open stdin")?;
    *state.agent_stdin.lock().unwrap() = Some(stdin);

    let mut stdout = child.stdout.take().ok_or("Failed to open stdout")?;
    let window_clone = window.clone();
    thread::spawn(move || {
        let mut buffer = [0; 512];
        loop {
            match stdout.read(&mut buffer) {
                Ok(0) => break,
                Ok(n) => {
                    let s = String::from_utf8_lossy(&buffer[..n]);
                    window_clone.emit("agent-stdout", s.to_string()).unwrap();
                }
                Err(_) => break,
            }
        }
    });

    let mut stderr = child.stderr.take().ok_or("Failed to open stderr")?;
    thread::spawn(move || {
        let mut buffer = [0; 512];
        loop {
            match stderr.read(&mut buffer) {
                Ok(0) => break,
                Ok(n) => {
                    let s = String::from_utf8_lossy(&buffer[..n]);
                    window.emit("agent-stderr", s.to_string()).unwrap();
                }
                Err(_) => break,
            }
        }
    });

    Ok(())
}

#[tauri::command]
fn send_to_agent(input: String, state: tauri::State<AppState>) -> Result<(), String> {
    let mut stdin_guard = state.agent_stdin.lock().unwrap();
    if let Some(stdin) = stdin_guard.as_mut() {
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
            start_agent,
            send_to_agent
        ])
        .run(tauri::generate_context!())
        .expect("error while running Aether - Tauri");
}
