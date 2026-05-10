$source = "C:\Users\earnerbaymalay\aether"
$destination = "C:\Users\earnerbaymalay\aether_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Path $source -Destination $destination -Recurse
Write-Host "Backup created at $destination"