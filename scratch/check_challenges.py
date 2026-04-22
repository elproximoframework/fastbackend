import sqlite3

def check_challenges():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM challenges LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}")
    conn.close()

if __name__ == "__main__":
    check_challenges()
