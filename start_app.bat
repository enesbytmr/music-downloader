@echo off
echo 🎵 Music Downloader Web App Başlatılıyor...
echo ==================================================

REM Dizin kontrolü
if not exist "music_downloader_app" (
    echo ❌ Hata: music_downloader_app klasörü bulunamadı!
    echo Bu scripti djenes klasörü içinde çalıştırın.
    pause
    exit /b 1
)

REM Python kontrolü
echo 🐍 Python kontrolü...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin.
    pause
    exit /b 1
)

REM Flask kontrolü
echo 🌐 Flask kontrolü...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 Flask yükleniyor...
    pip install -r music_downloader_app/requirements.txt
)

REM Script kontrolü
echo 📄 Script kontrolü...
if not exist "ytbmsc.py" (
    echo ❌ ytbmsc.py bulunamadı!
    pause
    exit /b 1
)

if not exist "spotidownloader.py" (
    echo ❌ spotidownloader.py bulunamadı!
    pause
    exit /b 1
)

REM İndirme klasörü
echo 📁 İndirme klasörü hazırlanıyor...
if not exist "%USERPROFILE%\Desktop\Music" mkdir "%USERPROFILE%\Desktop\Music"

echo ✅ Hazırlık tamamlandı!
echo.
echo 🚀 Web uygulaması başlatılıyor...
echo 🌐 Tarayıcınızda şu adresi açın: http://localhost:5001
echo ⚡ Durdurmak için Ctrl+C basın
echo.

REM Web uygulamasını başlat
cd music_downloader_app
python app.py

pause
