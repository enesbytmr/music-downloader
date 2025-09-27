#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import subprocess
import os
import sys
import threading
import time
from datetime import datetime
import json
import shutil
import sqlite3
import platform
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'music_downloader_secret_key_2025'

# Ana dizinleri ayarla
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Music")

# Global değişkenler
download_status = {
    'is_downloading': False,
    'current_task': None,
    'progress': 0,
    'total': 0,
    'current_song': '',
    'error': None,
    'completed': False,
    'log': []
}

def sanitize_folder_name(name):
    """Klasör adını temizle"""
    return "".join(c for c in name if c.isalnum() or c in " _-").strip()

def get_browser_cookie_paths():
    """Farklı işletim sistemleri ve browser'lar için cookie yollarını döndür"""
    system = platform.system()
    home = Path.home()
    
    paths = {}
    
    if system == "Windows":
        paths.update({
            "chrome": home / "AppData/Local/Google/Chrome/User Data/Default/Network/Cookies",
            "edge": home / "AppData/Local/Microsoft/Edge/User Data/Default/Network/Cookies",
        })
    elif system == "Darwin":  # macOS
        paths.update({
            "chrome": home / "Library/Application Support/Google/Chrome/Default/Network/Cookies",
            "edge": home / "Library/Application Support/Microsoft Edge/Default/Network/Cookies"
        })
    elif system == "Linux":
        paths.update({
            "chrome": home / ".config/google-chrome/Default/Network/Cookies",
            "chromium": home / ".config/chromium/Default/Network/Cookies",
        })
    
    return paths

