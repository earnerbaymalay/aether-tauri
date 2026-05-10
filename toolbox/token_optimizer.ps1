function Get-TokenEstimate($text) {
    if (-not $text) { return 0 }
    return [math]::Round($text.Length / 4)
}

function Compress-Context($path) {
    if (-not (Test-Path $path)) { Write-Error "File not found."; return }
    $content = Get-Content $path
    $cleaned = $content | Where-Object { $_ -notmatch '^\s*$' -and $_ -notmatch '^\s*#' -and $_ -notmatch '^\s*//' }
    $cleaned = $cleaned -replace '\s+', ' '
    return $cleaned
}

$action = $args[0] ?? "stats"
case "stats" {
    Write-Host "=== Token Optimization Statistics ==="
    $sessionLog = "$HOME\.aether\sessions\last_session.log"
    if (Test-Path $sessionLog) {
        $tokens = Get-TokenEstimate (Get-Content $sessionLog -Raw)
        Write-Host "  Session Log: $tokens tokens"
    } else {
        Write-Host "  Session Log: 0 tokens"
    }
}
case "compress" {
    Compress-Context $args[1]
}
