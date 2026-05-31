# Downloading youtube videos

#installations
#pip install yt-dlp tqdm pandas openpyxl

import pandas as pd
import subprocess
import os
from tqdm import tqdm
import time
from datetime import datetime

SOBER_EXCEL = r"C:/Users/simrankhare/Desktop/dataset_links_sober.xlsx"
DRUNK_EXCEL = r"C:/Users/simrankhare/Desktop/dataset_links_drunk.xlsx"     

# Output directory on D drive because i have more space there
OUTPUT_BASE_DIR = r"D:\DIF_Videos"

DRUNK_DIR = os.path.join(OUTPUT_BASE_DIR, "drunk")
SOBER_DIR = os.path.join(OUTPUT_BASE_DIR, "sober")

LOG_DIR = os.path.join(OUTPUT_BASE_DIR, "logs")

# create directory
for dir_path in [DRUNK_DIR, SOBER_DIR]:
    os.makedirs(dir_path, exist_ok=True)

print(f"Output directories ready:")
print(f"Drunk:  {DRUNK_DIR}")
print(f"Sober:  {SOBER_DIR}")

#loading URLs

def load_urls_from_excel(filepath, category):
    try:
        df = pd.read_excel(filepath, sheet_name=0, header=None)
        
        # Get all URLs from Column B
        urls = df[1].dropna().tolist()
        
        # Filter to only YouTube URLs
        youtube_urls = [url for url in urls if 'youtube' in str(url).lower()]
        
        print(f"Loaded {category.upper()} Excel file")
        print(f"File: {filepath}")
        print(f"Total URLs: {len(youtube_urls)}\n")
        
        return youtube_urls
    
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return []
    except Exception as e:
        print(f"ERROR reading file: {str(e)}")
        return []
    
    
#Loading Files

sober_urls = load_urls_from_excel(SOBER_EXCEL, "sober")
drunk_urls = load_urls_from_excel(DRUNK_EXCEL, "drunk")
if not sober_urls or not drunk_urls:
    print("\nERROR: Could not load Excel files.")
    print("Please check your file paths and try again.")
    exit()

#downloading
def download_video(url, index, category, output_dir):
    # Extract video ID from URL
    try:
        video_id = url.split('v=')[1].split('&')[0]
    except:
        video_id = f"{category}_{index:03d}"
    
    output_path = os.path.join(output_dir, f"{video_id}.mp4")
    
    # Check if already downloaded
    if os.path.exists(output_path):
        size_mb = round(os.path.getsize(output_path) / (1024*1024), 2)
        return {
            'index': index,
            'url': url[:50],
            'category': category,
            'video_id': video_id,
            'status': 'ALREADY_EXISTS',
            'size_mb': size_mb,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Download
    try:
        cmd = [
            'yt-dlp',
            url,
            '-f', 'best[ext=mp4]/best',
            '-o', output_path,
            '--no-playlist',
            '--socket-timeout', '30',
            '-q'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists(output_path):
            size_mb = round(os.path.getsize(output_path) / (1024*1024), 2)
            return {
                'index': index,
                'url': url[:50],
                'category': category,
                'video_id': video_id,
                'status': 'SUCCESS',
                'size_mb': size_mb,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                'index': index,
                'url': url[:50],
                'category': category,
                'video_id': video_id,
                'status': 'FAILED',
                'size_mb': 0,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    except Exception as e:
        return {
            'index': index,
            'url': url[:50],
            'category': category,
            'video_id': video_id,
            'status': 'FAILED',
            'size_mb': 0,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
print(f"STARTING DOWNLOADS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

stats = {
    'drunk': {'success': 0, 'failed': 0, 'already_exists': 0, 'total_size_mb': 0},
    'sober': {'success': 0, 'failed': 0, 'already_exists': 0, 'total_size_mb': 0}
}

download_results = []

# Download sober videos
print("Downloading SOBER videos...\n")
for idx, url in tqdm(enumerate(sober_urls), total=len(sober_urls), desc="Sober Videos"):
    result = download_video(url, idx, 'sober', SOBER_DIR)
    download_results.append(result)
    
    status = result['status']
    if status == 'SUCCESS':
        stats['sober']['success'] += 1
        stats['sober']['total_size_mb'] += result.get('size_mb', 0)
    elif status == 'ALREADY_EXISTS':
        stats['sober']['already_exists'] += 1
        stats['sober']['total_size_mb'] += result.get('size_mb', 0)
    else:
        stats['sober']['failed'] += 1

print()

# Download drunk videos
print("Downloading DRUNK videos...\n")
for idx, url in tqdm(enumerate(drunk_urls), total=len(drunk_urls), desc="Drunk Videos"):
    result = download_video(url, idx, 'drunk', DRUNK_DIR)
    download_results.append(result)
    
    status = result['status']
    if status == 'SUCCESS':
        stats['drunk']['success'] += 1
        stats['drunk']['total_size_mb'] += result.get('size_mb', 0)
    elif status == 'ALREADY_EXISTS':
        stats['drunk']['already_exists'] += 1
        stats['drunk']['total_size_mb'] += result.get('size_mb', 0)
    else:
        stats['drunk']['failed'] += 1

print(f"DOWNLOAD COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*80}\n")

drunk_total = stats['drunk']['success'] + stats['drunk']['failed'] + stats['drunk']['already_exists']
sober_total = stats['sober']['success'] + stats['sober']['failed'] + stats['sober']['already_exists']



