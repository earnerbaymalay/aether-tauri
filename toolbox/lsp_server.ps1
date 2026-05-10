$action = $args[0] ?? "status"

function Get-Language($path) {
    $ext = [System.IO.Path]::GetExtension($path).ToLower()
    switch ($ext) {
        ".py" { return "python" }
        ".js" { return "javascript" }
        ".ts" { return "typescript" }
        ".ps1" { return "powershell" }
        default { return "unknown" }
    }
}

case "status" {
    Write-Host "=== LSP Server Status (Windows) ==="
    Write-Host "Capabilities: Diagnostics, Symbols, Hover"
    Write-Host "Supported: Python, JS, TS, PowerShell"
}
case "diagnostics" {
    $file = $args[1]
    $lang = Get-Language $file
    Write-Host "=== Diagnostics for $file ($lang) ==="
    if ($lang -eq "python" -and (Get-Command python -ErrorAction SilentlyContinue)) {
        python -m py_compile $file
    } elseif ($lang -eq "powershell") {
        # Basic PS syntax check
        [ast]::ParseFile($file, [ref]$null, [ref]$null)
    }
}
