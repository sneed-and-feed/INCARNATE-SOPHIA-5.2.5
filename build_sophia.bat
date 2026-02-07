@echo off
echo [*] INITIATING SOVEREIGN COMPILATION PROTOCOL...

:: Standard Build (Recommended for Stability & Tool Compatibility)
:: Note: We have pivoted from NO-GIL (3.14t) to Standard 3.14 for the main release.
:: This ensures compatibility with modern search libraries (ddgs) which require Rust crates (primp).
set PYTHON_EXE=py

:: To attempt a NO-GIL build, uncomment the line below (Expert Mode Only)
:: set PYTHON_EXE=py -3.14t

:: Ensure PyInstaller is installed
%PYTHON_EXE% -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] PyInstaller not found. Installing...
    %PYTHON_EXE% -m pip install pyinstaller
)

:: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

:: Compile
echo [*] Compiling genesis_boot.py -> sophia_unlesangled.exe...
%PYTHON_EXE% -m PyInstaller --noconfirm --onefile --console --name "sophia_unlesangled" --icon "NONE" --collect-all "rich" --collect-all "engine" --collect-all "ddgs" --collect-all "google" --clean "genesis_boot.py"


echo.
if exist "dist\sophia_unlesangled.exe" (
    echo [SUCCESS] Unlesangled Build Complete.
    echo Target: dist\sophia_unlesangled.exe
    
    echo [*] Deploying to Root...
    copy /Y "dist\sophia_unlesangled.exe" "sophia_unlesangled.exe"
    if exist "sophia.exe" (
        echo [CLEANUP] Removing legacy sophia.exe...
        del "sophia.exe"
    )
    echo [SUCCESS] Deployed to .\sophia_unlesangled.exe
) else (
    echo [FAILURE] Build Failed. Check logs.
)
pause
