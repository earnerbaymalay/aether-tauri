$query = $args[0]
if (-not $query) {
    Write-Error "No search query provided."
    exit 1
}

$encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)
$url = "https://duckduckgo.com/html/?q=$encodedQuery"
$response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0"
$response.Content | Select-String -Pattern "<a class=`"result__a`".*?>(.*?)</a>" -AllMatches | ForEach-Object { $_.Matches } | Select-Object -First 5 | ForEach-Object { $_.Groups[1].Value }
