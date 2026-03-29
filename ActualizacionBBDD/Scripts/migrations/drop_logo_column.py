import psycopg2
import os

def drop_column():
    # Connection parameters
    conn_str = os.getenv("DATABASE_URL", "postgresql://space_user:space_password@localhost:5433/space_db")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # SQL to drop the column if it exists
        sql = "ALTER TABLE companies DROP COLUMN IF EXISTS logo;"
        
        print(f"Executing: {sql}")
        cur.execute(sql)
        
        # Commit the changes
        conn.commit()
        print("Column 'logo' successfully dropped from 'companies' table!")
        
        # Close connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error dropping column: {e}")

if __name__ == "__main__":
    drop_column()
