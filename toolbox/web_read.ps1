$url = $args[0]
if (-not $url) { Write-Error "No URL provided."; exit 1 }
$response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0"
$response.Content -replace "<[^>]+>", "" -replace "\s+", " "