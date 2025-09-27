#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys

def sanitize(s: str) -> str:
    """
    Remove characters invalid for filenames.
    """
    return "".join(c for c in s if c.isalnum() or c in " _-").rstrip()

def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube Music playlist with best quality'
    )
    parser.add_argument(
        'playlist_url',
        help='YouTube Music playlist URL'
    )
    parser.add_argument(
        '--output-dir',
        default='downloads',
        help='Base directory to save downloads'
    )
    parser.add_argument(
        '--folder-name',
        help='Name of the playlist folder (if not provided, will use playlist title)'
    )
    parser.add_argument(
        '--cookies',
        default=None,
        help='Path to cookies.txt file for YouTube Music authentication'
    )

    args = parser.parse_args()

    # Validate URL
    if 'music.youtube.com' not in args.playlist_url:
        print("Error: Please provide a valid YouTube Music playlist URL")
        sys.exit(1)

    # Create output directory
    if args.folder_name:
        playlist_name = sanitize(args.folder_name)
    else:
        # Extract playlist ID and use it as folder name for now
        try:
            playlist_id = args.playlist_url.split('list=')[1].split('&')[0]
            playlist_name = f"ytmusic_{playlist_id[:10]}"
        except:
            playlist_name = "ytmusic_playlist"

    output_dir = os.path.join(args.output_dir, playlist_name)
    os.makedirs(output_dir, exist_ok=True)

    # Output template for best organization
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    # Build yt-dlp command for best quality audio
    cmd = [
        'yt-dlp',
        args.playlist_url,
        '--format', 'bestaudio[ext=m4a]/bestaudio[ext=aac]/bestaudio/best',
        '--output', output_template,
        '--ignore-errors',
        '--embed-thumbnail',  # Thumbnail'ı müzik dosyasına göm
        '--embed-metadata',   # Metadata'yı müzik dosyasına göm
        '--add-metadata',     # Ek metadata ekle
        '--no-write-info-json',  # Ayrı JSON dosyası oluşturma
        '--no-write-thumbnail',  # Ayrı thumbnail dosyası oluşturma
        '--no-write-playlist-metafiles'  # Playlist meta dosyalarını yazma
    ]
    
    # Add cookies if provided
    if args.cookies and os.path.exists(args.cookies):
        cmd.extend(['--cookies', args.cookies])
        print(f"Using cookies from: {args.cookies}")
    else:
        print("⚠️ Warning: No cookies provided. Some videos may not be accessible.")

    print(f"Downloading YouTube Music playlist to: {output_dir}")
    print('Running command:', ' '.join(cmd))
    print("-" * 60)

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("-" * 60)
        print(f"✅ Download completed successfully!")
        print(f"📁 Files saved to: {output_dir}")
        
        # Count downloaded files
        audio_files = [f for f in os.listdir(output_dir) if f.endswith(('.m4a', '.aac', '.mp3', '.webm'))]
        print(f"🎵 Total downloaded: {len(audio_files)} audio files")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed with error code {e.returncode}")
        print("Possible issues:")
        print("1. Invalid YouTube Music playlist URL")
        print("2. Playlist is private or unavailable") 
        print("3. Cookies file is invalid or expired")
        print("4. Network connectivity issues")
        print("5. Geographic restrictions")
        return 1
        
    except FileNotFoundError:
        print("❌ Error: yt-dlp not found!")
        print("Please install yt-dlp: pip install yt-dlp")
        return 1
        
    except KeyboardInterrupt:
        print("\n⚠️  Download interrupted by user")
        return 1

    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
