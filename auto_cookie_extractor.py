#!/usr/bin/env python3

import os
import json
import sqlite3
import subprocess
import platform
from pathlib import Path
import shutil

def get_browser_cookie_paths():
    """Farklı işletim sistemleri ve browser'lar için cookie yollarını döndür"""
    system = platform.system()
    home = Path.home()
    
    paths = {}
    
    if system == "Windows":
        paths.update({
            "chrome": home / "AppData/Local/Google/Chrome/User Data/Default/Network/Cookies",
            "edge": home / "AppData/Local/Microsoft/Edge/User Data/Default/Network/Cookies",
            "firefox": home / "AppData/Roaming/Mozilla/Firefox/Profiles",
            "opera": home / "AppData/Roaming/Opera Software/Opera Stable/Network/Cookies"
        })
    elif system == "Darwin":  # macOS
        paths.update({
            "chrome": home / "Library/Application Support/Google/Chrome/Default/Network/Cookies",
            "safari": home / "Library/Cookies/Cookies.binarycookies",
            "firefox": home / "Library/Application Support/Firefox/Profiles",
            "edge": home / "Library/Application Support/Microsoft Edge/Default/Network/Cookies"
        })
    elif system == "Linux":
        paths.update({
            "chrome": home / ".config/google-chrome/Default/Network/Cookies",
            "chromium": home / ".config/chromium/Default/Network/Cookies",
            "firefox": home / ".mozilla/firefox",
            "opera": home / ".config/opera/Network/Cookies"
        })
    
    return paths

def extract_youtube_cookies_chrome(cookie_db_path):
    """Chrome/Chromium cookie database'inden YouTube cookies'lerini çıkar"""
    try:
        # Temporary copy (browser açıkken database kilitli olabilir)
        temp_db = "/tmp/temp_cookies.db"
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

def find_and_extract_cookies():
    """Mevcut browser'lardan YouTube cookies'lerini bul ve çıkar"""
    print("🍪 Browser cookies'leri aranıyor...")
    
    paths = get_browser_cookie_paths()
    extracted_cookies = []
    
    for browser, path in paths.items():
        if not path.exists():
            continue
            
        print(f"📁 {browser.title()} kontrol ediliyor...")
        
        if browser in ["chrome", "edge", "chromium", "opera"]:
            if path.name == "Cookies" and path.exists():
                cookies = extract_youtube_cookies_chrome(path)
                if cookies:
                    extracted_cookies.extend(cookies)
                    print(f"✅ {browser.title()}'dan {len(cookies)} cookie bulundu")
        
        elif browser == "firefox":
            # Firefox için ayrı implementasyon gerekebilir
            print(f"⚠️  {browser.title()} desteği henüz eklenmedi")
    
    if extracted_cookies:
        netscape_content = cookies_to_netscape_format(extracted_cookies)
        return netscape_content
    
    return None

def create_auto_cookies():
    """Otomatik cookie çıkarma ve kaydetme"""
    print("🔍 Otomatik cookie çıkarma başlatılıyor...")
    
    cookies_content = find_and_extract_cookies()
    
    if cookies_content:
        # Cookies'leri kaydet
        cookies_file = "cookies_auto.txt"
        with open(cookies_file, 'w', encoding='utf-8') as f:
            f.write(cookies_content)
        
        print(f"✅ Cookies başarıyla çıkarıldı: {cookies_file}")
        return cookies_file
    else:
        print("❌ Hiç cookie bulunamadı")
        return None

def test_cookies(cookies_file):
    """Cookies'lerin çalışıp çalışmadığını test et"""
    print("🧪 Cookies test ediliyor...")
    
    try:
        # yt-dlp ile basit bir test
        result = subprocess.run([
            'yt-dlp', 
            '--cookies', cookies_file,
            '--dump-json',
            'https://music.youtube.com/watch?v=dQw4w9WgXcQ'  # Test video
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Cookies çalışıyor!")
            return True
        else:
            print("❌ Cookies çalışmıyor")
            return False
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def main():
    print("🍪 YouTube Cookies Otomatik Çıkarıcı")
    print("=" * 40)
    
    # Cookies çıkar
    cookies_file = create_auto_cookies()
    
    if cookies_file:
        # Test et
        if test_cookies(cookies_file):
            print(f"🎉 Başarılı! {cookies_file} kullanıma hazır")
        else:
            print("⚠️  Cookies çıkarıldı ama test başarısız")
            print("Elle cookie çıkarmanız gerekebilir")
    else:
        print("💡 Manuel cookie çıkarma talimatları:")
        print("1. Browser'da YouTube.com'a gidin ve giriş yapın")
        print("2. F12 basın -> Application/Storage -> Cookies")
        print("3. YouTube.com cookies'lerini kopyalayın")
        print("4. cookies.txt dosyasına yapıştırın")

if __name__ == "__main__":
    main()
