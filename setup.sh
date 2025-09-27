#!/bin/bash

# Renkli çıktı fonksiyonları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${PURPLE}"
    echo "=========================================="
    echo "  🎵 Music Downloader Web App Kurulum"
    echo "=========================================="
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# OS detection
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        OS="Unknown"
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    fi
}

# Python kurulumu kontrolü
check_python() {
    echo "🐍 Python kontrolü..."
    if command -v $PYTHON_CMD &> /dev/null; then
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
        print_success "Python $PYTHON_VERSION mevcut"
        return 0
    else
        print_error "Python bulunamadı!"
        return 1
    fi
}

# Python kurulum
install_python() {
    echo "📦 Python yükleniyor..."
    
    if [[ "$OS" == "macOS" ]]; then
        if command -v brew &> /dev/null; then
            brew install python3
        else
            print_warning "Homebrew bulunamadı. Python'u manuel yükleyin: https://python.org"
            open "https://python.org/downloads/"
            exit 1
        fi
    elif [[ "$OS" == "Linux" ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v pacman &> /dev/null; then
            sudo pacman -S python python-pip
        else
            print_error "Paket yöneticisi bulunamadı. Python'u manuel yükleyin."
            exit 1
        fi
    fi
}

# Bağımlılıkları yükle
install_dependencies() {
    echo "📦 Gerekli kütüphaneler yükleniyor..."
    
    # Pip'i güncelle
    $PYTHON_CMD -m pip install --upgrade pip
    
    # Ana kütüphaneler
    $PIP_CMD install flask requests yt-dlp spotdl six
    
    if [ $? -eq 0 ]; then
        print_success "Kütüphaneler başarıyla yüklendi"
    else
        print_error "Kütüphane yükleme hatası!"
        exit 1
    fi
}

# Klasörleri hazırla
setup_directories() {
    echo "📁 Dizinler hazırlanıyor..."
    
    # İndirme klasörü
    MUSIC_DIR="$HOME/Desktop/Music"
    mkdir -p "$MUSIC_DIR"
    print_success "İndirme klasörü: $MUSIC_DIR"
    
    # App klasörü kontrolü
    if [ ! -d "music_downloader_app" ]; then
        print_error "music_downloader_app klasörü bulunamadı!"
        exit 1
    fi
}

# Uygulamayı başlat
start_app() {
    echo "🚀 Web uygulaması başlatılıyor..."
    echo "🌐 Tarayıcınızda otomatik olarak açılacak: http://localhost:5001"
    echo "⚡ Durdurmak için Ctrl+C basın"
    echo ""
    
    # Tarayıcıda aç
    if [[ "$OS" == "macOS" ]]; then
        open "http://localhost:5001" &
    elif [[ "$OS" == "Linux" ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "http://localhost:5001" &
        fi
    fi
    
    # Uygulamayı başlat
    cd music_downloader_app
    $PYTHON_CMD app.py
}

# Ana fonksiyon
main() {
    print_header
    
    detect_os
    print_info "İşletim sistemi: $OS"
    
    # Python kontrolü ve kurulumu
    if ! check_python; then
        install_python
        if ! check_python; then
            print_error "Python kurulumu başarısız!"
            exit 1
        fi
    fi
    
    # Bağımlılıkları yükle
    install_dependencies
    
    # Dizinleri hazırla
    setup_directories
    
    print_success "Kurulum tamamlandı!"
    echo ""
    
    # Uygulamayı başlat
    start_app
}

# Scripti çalıştır
main "$@"
