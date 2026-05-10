$noteName = $args[0]
$vaultPath = "C:\Users\earnerbaymalay\Documents\vault\vault"
$note = Get-ChildItem -Path $vaultPath -Filter "$noteName" -Recurse | Select-Object -First 1
if ($note) {
    Get-Content $note.FullName
} else {
    Write-Error "Note not found."
}