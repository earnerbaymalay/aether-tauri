$configPath = "C:\Users\earnerbaymalay\aether\settings\config.json"
if (-not (Test-Path $configPath)) {
    $defaultConfig = @{
        appearance = @{ accent_color = "#00ff9d" }
        model = @{ threads = 6; context_size = 2048; temperature = 0.7 }
        profile = "balanced"
    }
    $defaultConfig | ConvertTo-Json | Out-File $configPath
}
Get-Content $configPath