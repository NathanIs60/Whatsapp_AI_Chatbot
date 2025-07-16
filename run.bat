@echo off
title AI Manager - WhatsApp AI ChatBot
echo.
echo =========================================
echo    AI Manager - WhatsApp AI ChatBot
echo =========================================
echo.

REM Mevcut EXE dosyasını kontrol et
if exist "dist\AI_Manager.exe" (
    echo EXE dosyası bulundu, çalıştırılıyor...
    echo.
    start "AI Manager" "dist\AI_Manager.exe"
    echo AI Manager başlatıldı!
) else (
    echo EXE dosyası bulunamadı, Python scripti çalıştırılıyor...
    echo.
    
    REM Python kurulu mu kontrol et
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo HATA: Python bulunamadı!
        echo Lütfen önce Python yükleyin veya build.bat ile EXE dosyası oluşturun.
        pause
        exit /b 1
    )
    
    REM Gerekli kütüphaneleri kontrol et
    echo Gerekli kütüphaneler kontrol ediliyor...
    py -c "import tkinter, openai, requests" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Gerekli kütüphaneler eksik! Yüklenecek...
        py -m pip install openai anthropic requests
    )
    
    echo Python scripti başlatılıyor...
    py ai_manager.py
)

echo.
echo Program kapatıldı.
pause

