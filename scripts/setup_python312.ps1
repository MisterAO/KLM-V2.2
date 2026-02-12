# Python 3.12 Setup Automation Script for KLM V2
# Run this in PowerShell as Administrator

Write-Host "=========================================" -ForegroundColor Green
Write-Host "KLM V2 Python 3.12 Setup Automation" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some operations may fail." -ForegroundColor Yellow
    Write-Host "Consider running PowerShell as Administrator for best results." -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Check current Python version
Write-Host "Step 1: Checking current Python version..." -ForegroundColor Cyan
$currentPython = python --version 2>&1
Write-Host "Current: $currentPython" -ForegroundColor Yellow
Write-Host ""

# Step 2: Check if Python 3.12 is installed
Write-Host "Step 2: Checking for Python 3.12..." -ForegroundColor Cyan
$py312 = py -3.12 --version 2>&1
if ($py312 -match "3.12") {
    Write-Host "✓ Python 3.12 found: $py312" -ForegroundColor Green
} else {
    Write-Host "✗ Python 3.12 not found. Please download and install from:" -ForegroundColor Red
    Write-Host "  https://www.python.org/downloads/release/python-3129/" -ForegroundColor Yellow
    Write-Host "  Download: Windows installer (64-bit)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "IMPORTANT: Check 'Add python.exe to PATH' during installation!" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter after installing Python 3.12"
    
    # Check again
    $py312 = py -3.12 --version 2>&1
    if ($py312 -match "3.12") {
        Write-Host "✓ Python 3.12 now found: $py312" -ForegroundColor Green
    } else {
        Write-Host "✗ Python 3.12 still not found. Exiting." -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 3: Navigate to project directory
Write-Host "Step 3: Setting up project directory..." -ForegroundColor Cyan
$projectPath = "C:\Users\ounga\Documents\GitHub\KLM V2"
if (-not (Test-Path $projectPath)) {
    Write-Host "✗ Project directory not found: $projectPath" -ForegroundColor Red
    exit 1
}
Set-Location $projectPath
Write-Host "✓ Changed to: $projectPath" -ForegroundColor Green
Write-Host ""

# Step 4: Create virtual environment
Write-Host "Step 4: Creating virtual environment with Python 3.12..." -ForegroundColor Cyan
$venvPath = "venv312"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists. Removing old one..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venvPath
}

py -3.12 -m venv $venvPath
if ($?) {
    Write-Host "✓ Virtual environment created: $venvPath" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 5: Activate virtual environment
Write-Host "Step 5: Activating virtual environment..." -ForegroundColor Cyan
$activateScript = ".\venv312\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Activation script not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 6: Verify Python version in venv
Write-Host "Step 6: Verifying Python version..." -ForegroundColor Cyan
$venvPython = python --version
Write-Host "Virtual env Python: $venvPython" -ForegroundColor Green
Write-Host ""

# Step 7: Upgrade pip
Write-Host "Step 7: Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip
Write-Host "✓ Pip upgraded" -ForegroundColor Green
Write-Host ""

# Step 8: Install core dependencies
Write-Host "Step 8: Installing core dependencies..." -ForegroundColor Cyan

# Install discord bot dependencies
pip install discord.py python-dotenv aiohttp

# Install ChromaDB (this should work with Python 3.12)
pip install chromadb

# Install other common deps
pip install pydantic fastapi uvicorn sqlalchemy

Write-Host "✓ Core dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 9: Test imports
Write-Host "Step 9: Testing imports..." -ForegroundColor Cyan
$testCode = @"
try:
    import chromadb
    print('✓ ChromaDB imported successfully')
except Exception as e:
    print(f'✗ ChromaDB import failed: {e}')

try:
    import discord
    print('✓ Discord.py imported successfully')
except Exception as e:
    print(f'✗ Discord import failed: {e}')

try:
    from pydantic import BaseModel
    print('✓ Pydantic imported successfully')
except Exception as e:
    print(f'✗ Pydantic import failed: {e}')
"@

python -c $testCode
Write-Host ""

# Step 10: Summary
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate this environment in the future:" -ForegroundColor Cyan
Write-Host "  cd 'C:\Users\ounga\Documents\GitHub\KLM V2'" -ForegroundColor Yellow
Write-Host "  .\venv312\Scripts\activate" -ForegroundColor Yellow
Write-Host ""
Write-Host "To run the Discord bot:" -ForegroundColor Cyan
Write-Host "  cd 30-Implementation\discord_bot" -ForegroundColor Yellow
Write-Host "  python ai_bot.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green

# Keep window open
Read-Host "Press Enter to exit"
