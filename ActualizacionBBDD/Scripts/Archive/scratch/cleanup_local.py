import psycopg2

def cleanup():
    conn_str = "postgresql://space_user:space_password@localhost:5433/space_db"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        ids_to_delete = [616, 618]
        for id_val in ids_to_delete:
            cur.execute("DELETE FROM companies WHERE id = %s", (id_val,))
            print(f"Deleted duplicate ID {id_val} from local database.")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cleanup()
