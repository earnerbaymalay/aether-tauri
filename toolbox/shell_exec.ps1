if ($args.Count -eq 0) { throw "Command required" }
Invoke-Expression -Command $args[0]