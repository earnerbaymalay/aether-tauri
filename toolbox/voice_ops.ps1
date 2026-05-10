param(
    [string]$Action, # "speak" or "transcribe"
    [string]$Text,   # For "speak"
    [string]$File    # For "transcribe"
)

$LOCAL_BIN = "$HOME\.local\bin"
$ENV:PATH = "$LOCAL_BIN;$ENV:PATH"

if ($Action -eq "speak") {
    if (-not $Text) { Write-Output "Error: Text required for speak."; exit 1 }
    # Using sag (ElevenLabs) for TTS
    & sag.exe $Text
}
elseif ($Action -eq "transcribe") {
    if (-not $File -or -not (Test-Path $File)) { Write-Output "Error: Valid file required for transcribe."; exit 1 }
    # Using local whisper.exe for STT
    & whisper.exe $File --model base --output_format txt
}
else {
    Write-Output "Error: Invalid action. Use 'speak' or 'transcribe'."
}
