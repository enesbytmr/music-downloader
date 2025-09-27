#!/usr/bin/env python3

import os
import argparse
import subprocess

def sanitize(s: str) -> str:
    """
    Remove characters invalid for filenames.
    """
    return "".join(c for c in s if c.isalnum() or c in " _-").rstrip()

def main():
    parser = argparse.ArgumentParser(
        description='Download a Spotify playlist via the spotdl CLI.'
    )
    parser.add_argument(
        'playlist',
        help='Spotify playlist URL'
    )
    parser.add_argument(
        '--output-dir',
        default='downloads',
        help='Base directory to save downloads'
    )
    parser.add_argument(
        '--folder-name',
        help='Name of the playlist folder (defaults to playlist ID)'
    )
    parser.add_argument(
        '--cookies',
        help='Path to cookies.txt file for YouTube Music authentication (optional)'
    )

    args = parser.parse_args()

    # Determine playlist folder name
    if args.folder_name:
        playlist_name = sanitize(args.folder_name)
    else:
        raw_name = args.playlist.rstrip('/').split('/')[-1].split('?')[0]
        playlist_name = sanitize(raw_name)

    # Create base directory
    base_dir = os.path.join(args.output_dir, playlist_name)
    os.makedirs(base_dir, exist_ok=True)

    # Output template: no subfolders
    output_template = os.path.join(
        base_dir
    )

    # Build command
    cmd = [
        'spotdl',
        args.playlist,
        '--output', output_template,
        '--audio', 'youtube',  # Use regular YouTube instead of YouTube Music
        '--format', 'm4a',
        '--cookie-file', '/Users/fevzienesbaytemir/Documents/djenes/cookies.txt',
        '--search-query', '{title} {artists}',  # More flexible search - title first
        '--dont-filter-results',  # Don't filter results strictly
        '--simple-tui',  # Simpler interface
        '--max-retries', '3',  # Retry failed downloads
        '--skip-explicit'  # Skip explicit content if needed
    ]

    # Add additional cookies if provided via argument
    if args.cookies:
        cmd.extend(['--cookie-file', args.cookies])

    # Add cookies if provided
    if args.cookies:
        cmd.extend(['--cookie-file', args.cookies])

    print('Running:', ' '.join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("Download completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Download failed with error code {e.returncode}")
        print("This might be due to:")
        print("1. YouTube API rate limiting")
        print("2. Cookie authentication issues")
        print("3. Some tracks not being available")
        print("Try running the command again or check your cookies.txt file")
        return

if __name__ == '__main__':
    main()