# 🎵 Music Downloader Web App

Modern web arayüzü ile YouTube Music ve Spotify playlist'lerini kolayca indirin!

![Music Downloader](https://img.shields.io/badge/Music-Downloader-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-Web%20App-red)
![Cross Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ Özellikler

- 🎵 **Dual Platform:** YouTube Music + Spotify desteği
- 🎨 **Modern Web Arayüzü:** Responsive ve kullanıcı dostu tasarım
- 📊 **Canlı Takip:** Real-time progress bar ve log takibi
- 🎧 **Yüksek Kalite:** M4A formatında ses indirme
- 🏷️ **Metadata:** Şarkı bilgileri ve kapak resmi otomatik ekleme
- 🍪 **Otomatik Cookie Yönetimi:** Browser'dan otomatik cookie çıkarma
- 🌐 **Cross-Platform:** Windows, macOS, Linux uyumlu
- 🚀 **Kolay Kurulum:** Tek komutla kurulum ve başlatma

## 🚀 Hızlı Başlangıç

### İlk Kurulum (Sadece Bir Kez)

#### Windows
```cmd
setup.bat
```

#### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

### Günlük Kullanım (Her Seferinde)

#### Windows
```cmd
start_app.bat
```

#### macOS/Linux
```bash
./start_app.sh
```

### Web Arayüzü
1. Kurulum/başlatma sonrası tarayıcıda: **http://localhost:5001**
2. YouTube Music veya Spotify playlist URL'sini yapıştırın
3. İndirmeyi başlatın ve canlı takip edin!

## 📱 Kullanım Adımları

1. **URL Girişi:** YouTube Music veya Spotify playlist URL'sini yapıştırın
2. **Klasör Adı:** İsteğe bağlı - boş bırakırsanız otomatik ad verilir
3. **İndirme Konumu:** Varsayılan: `~/Desktop/Music`
4. **Cookie Yönetimi:** YouTube için otomatik cookie ayarları
5. **Canlı İzleme:** Progress sayfasında real-time takip

## 🛠️ Kurulum Detayları

### Gereksinimler
- Python 3.8+ (otomatik kurulacak)
- İnternet bağlantısı
- Disk alanı (playlist boyutuna göre)

### Manuel Kurulum
```bash
# Repository'yi klonlayın
git clone https://github.com/USERNAME/music-downloader-web.git
cd music-downloader-web

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
./start_app.sh
```

## 📁 Proje Yapısı

```
music-downloader-web/
├── setup.sh/bat          # İlk kurulum scriptleri
├── start_app.sh/bat      # Günlük başlatma scriptleri
├── ytbmsc.py            # YouTube Music downloader
├── spotidownloader.py   # Spotify downloader
├── music_downloader_app/
│   ├── app.py           # Flask web uygulaması
│   ├── templates/       # HTML şablonları
│   │   ├── index.html   # Ana sayfa
│   │   ├── cookies.html # Cookie yönetimi
│   │   └── progress.html# İndirme takibi
│   └── static/          # CSS/JS dosyaları
├── auto_cookie_extractor.py # Otomatik cookie çıkarma
├── cookies.txt          # YouTube authentication
└── README.md
```

## 🍪 Cookie Yönetimi

### Otomatik Cookie Çıkarma
- Chrome, Edge, Firefox, Safari desteği
- Tek tıkla browser'dan cookie çıkarma
- Cross-platform uyumluluk

### Manuel Cookie Yükleme
- Drag & drop dosya yükleme
- Hazır cookies.txt dosyası desteği
- Netscape format uyumluluğu

## 🎯 Desteklenen Platformlar

| Platform | YouTube Music | Spotify | Notlar |
|----------|---------------|---------|--------|
| **YouTube Music** | ✅ | - | Cookie gerekli |
| **Spotify** | - | ✅ | YouTube'dan arama |

## 📊 Özellik Detayları

### Web Arayüzü
- **Responsive Tasarım:** Tüm cihazlarda çalışır
- **Modern UI:** Bootstrap 5 + Font Awesome
- **Real-time Updates:** AJAX ile canlı güncelleme
- **Progress Tracking:** Detaylı indirme takibi

### İndirme Özellikleri
- **Yüksek Kalite:** M4A formatında ses
- **Metadata:** Otomatik şarkı bilgileri
- **Thumbnail:** Kapak resmi ekleme
- **Batch Download:** Tüm playlist toplu indirme

## 🔧 Sorun Giderme

### Yaygın Sorunlar

**1. YouTube "Giriş yapın" hatası:**
- Cookie Ayarları sayfasından otomatik cookie çıkarın
- Browser'da YouTube'a giriş yapmış olduğunuzdan emin olun

**2. Port 5001 kullanımda:**
- Mevcut uygulamayı kapatın: `Ctrl+C`
- Port kontrolü: `lsof -i :5001`

**3. Python bulunamadı:**
- Python 3.8+ yükleyin
- PATH ayarlarını kontrol edin

**4. İndirme başlamıyor:**
- İnternet bağlantınızı kontrol edin
- Playlist URL'sinin doğru olduğundan emin olun
- Log dosyalarını kontrol edin

### Destek

Sorun yaşarsanız:
1. Terminali/CMD'yi yönetici olarak çalıştırın
2. Antivürüs yazılımınızı geçici kapatın
3. Firewall ayarlarını kontrol edin
4. Issue açın: [GitHub Issues](https://github.com/USERNAME/music-downloader-web/issues)

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun: `git checkout -b feature/AmazingFeature`
3. Değişikliklerinizi commit edin: `git commit -m 'Add AmazingFeature'`
4. Branch'i push edin: `git push origin feature/AmazingFeature`
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube indirme motoru
- [spotdl](https://github.com/spotDL/spotify-downloader) - Spotify indirme
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework

## 📞 İletişim

- **GitHub:** [@USERNAME](https://github.com/USERNAME)
- **Issues:** [Sorun bildir](https://github.com/USERNAME/music-downloader-web/issues)

---

⭐ **Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!** ⭐

Made with ❤️ by Music Downloader Team
