# PowerShell setup script for OSINT Pipeline
# Usage (PowerShell):
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   .\setup_windows.ps1

$env:VENV_DIR = "osint_env"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found in PATH. Please install Python 3.10+ and try again." -ForegroundColor Red
    exit 1
}

# Create virtual environment
python -m venv $env:VENV_DIR

# Activate environment for this script
$activate = Join-Path $env:VENV_DIR 'Scripts\Activate.ps1'
if (Test-Path $activate) {
    Write-Host "Activating virtual environment..."
    & $activate
} else {
    Write-Host "Could not find Activate.ps1 in $env:VENV_DIR\Scripts" -ForegroundColor Yellow
}

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# NLTK downloads (optional)
python - <<"PY"
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
PY

Write-Host "Setup complete. To activate the venv in PowerShell: .\$env:VENV_DIR\Scripts\Activate.ps1" -ForegroundColor Green
Write-Host "Run 'python main.py' to collect data and 'python app.py' to start the web server." -ForegroundColor Green
