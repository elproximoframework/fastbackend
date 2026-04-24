import sys
import os
import argparse
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# Try to import yt-dlp, if not present, advise the user
try:
    import yt_dlp
except ImportError:
    print("Error: 'yt-dlp' is not installed. Please run: pip install yt-dlp")
    sys.exit(1)

# Database configuration
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

DB_URLS = [LOCAL_URL, REMOTE_URL]

def get_video_info(url):
    """Fetches video metadata using yt-dlp"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract relevant fields
            title = info.get('title', 'No Title')
            description = info.get('description', '')
            # yt-dlp date is YYYYMMDD
            upload_date = info.get('upload_date', datetime.now().strftime("%Y%m%d"))
            formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
            
            return {
                'video_name': title,
                'url': url,
                'description': description[:500] + ('...' if len(description) > 500 else ''), # Limiting length
                'date': formatted_date
            }
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return None

def save_to_db(video_data, video_type, own=False):
    """Inserts the video record into all configured databases"""
    successCount = 0
    for db_url in DB_URLS:
        db_name = "Local" if "localhost" in db_url else "Remote"
        try:
            conn = psycopg2.connect(db_url)
            conn.set_client_encoding('UTF8')
            conn.autocommit = True
            cur = conn.cursor()
            
            # Using UPSERT (INSERT ... ON CONFLICT)
            cur.execute(
                """
                INSERT INTO youtube (video_name, url, type, description, description_en, date, own, show) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    video_name = EXCLUDED.video_name,
                    type = EXCLUDED.type,
                    description = EXCLUDED.description,
                    description_en = EXCLUDED.description_en,
                    date = EXCLUDED.date,
                    own = EXCLUDED.own,
                    show = EXCLUDED.show
                """,
                (
                    video_data['video_name'],
                    video_data['url'],
                    video_type,
                    video_data['description'],
                    video_data['description'], # Using same for EN
                    video_data['date'],
                    own,
                    True # show = True by default
                )
            )
            
            # Using encode/decode to avoid console print errors on Windows
            try:
                print(f"[{db_name}] Successfully added: {video_data['video_name']}")
            except UnicodeEncodeError:
                print(f"[{db_name}] Successfully added: {video_data['video_name'].encode('ascii', 'ignore').decode('ascii')}")
            
            cur.close()
            conn.close()
            successCount += 1
        except Exception as e:
            print(f"[{db_name}] Database error: {e}")
    
    return successCount > 0

def main():
    parser = argparse.ArgumentParser(description="Add a YouTube video to the database automatically.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--type", choices=['new_spacex', 'new_china', 'new_space', 'launches', 'other'], 
                        default='other', help="Video category")
    parser.add_argument("--own", action="store_true", help="Mark as own content")
    
    args = parser.parse_args()
    
    print(f"Fetching info for {args.url}...")
    video_info = get_video_info(args.url)
    
    if video_info:
        save_to_db(video_info, args.type, args.own)
    else:
        print("Failed to retrieve video information.")

if __name__ == "__main__":
    main()
