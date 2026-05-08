@echo off
title kairus - Build Executable Builder
color 0A

echo ================================================
echo    kairus - Executable Builder
echo ================================================
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [OK] Python found!
echo.

REM Check if PyInstaller is installed
echo [2/6] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [WARNING] PyInstaller not found! Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller!
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller is installed!
echo.

REM Check if icon.png exists
echo [3/6] Checking icon.png...
if not exist "icon.png" (
    echo [WARNING] icon.png not found! Creating placeholder...
    echo Creating empty icon file...
    echo This is a placeholder icon > icon.png
)
echo [OK] icon.png found!
echo.

REM Clean previous builds
echo [4/6] Cleaning previous builds...
if exist "build" (
    echo Deleting build folder...
    rmdir /s /q build
)
if exist "dist" (
    echo Deleting dist folder...
    rmdir /s /q dist
)
if exist "*.spec" (
    echo Deleting spec files...
    del /q *.spec
)
echo [OK] Cleanup complete!
echo.

REM Build the executable
echo [5/6] Building kairus executable...
echo This may take a few minutes. Please wait...
echo.

pyinstaller --name=kairus --onefile --windowed --icon=icon.png --add-data "icon.png;." --add-data "ui;ui" --add-data "core;core" --add-data "security;security" --add-data "storage;storage" --add-data "utils;utils" --hidden-import PySide6 --hidden-import cryptography --hidden-import bcrypt --hidden-import reportlab --hidden-import sqlite3 --collect-all PySide6 --collect-all cryptography --collect-all reportlab --clean --noconfirm main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo.
echo [OK] Build completed successfully!
echo.

REM Check if executable was created
echo [6/6] Verifying executable...
if exist "dist\kairus.exe" (
    echo [OK] kairus.exe created successfully!
    echo.
    echo ================================================
    echo    BUILD SUCCESSFUL!
    echo ================================================
    echo.
    echo Executable location: %CD%\dist\kairus.exe
    echo File size: 
    dir "dist\kairus.exe" | find "kairus.exe"
    echo.
    echo Do you want to run the executable now?
    choice /c SN /n /m "Run now? (S/N): "
    if errorlevel 2 goto :end
    if errorlevel 1 start "" "dist\kairus.exe"
) else (
    echo [ERROR] Executable not found! Build may have failed.
)

:end
echo.
echo Press any key to exit...
pause >nul
exit /b 0