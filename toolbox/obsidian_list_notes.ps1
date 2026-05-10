$vaultPath = "C:\Users\earnerbaymalay\Documents\vault\vault"
Get-ChildItem -Path $vaultPath -Filter "*.md" -Recurse | Select-Object Name, FullName