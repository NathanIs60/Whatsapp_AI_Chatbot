@echo off
echo WhatsApp AI Chatbot - Kurulum
echo ===============================

echo Python sürümünü kontrol ediliyor...
py --version
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadı! Lütfen Python 3.10 veya daha yeni bir sürüm yükleyin.
    pause
    exit /b 1
)

echo.
echo Gerekli kütüphaneler yükleniyor...
echo.

REM Temel kütüphaneleri yükle
py -m pip install openai>=1.0.0
py -m pip install anthropic>=0.8.0
py -m pip install requests>=2.25.0
py -m pip install selenium>=4.0.0
py -m pip install pywhatkit>=5.3
py -m pip install pyinstaller>=5.0.0
py -m pip install webdriver-manager>=3.8.0

echo.
echo Yapılandırma dosyası oluşturuluyor...
echo.

REM Varsayılan yapılandırma dosyası oluştur
echo { > ai_config.json
echo   "openai_api_key": "", >> ai_config.json
echo   "claude_api_key": "", >> ai_config.json
echo   "deepseek_api_key": "", >> ai_config.json
echo   "last_selected_ai": "OpenAI", >> ai_config.json
echo   "settings": { >> ai_config.json
echo     "temperature": 0.7, >> ai_config.json
echo     "max_tokens": 1000, >> ai_config.json
echo     "system_message": "Sen yardımcı bir AI asistanısın. Türkçe sorulara Türkçe cevap ver." >> ai_config.json
echo   } >> ai_config.json
echo } >> ai_config.json

echo.
echo Kurulum tamamlandı!
echo.
echo Kullanım:
echo 1. 'build.bat' dosyasını çalıştırarak EXE dosyalarını oluşturun
echo 2. 'ai_manager.py' dosyasını doğrudan çalıştırabilirsiniz: python ai_manager.py
echo 3. API anahtarlarınızı GUI üzerinden girin
echo.

pause

