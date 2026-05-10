if ($args.Count -eq 0) { throw "Path required" }
Get-Content -Path $args[0] -Raw