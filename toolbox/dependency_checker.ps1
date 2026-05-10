$deps = @("node", "npm", "python", "git", "ollama")
foreach ($dep in $deps) {
    if (Get-Command $dep -ErrorAction SilentlyContinue) {
        Write-Host "✓ $dep: Found"
    } else {
        Write-Host "✗ $dep: Missing"
    }
}