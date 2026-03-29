import os
import shutil

# Paths
FRONTEND_LOGOS_DIR = r"d:\YoutubeElProximoFrameworkEnElEspacio\Web\Frontend\public\logos"
BACKEND_LOGOS_DIR = r"d:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\company_logos"

def main():
    if not os.path.exists(FRONTEND_LOGOS_DIR):
        print(f"Error: Frontend logos directory not found at {FRONTEND_LOGOS_DIR}")
        return

    if not os.path.exists(BACKEND_LOGOS_DIR):
        os.makedirs(BACKEND_LOGOS_DIR)
        print(f"Created backend logos directory at {BACKEND_LOGOS_DIR}")

    # Copy files
    files = [f for f in os.listdir(FRONTEND_LOGOS_DIR) if os.path.isfile(os.path.join(FRONTEND_LOGOS_DIR, f))]
    
    for file_name in files:
        src_path = os.path.join(FRONTEND_LOGOS_DIR, file_name)
        dst_path = os.path.join(BACKEND_LOGOS_DIR, file_name)
        
        try:
            shutil.copy2(src_path, dst_path)
            print(f"Copied: {file_name}")
        except Exception as e:
            print(f"Failed to copy {file_name}: {e}")

    print(f"\nMigration complete. {len(files)} files processed.")

if __name__ == "__main__":
    main()