def extract_youtube_cookies_chrome(cookie_db_path):
    """Chrome/Chromium cookie database'inden YouTube cookies'lerini çıkar"""
    try:
        # Temporary copy (browser açıkken database kilitli olabilir)
        temp_db = os.path.join(os.getcwd(), "temp_cookies.db")
        shutil.copy2(cookie_db_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # YouTube cookies'lerini çıkar
        cursor.execute("""
            SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly
            FROM cookies 
            WHERE host_key LIKE '%youtube.com%' OR host_key LIKE '%google.com%'
        """)
        
        cookies = cursor.fetchall()
        conn.close()
        os.remove(temp_db)
        
        return cookies
    except Exception as e:
        print(f"Chrome cookies çıkarma hatası: {e}")
        return []

def cookies_to_netscape_format(cookies):
    """Cookies'leri Netscape/yt-dlp formatına çevir"""
    netscape_lines = ["# Netscape HTTP Cookie File\n"]
    
    for cookie in cookies:
        name, value, domain, path, expires, secure, httponly = cookie
        
        # Expires timestamp'i düzelt (Chrome microseconds kullanır)
        if expires:
            expires = int(expires / 1000000) - 11644473600  # Windows epoch to Unix epoch
        else:
            expires = 0
            
        secure_flag = "TRUE" if secure else "FALSE"
        domain_flag = "TRUE" if domain.startswith('.') else "FALSE"
        
        line = f"{domain}\t{domain_flag}\t{path}\t{secure_flag}\t{expires}\t{name}\t{value}\n"
        netscape_lines.append(line)
    
    return "".join(netscape_lines)

def auto_extract_cookies():
    """Otomatik cookie çıkarma"""
    try:
        paths = get_browser_cookie_paths()
        extracted_cookies = []
        
        for browser, path in paths.items():
            if not path.exists():
                continue
                
            if browser in ["chrome", "edge", "chromium"]:
                cookies = extract_youtube_cookies_chrome(path)
                if cookies:
                    extracted_cookies.extend(cookies)
        
        if extracted_cookies:
            netscape_content = cookies_to_netscape_format(extracted_cookies)
            
            # Auto cookies dosyasını kaydet
            auto_cookies_path = os.path.join(PARENT_DIR, 'cookies_auto.txt')
            with open(auto_cookies_path, 'w', encoding='utf-8') as f:
                f.write(netscape_content)
            
            return auto_cookies_path
        
        return None
    except Exception as e:
        print(f"Auto cookie extraction error: {e}")
        return None

def run_youtube_downloader(url, output_dir, folder_name):
    """YouTube Music downloader çalıştır"""
    global download_status
    
    try:
        download_status['is_downloading'] = True
        download_status['current_task'] = 'YouTube Music'
        download_status['error'] = None
        download_status['completed'] = False
        download_status['log'] = []
        
        # Cookie dosyasını belirle
        cookies_file = None
        
        # Önce manuel cookies'i dene (senin dosyan)
        manual_cookies = os.path.join(PARENT_DIR, 'cookies.txt')
        auto_cookies = os.path.join(PARENT_DIR, 'cookies_auto.txt')
        
        if os.path.exists(manual_cookies):
            cookies_file = manual_cookies
            download_status['log'].append(f"Manuel cookies.txt kullanılıyor")
        elif os.path.exists(auto_cookies):
            cookies_file = auto_cookies
            download_status['log'].append(f"Otomatik cookies_auto.txt kullanılıyor")
        else:
            # Otomatik çıkarma dene
            download_status['log'].append(f"Cookie dosyası bulunamadı, otomatik çıkarma deneniyor...")
            auto_cookies_result = auto_extract_cookies()
            if auto_cookies_result:
                cookies_file = auto_cookies_result
                download_status['log'].append(f"Otomatik cookie çıkarma başarılı")
            else:
                download_status['log'].append(f"⚠️ Cookie bulunamadı! Bazı videolar indirilemeyebilir.")
        
        # ytbmsc.py scriptini çalıştır
        ytbmsc_path = os.path.join(PARENT_DIR, 'ytbmsc.py')
        cmd = [
            'python3.11', ytbmsc_path,
            url,
            '--output-dir', output_dir,
            '--folder-name', folder_name
        ]
        
        if cookies_file:
            cmd.extend(['--cookies', cookies_file])
        
        download_status['log'].append(f"YouTube Music indirme başlatıldı: {folder_name}")
        download_status['log'].append(f"Komut: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=PARENT_DIR
        )
        
        # Output'u oku ve progress takip et
        for line in iter(process.stdout.readline, ''):
            if line:
                download_status['log'].append(line.strip())
                
                # Progress tracking
                if 'Downloading item' in line:
                    try:
                        parts = line.split('Downloading item')[1].split('of')
                        current = int(parts[0].strip())
                        total = int(parts[1].strip().split()[0])
                        download_status['progress'] = current
                        download_status['total'] = total
                        download_status['current_song'] = f"Şarkı {current}/{total}"
                    except:
                        pass
                elif 'Destination:' in line:
                    try:
                        song_name = line.split('/')[-1].replace('.m4a', '')
                        download_status['current_song'] = song_name[:50]
                    except:
                        pass
        
        process.wait()
        
        if process.returncode == 0:
            download_status['completed'] = True
            download_status['log'].append("✅ YouTube Music indirme tamamlandı!")
        else:
            download_status['error'] = f"YouTube Music indirme hatası (kod: {process.returncode})"
            
    except Exception as e:
        download_status['error'] = f"YouTube Music indirme hatası: {str(e)}"
    finally:
        download_status['is_downloading'] = False

def run_spotify_downloader(url, output_dir, folder_name):
    """Spotify downloader çalıştır"""
    global download_status
    
    try:
        download_status['is_downloading'] = True
        download_status['current_task'] = 'Spotify'
        download_status['error'] = None
        download_status['completed'] = False
        download_status['log'] = []
        
        # spotidownloader.py scriptini çalıştır
        spoti_path = os.path.join(PARENT_DIR, 'spotidownloader.py')
        cmd = [
            'python3.11', spoti_path,
            url,
            '--output-dir', output_dir,
            '--folder-name', folder_name
        ]
        
        download_status['log'].append(f"Spotify indirme başlatıldı: {folder_name}")
        download_status['log'].append(f"Komut: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=PARENT_DIR
        )
        
        # Output'u oku ve progress takip et
        for line in iter(process.stdout.readline, ''):
            if line:
                download_status['log'].append(line.strip())
                
                # Progress tracking
                if '/103 complete' in line or '/100 complete' in line:
                    try:
                        current = int(line.split('/')[0].strip())
                        total = int(line.split('/')[1].split(' ')[0])
                        download_status['progress'] = current
                        download_status['total'] = total
                    except:
                        pass
                elif 'Downloaded' in line and '"' in line:
                    try:
                        song_name = line.split('"')[1]
                        download_status['current_song'] = song_name[:50]
                    except:
                        pass
        
        process.wait()
        
        if process.returncode == 0:
            download_status['completed'] = True
            download_status['log'].append("✅ Spotify indirme tamamlandı!")
        else:
            download_status['error'] = f"Spotify indirme hatası (kod: {process.returncode})"
            
    except Exception as e:
        download_status['error'] = f"Spotify indirme hatası: {str(e)}"
    finally:
        download_status['is_downloading'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get('url', '').strip()
        folder_name = request.form.get('folder_name', '').strip()
        output_dir = request.form.get('output_dir', DOWNLOADS_DIR).strip()
        
        if not url:
            flash('URL boş olamaz!', 'error')
            return redirect(url_for('index'))
        
        if not folder_name:
            folder_name = f"playlist_{int(time.time())}"
        
        folder_name = sanitize_folder_name(folder_name)
        
        # URL tipini kontrol et
        if 'music.youtube.com' in url:
            # YouTube Music
            thread = threading.Thread(
                target=run_youtube_downloader,
                args=(url, output_dir, folder_name)
            )
            thread.daemon = True
            thread.start()
            
        elif 'spotify.com' in url:
            # Spotify
            thread = threading.Thread(
                target=run_spotify_downloader,
                args=(url, output_dir, folder_name)
            )
            thread.daemon = True
            thread.start()
            
        else:
            flash('Desteklenmeyen URL! Lütfen YouTube Music veya Spotify playlist URL\'si girin.', 'error')
            return redirect(url_for('index'))
        
        return redirect(url_for('progress'))
        
    except Exception as e:
        flash(f'Hata: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/cookies')
def cookies_page():
    return render_template('cookies.html')

@app.route('/api/status')
def api_status():
    return jsonify(download_status)

@app.route('/api/logs')
def api_logs():
    return jsonify({
        'logs': download_status['log'][-50:],  # Son 50 log satırı
        'is_downloading': download_status['is_downloading'],
        'error': download_status['error'],
        'completed': download_status['completed']
    })

@app.route('/api/extract-cookies', methods=['POST'])
def extract_cookies():
    try:
        auto_cookies = auto_extract_cookies()
        if auto_cookies:
            return jsonify({
                'success': True,
                'message': 'Cookies başarıyla çıkarıldı!',
                'file': 'cookies_auto.txt'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Cookies çıkarılamadı. Browser\'da YouTube\'a giriş yapmış olduğunuzdan emin olun.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        })

@app.route('/api/upload-cookies', methods=['POST'])
def upload_cookies():
    try:
        if 'cookies' not in request.files:
            return jsonify({'success': False, 'message': 'Dosya seçilmedi'})
        
        file = request.files['cookies']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Dosya seçilmedi'})
        
        if file:
            cookies_path = os.path.join(PARENT_DIR, 'cookies_manual.txt')
            file.save(cookies_path)
            return jsonify({
                'success': True,
                'message': 'Cookies dosyası başarıyla yüklendi!'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Hata: {str(e)}'
        })

@app.route('/api/cookie-status')
def cookie_status():
    status = {
        'auto_cookies': os.path.exists(os.path.join(PARENT_DIR, 'cookies_auto.txt')),
        'manual_cookies': os.path.exists(os.path.join(PARENT_DIR, 'cookies.txt')),
        'uploaded_cookies': os.path.exists(os.path.join(PARENT_DIR, 'cookies_manual.txt'))
    }
    
    return jsonify(status)

if __name__ == '__main__':
    # Downloads dizinini oluştur
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    
    print("🎵 Music Downloader Web App")
    print(f"📁 İndirme dizini: {DOWNLOADS_DIR}")
    print("🌐 Web arayüzü: http://localhost:5001")
    print("⚡ Ctrl+C ile durdurun")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
