param(
    [string]$file_path,
    [string]$old_string,
    [string]$new_string
)

if (-not (Test-Path $file_path)) {
    Write-Error "File not found: $file_path"
    exit 1
}

$content = Get-Content -Path $file_path -Raw
if ($content -like "*$old_string*") {
    $new_content = $content.Replace($old_string, $new_string)
    Set-Content -Path $file_path -Value $new_content -NoNewline
    Write-Host "Successfully edited $file_path"
} else {
    Write-Error "Could not find exact match for replacement in $file_path"
    exit 1
}
