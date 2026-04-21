import psycopg2
import sys

conn_string = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

try:
    print(f"Intentando conectar a: {conn_string.split('@')[1]}")
    # Forzamos SSL mode require
    conn = psycopg2.connect(conn_string, sslmode='require')
    print("¡Conexión exitosa desde Python (con SSL)!")
    
    cur = conn.cursor()
    cur.execute("SELECT version();")
    record = cur.fetchone()
    print(f"Versión de PostgreSQL: {record}")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error en la conexión: {e}")
    sys.exit(1)
