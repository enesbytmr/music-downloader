#!/bin/bash

echo "🎵 Music Downloader Web App Başlatılıyor..."
echo "=================================================="

# Dizin kontrolü
if [ ! -d "music_downloader_app" ]; then
    echo "❌ Hata: music_downloader_app klasörü bulunamadı!"
    echo "Bu scripti djenes klasörü içinde çalıştırın."
    exit 1
fi

# Python ve gerekli modülleri kontrol et
echo "🐍 Python kontrolü..."
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 bulunamadı! Lütfen Python 3.11'i yükleyin."
    exit 1
fi

# Flask yüklü mü kontrol et
echo "🌐 Flask kontrolü..."
if ! python3.11 -c "import flask" 2>/dev/null; then
    echo "📦 Flask yükleniyor..."
    pip3.11 install -r music_downloader_app/requirements.txt
fi

# Gerekli scriptlerin varlığını kontrol et
echo "📄 Script kontrolü..."
if [ ! -f "ytbmsc.py" ]; then
    echo "❌ ytbmsc.py bulunamadı!"
    exit 1
fi

if [ ! -f "spotidownloader.py" ]; then
    echo "❌ spotidownloader.py bulunamadı!"
    exit 1
fi

# İndirme klasörünü oluştur
echo "📁 İndirme klasörü hazırlanıyor..."
mkdir -p ~/Desktop/Music

echo "✅ Hazırlık tamamlandı!"
echo ""
echo "🚀 Web uygulaması başlatılıyor..."
echo "🌐 Tarayıcınızda şu adresi açın: http://localhost:5001"
echo "⚡ Durdurmak için Ctrl+C basın"
echo ""

# Web uygulamasını başlat
cd music_downloader_app

# Port 5001'in kullanımda olup olmadığını kontrol et
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5001 zaten kullanımda! Mevcut uygulamayı durdurun."
    echo "🔧 Alternatif: http://localhost:5001 zaten açık olabilir"
    read -p "Devam etmek için Enter basın veya Ctrl+C ile çıkın..."
fi

python3.11 app.py
