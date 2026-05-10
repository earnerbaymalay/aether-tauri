param(
    [string]$target = "127.0.0.1",
    [int]$start_port = 1,
    [int]$end_port = 1024
)

Write-Host "🌌 Aether Security: Initializing Network Scan on $target..." -ForegroundColor Cyan
Write-Host "Scanning ports $start_port to $end_port..." -ForegroundColor Gray

$openPorts = @()

foreach ($port in $start_port..$end_port) {
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $connection = $tcpClient.BeginConnect($target, $port, $null, $null)
        $wait = $connection.AsyncWaitHandle.WaitOne(100, $false)
        if ($connection.IsCompleted) {
            $tcpClient.EndConnect($connection)
            Write-Host "[!] Port $port is OPEN" -ForegroundColor Green
            $openPorts += $port
        }
        $tcpClient.Close()
    } catch {
        # Port closed or filtered
    }
}

if ($openPorts.Count -eq 0) {
    Write-Host "No open ports discovered in range." -ForegroundColor Yellow
} else {
    Write-Host "`nScan complete. Discovered $($openPorts.Count) open ports." -ForegroundColor Green
}
