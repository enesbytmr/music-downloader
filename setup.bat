@echo off
echo.
echo ==========================================
echo   🎵 Music Downloader Web App Kurulum
echo ==========================================
echo.

:: Admin kontrolü
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Yönetici yetkileri mevcut
) else (
    echo ⚠️  Bu scripti "Yönetici olarak çalıştır" ile açın!
    pause
    exit /b 1
)

:: Python varlığını kontrol et
echo 🐍 Python kontrolü...
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Python zaten yüklü
    goto :install_deps
)

echo 📦 Python yüklenecek...
echo Python'u resmi sitesinden indirip yükleyin: https://python.org
echo Yükleme tamamlandıktan sonra bu scripti tekrar çalıştırın.
start https://python.org/downloads/
pause
exit /b 1

:install_deps
echo.
echo 📦 Gerekli kütüphaneler yükleniyor...
pip install flask requests yt-dlp spotdl

if %errorLevel% neq 0 (
    echo ❌ Kütüphane yükleme hatası! İnternet bağlantınızı kontrol edin.
    pause
    exit /b 1
)

:: İndirme klasörünü oluştur
echo 📁 İndirme klasörü hazırlanıyor...
if not exist "%USERPROFILE%\Desktop\Music" (
    mkdir "%USERPROFILE%\Desktop\Music"
)

echo.
echo ✅ Kurulum tamamlandı!
echo.
echo 🚀 Web uygulaması başlatılıyor...
echo 🌐 Tarayıcınızda otomatik olarak açılacak: http://localhost:5001
echo ⚡ Durdurmak için bu pencereyi kapatın
echo.

:: Web uygulamasını başlat
cd music_downloader_app
start http://localhost:5001
python app.py

pause
