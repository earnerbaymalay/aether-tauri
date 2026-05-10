if ($args.Count -lt 2) { throw "Path and content required" }
$path = $args[0]
$content = $args[1]
Set-Content -Path $path -Value $content -Force
"Successfully wrote to $path"