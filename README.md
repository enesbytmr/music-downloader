# 🎵 Music Downloader Web App

Easily download YouTube Music and Spotify playlists with a modern web interface!

![Music Downloader](https://img.shields.io/badge/Music-Downloader-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-Web%20App-red)
![Cross Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ Features

- 🎵 **Dual Platform:** YouTube Music + Spotify support
- 🎨 **Modern Web Interface:** Responsive and user-friendly design
- 📊 **Live Tracking:** Real-time progress bar and log monitoring
- 🎧 **High Quality:** M4A format audio downloads
- 🏷️ **Metadata:** Automatic song information and album art embedding
- 🍪 **Automatic Cookie Management:** Auto cookie extraction from browsers
- 🌐 **Cross-Platform:** Compatible with Windows, macOS, Linux
- 🚀 **Easy Setup:** One-command installation and startup

## 🚀 Quick Start

### Initial Setup (One Time Only)

#### Windows
```cmd
setup.bat
```

#### macOS/Linux
```bash
chmod +x setup.sh
./setup.sh
```

### Daily Usage (Every Time)

#### Windows
```cmd
start_app.bat
```

#### macOS/Linux
```bash
./start_app.sh
```

### Web Interface
1. After setup/startup, open in browser: **http://localhost:5001**
2. Paste YouTube Music or Spotify playlist URL
3. Start download and track live progress!

## 📱 Usage Steps

1. **URL Input:** Paste YouTube Music or Spotify playlist URL
2. **Folder Name:** Optional - automatic name if left blank
3. **Download Location:** Default: `~/Desktop/Music`
4. **Cookie Management:** Automatic cookie settings for YouTube
5. **Live Monitoring:** Real-time tracking on progress page

## 🛠️ Installation Details

### Requirements
- Python 3.8+ (will be installed automatically)
- Internet connection
- Disk space (depending on playlist size)

### Manual Installation
```bash
# Clone the repository
git clone https://github.com/USERNAME/music-downloader-web.git
cd music-downloader-web

# Install required packages
pip install -r requirements.txt

# Start the application
./start_app.sh
```

## 📁 Project Structure

```
music-downloader-web/
├── setup.sh/bat          # Initial setup scripts
├── start_app.sh/bat      # Daily startup scripts
├── ytbmsc.py            # YouTube Music downloader
├── spotidownloader.py   # Spotify downloader
├── music_downloader_app/
│   ├── app.py           # Flask web application
│   ├── templates/       # HTML templates
│   │   ├── index.html   # Main page
│   │   ├── cookies.html # Cookie management
│   │   └── progress.html# Download tracking
│   └── static/          # CSS/JS files
├── auto_cookie_extractor.py # Automatic cookie extraction
├── cookies.txt          # YouTube authentication
└── README.md
```

## 🍪 Cookie Management

### Automatic Cookie Extraction
- Chrome, Edge, Firefox, Safari support
- One-click cookie extraction from browsers
- Cross-platform compatibility

### Manual Cookie Upload
- Drag & drop file upload
- Ready-made cookies.txt file support
- Netscape format compatibility

## 🎯 Supported Platforms

| Platform | YouTube Music | Spotify | Notes |
|----------|---------------|---------|--------|
| **YouTube Music** | ✅ | - | Cookie required |
| **Spotify** | - | ✅ | Search from YouTube |

## 📊 Feature Details

### Web Interface
- **Responsive Design:** Works on all devices
- **Modern UI:** Bootstrap 5 + Font Awesome
- **Real-time Updates:** Live updates with AJAX
- **Progress Tracking:** Detailed download monitoring

### Download Features
- **High Quality:** M4A format audio
- **Metadata:** Automatic song information
- **Thumbnail:** Album art embedding
- **Batch Download:** Bulk playlist downloading

## 🔧 Troubleshooting

### Common Issues

**1. YouTube "Sign in" error:**
- Extract automatic cookies from Cookie Settings page
- Make sure you're logged into YouTube in your browser

**2. Port 5001 in use:**
- Close existing application: `Ctrl+C`
- Check port: `lsof -i :5001`

**3. Python not found:**
- Install Python 3.8+
- Check PATH settings

**4. Download not starting:**
- Check your internet connection
- Make sure playlist URL is correct
- Check log files

### Support

If you experience issues:
1. Run Terminal/CMD as administrator
2. Temporarily disable antivirus software
3. Check firewall settings
4. Open an issue: [GitHub Issues](https://github.com/USERNAME/music-downloader-web/issues)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## 📄 License

This project is distributed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube download engine
- [spotdl](https://github.com/spotDL/spotify-downloader) - Spotify downloader
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework


---

⭐ **Don't forget to star this project if you liked it!** ⭐


