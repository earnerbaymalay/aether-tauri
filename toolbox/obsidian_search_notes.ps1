$query = $args[0]
$vaultPath = "C:\Users\earnerbaymalay\Documents\vault\vault"
Select-String -Path "$vaultPath\*.md" -Pattern $query -Context 0,1 | Select-Object FileName, Line, LineNumber