# used to test the mpremote edit command
$txt = Get-Content $args[0] 
$txt | ForEach-Object { $_ -replace "Hello", "Goodbye" } | Set-Content $args[0]
