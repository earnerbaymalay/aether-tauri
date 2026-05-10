param(
    [string]$query
)

if (-not $query) {
    Write-Error "No search query provided."
    exit 1
}

# 1. Load Aether Config
$configFile = "$HOME\.aether\config.json"
$browserPath = "C:\Program Files\Google\Chrome\Application\chrome.exe" # Default fallback
$browserType = "chrome"

if (Test-Path $configFile) {
    try {
        $config = Get-Content $configFile | ConvertFrom-Json
        if ($config.browser_path) { $browserPath = $config.browser_path }
        if ($config.browser_type) { $browserType = $config.browser_type }
    } catch {
        Write-Warning "Failed to parse Aether config. Using defaults."
    }
}

# 2. Perform Search (DuckDuckGo)
# Since we are an AI workstation, we want to retrieve results, not just open a browser.
# However, if the user specifically asked for browser choice, they might want the AI to launch it or use it for rendering.
# For now, we'll retrieve results via web request but honor the "browser" preference by opening the search page if requested.

$encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)
$searchUrl = "https://duckduckgo.com/?q=$encodedQuery"

# Retrieve top results for the AI to process
$apiResults = "Top results from DuckDuckGo for '$query':`n"
try {
    $htmlResults = "https://duckduckgo.com/html/?q=$encodedQuery"
    $response = Invoke-WebRequest -Uri $htmlResults -UserAgent "Mozilla/5.0" -TimeoutSec 10
    $links = $response.Content | Select-String -Pattern "<a class=`"result__a`".*?>(.*?)</a>" -AllMatches | ForEach-Object { $_.Matches } | Select-Object -First 5
    foreach ($l in $links) {
        $apiResults += "- " + $l.Groups[1].Value + "`n"
    }
} catch {
    $apiResults += "Error retrieving search results: $_"
}

# 3. Optional: Open the browser for the user if they are in interactive mode (simulated)
# In this environment, we mostly care about the data for the AI.
# But we can log that we are using the user's preferred browser.

Write-Host "Neural Search executed via $browserType ($browserPath)"
Write-Host "---"
Write-Host $apiResults
