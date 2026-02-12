@echo off
ECHO =========================================
ECHO KLM V2 Python 3.12 Setup (CMD Version)
ECHO =========================================
ECHO.

:: Check if Python 3.12 is available
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    ECHO [ERROR] Python 3.12 not found!
    ECHO.
    ECHO Please download and install Python 3.12 from:
    ECHO   https://www.python.org/downloads/release/python-3129/
    ECHO.
    ECHO IMPORTANT: Check "Add python.exe to PATH" during installation!
    ECHO.
    PAUSE
    EXIT /B 1
)

ECHO [OK] Python 3.12 found
py -3.12 --version
ECHO.

:: Navigate to project
cd /d "C:\Users\ounga\Documents\GitHub\KLM V2"
if errorlevel 1 (
    ECHO [ERROR] Could not find project directory
    PAUSE
    EXIT /B 1
)

ECHO [OK] In project directory
ECHO.

:: Remove old venv if exists
if exist venv312 (
    ECHO Removing old virtual environment...
    rmdir /s /q venv312
)

:: Create virtual environment
ECHO Creating virtual environment with Python 3.12...
py -3.12 -m venv venv312
if errorlevel 1 (
    ECHO [ERROR] Failed to create virtual environment
    PAUSE
    EXIT /B 1
)

ECHO [OK] Virtual environment created
ECHO.

:: Activate and install
call venv312\Scripts\activate.bat
ECHO [OK] Virtual environment activated
ECHO.

ECHO Installing dependencies...
python -m pip install --upgrade pip
pip install discord.py python-dotenv aiohttp
pip install chromadb
pip install pydantic fastapi uvicorn sqlalchemy

ECHO.
ECHO [OK] Dependencies installed
ECHO.

:: Test imports
ECHO Testing imports...
python -c "import chromadb; print('[OK] ChromaDB imported')"
python -c "import discord; print('[OK] Discord imported')"
python -c "from pydantic import BaseModel; print('[OK] Pydantic imported')"

ECHO.
ECHO =========================================
ECHO Setup Complete!
ECHO =========================================
ECHO.
ECHO To activate in the future:
ECHO   C:\Users\ounga\Documents\GitHub\KLM V2\venv312\Scripts\activate.bat
ECHO.
ECHO To run the bot:
ECHO   cd 30-Implementation\discord_bot
ECHO   python ai_bot.py
ECHO.

PAUSE
