import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

def run_backup():
    # Load remote env
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env.remote")
    load_dotenv(env_path)
    
    db_url = os.getenv("REMOTE_DATABASE_URL")
    if not db_url:
        print("Error: REMOTE_DATABASE_URL not found in .env.remote")
        return

    # Parse URL
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path.lstrip("/")
    hostname = result.hostname
    port = result.port or 5432

    # Prepare backup directory
    backup_dir = os.path.join(os.path.dirname(__file__), "..", "DB_Backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_remote_{database}_{timestamp}.sql"
    filepath = os.path.join(backup_dir, filename)

    print(f"Starting backup of {database} from {hostname}...")
    
    # Use Docker to run pg_dump
    # We use -e PGPASSWORD to avoid interactive prompt
    # We use --rm to remove the container after completion
    command = [
        "docker", "run", "--rm",
        "-e", f"PGPASSWORD={password}",
        "postgres:latest",
        "pg_dump",
        "-h", hostname,
        "-p", str(port),
        "-U", username,
        "-d", database
    ]

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            print(f"Executing command: docker run ... pg_dump -h {hostname} -p {port} -U {username} -d {database}")
            result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"Error during backup: {result.stderr}")
                f.close() # Ensure closed before deleting
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass
            else:
                print(f"Backup successful! Saved to: {filepath}")
                print(f"File size: {os.path.getsize(filepath)} bytes")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_backup()
