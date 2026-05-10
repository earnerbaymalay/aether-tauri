param(
    [string]$pattern,
    [string]$path = "."
)

$files = Get-ChildItem -Path $path -Filter $pattern -Recurse -File -ErrorAction SilentlyContinue
if ($files) {
    foreach ($f in $files) {
        Write-Host $f.FullName
    }
} else {
    Write-Host "No files found matching pattern."
}
