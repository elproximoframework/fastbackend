import os
import shutil
import psycopg2

# Configuration
LOCAL_URL = "postgresql://space_user:space_password@localhost:5433/space_db"
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

FRONTEND_IMAGES_DIR = r"d:\YoutubeElProximoFrameworkEnElEspacio\Web\Frontend\public\assets\imagesnew"
BACKEND_IMAGES_DIR = r"d:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\news_images"

def migrate_files():
    print(f"Checking frontend images in: {FRONTEND_IMAGES_DIR}")
    if not os.path.exists(FRONTEND_IMAGES_DIR):
        print("Frontend images directory not found.")
        return

    if not os.path.exists(BACKEND_IMAGES_DIR):
        os.makedirs(BACKEND_IMAGES_DIR)

    files = os.listdir(FRONTEND_IMAGES_DIR)
    print(f"Found {len(files)} files to migrate.")

    for file in files:
        src = os.path.join(FRONTEND_IMAGES_DIR, file)
        dst = os.path.join(BACKEND_IMAGES_DIR, file)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print(f"Copied: {file}")

def update_db(url, db_name):
    print(f"Connecting to {db_name}...")
    try:
        conn = psycopg2.connect(url)
        conn.autocommit = True
        cur = conn.cursor()
        
        print(f"Updating image paths in {db_name}...")
        # Remove the prefix /assets/imagesnew/ from the image field
        cur.execute("UPDATE news SET image = REPLACE(image, '/assets/imagesnew/', '') WHERE image LIKE '/assets/imagesnew/%';")
        
        print(f"Success in {db_name}!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in {db_name}: {e}")

if __name__ == "__main__":
    migrate_files()
    update_db(LOCAL_URL, "Local DB")
    update_db(REMOTE_URL, "Remote DB (Railway)")
