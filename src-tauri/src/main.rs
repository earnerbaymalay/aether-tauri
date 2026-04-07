#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};
use std::process::Command;

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
    let llama_cli = which::which("llama-cli").is_ok();
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
    let threads = args.threads.unwrap_or(4);

    let output = Command::new("llama-cli")
        .args([
            "-m", &args.model_path,
            "-c", "128",
            "-t", &threads.to_string(),
            "--mmap",
            "-n", "20",
            "-p", "The future of AI is",
        ])
        .output()
        .map_err(|e| format!("Failed to run llama-cli: {}", e))?;

    let stderr = String::from_utf8_lossy(&output.stderr);
    let tps = parse_tokens_per_second(&stderr);

    Ok(BenchmarkResult {
        tokens_per_sec: tps,
        model: args.model_path,
        threads,
    })
}

fn parse_tokens_per_second(stderr: &str) -> f64 {
    for line in stderr.lines() {
        if line.contains("eval time") && line.contains("ms /") {
            if let Some(ms_str) = line.split_whitespace().rev().nth(2) {
                if let Ok(ms) = ms_str.parse::<f64>() {
                    if ms > 0.0 {
                        return 1000.0 / ms;
                    }
                }
            }
        }
    }
    0.0
}

#[tauri::command]
fn check_aether_install() -> Result<bool, String> {
    let home = dirs::home_dir().ok_or("Could not find home directory")?;
    let aether_dir = home.join("aether");
    let install_script = aether_dir.join("install.sh");
    let main_script = aether_dir.join("aether.sh");

    Ok(aether_dir.exists() && (install_script.exists() || main_script.exists()))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_system_info,
            run_benchmark,
            check_aether_install
        ])
        .run(tauri::generate_context!())
        .expect("error while running Aether Desktop");
}
