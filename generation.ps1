# Function to run a script and check its exit status
function Run-Script {
    param (
        [string]$scriptPath
    )
    
    Write-Host "Running $scriptPath..."
    python $scriptPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $scriptPath completed successfully"
    } else {
        Write-Host "❌ $scriptPath failed with error code $LASTEXITCODE"
        exit 1
    }
    Write-Host "----------------------------------------"
}

# Make sure we're in the project root directory
Set-Location $PSScriptRoot

# Activate virtual environment if it exists
if (Test-Path ".venv") {
    Write-Host "Activating virtual environment..."
    & .\.venv\Scripts\Activate.ps1
}

# Run scripts in sequence
Run-Script "src/tech/hacker_news_scraper.py"
Run-Script "src/tech/hacker_script.py"
Run-Script "src/tech/audio_generation.py"
Run-Script "src/stoic/stoic_news_scraper.py"
Run-Script "src/stoic/stoic_script.py"
Run-Script "src/stoic/audio_generation.py"


# Deactivate virtual environment
if (Test-Path ".venv") {
    deactivate
}

Write-Host "All scripts completed successfully! 🎉" 