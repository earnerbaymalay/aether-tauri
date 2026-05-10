param(
    [string]$target = "google.com"
)

Write-Host "🌌 Aether Security: Network Recon on $target..." -ForegroundColor Cyan

Write-Host "`n[1] DNS Lookup:" -ForegroundColor Magenta
Resolve-DnsName $target | Select-Object Name, Type, IPAddress, NameHost | Format-Table

Write-Host "`n[2] WHOIS (via Web):" -ForegroundColor Magenta
# Using a lightweight web-based whois for portability
$whoisUrl = "https://who.is/whois/$target"
Write-Host "View detailed WHOIS: $whoisUrl" -ForegroundColor Gray

Write-Host "`n[3] TraceRoute:" -ForegroundColor Magenta
Test-NetConnection -ComputerName $target -TraceRoute | Select-Object ComputerName, RemoteAddress, TraceRoute
