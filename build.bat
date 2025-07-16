@echo off
echo AI Manager EXE Oluşturucu
echo ==========================

echo Gerekli kütüphaneler yükleniyor...
py -m pip install -r requirements.txt

echo.
echo PyInstaller ile EXE dosyası oluşturuluyor...
echo.

REM AI Manager GUI için EXE oluştur
py -m PyInstaller --onefile --windowed --name "AI_Manager" --distpath "dist" --workpath "build" --add-data "*.json;." --hidden-import=tkinter --hidden-import=openai --hidden-import=anthropic --hidden-import=requests ai_manager.py

echo.
echo Enhanced AI Response modülü için EXE oluştur (isteğe bağlı)
py -m PyInstaller --onefile --name "Enhanced_AI_Response" --distpath "dist" --workpath "build" --add-data "*.json;." --hidden-import=openai --hidden-import=anthropic --hidden-import=requests enhanced_ai_response.py

echo.
echo Geçici dosyalar temizleniyor...
rmdir /s /q build 2>nul
del *.spec 2>nul

echo.
echo ====================================
echo Build işlemi tamamlandı!
echo EXE dosyaları 'dist' klasöründe:
echo - AI_Manager.exe
echo - Enhanced_AI_Response.exe
echo ====================================

echo.
echo Kullanım:
echo 1. AI_Manager.exe dosyasını çalıştırın
echo 2. API anahtarlarınızı girin
echo 3. İstediğiniz AI'ı seçin ve sorgunuzu gönderin
echo.

pause

