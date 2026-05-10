param(
    [string]$pattern,
    [string]$path = ".",
    [string]$include = "*"
)

$results = Select-String -Pattern $pattern -Path "$path\$include" -Recurse -ErrorAction SilentlyContinue
if ($results) {
    foreach ($res in $results) {
        Write-Host "$($res.Path):$($res.LineNumber): $($res.Line.Trim())"
    }
} else {
    Write-Host "No matches found."
}
