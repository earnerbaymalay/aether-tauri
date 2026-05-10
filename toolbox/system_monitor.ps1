$action = $args[0] ?? "status"

case "status" {
    Write-Host "=== System Status ==="
    Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host ""
    
    # Battery
    $battery = Get-CimInstance -ClassName Win32_Battery
    if ($battery) {
        Write-Host "--- Battery ---"
        Write-Host "  Level: $($battery.EstimatedChargeRemaining)%"
        Write-Host "  Status: $($battery.BatteryStatus)"
    }
    
    # Memory
    $mem = Get-CimInstance -ClassName Win32_OperatingSystem
    $total = [math]::Round($mem.TotalVisibleMemorySize / 1KB)
    $free = [math]::Round($mem.FreePhysicalMemory / 1KB)
    $used = $total - $free
    $pct = [math]::Round(($used / $total) * 100)
    Write-Host "--- Memory ---"
    Write-Host "  Total: $($total) MB, Used: $($used) MB, Free: $($free) MB"
    Write-Host "  Usage: $($pct)%"
    
    # Storage
    $disk = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='C:'"
    $dTotal = [math]::Round($disk.Size / 1GB)
    $dFree = [math]::Round($disk.FreeSpace / 1GB)
    $dUsed = $dTotal - $dFree
    Write-Host "--- Storage ---"
    Write-Host "  Total: $($dTotal) GB, Used: $($dUsed) GB, Available: $($dFree) GB"
    
    # CPU
    $cpu = Get-CimInstance -ClassName Win32_Processor
    Write-Host "--- CPU ---"
    Write-Host "  Cores: $($cpu.NumberOfCores)"
    Write-Host "  Load: $($cpu.LoadPercentage)%"
}
