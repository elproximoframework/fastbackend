import psycopg2

conn = psycopg2.connect('postgresql://space_user:space_password@localhost:5433/space_db')
cur = conn.cursor()

# 1. NULL to 'other'
cur.execute("UPDATE companies SET type = 'other' WHERE type IS NULL")
print(f"Updated {cur.rowcount} records from NULL to 'other'")

# 2. 'non-profit' to 'non_profit'
cur.execute("UPDATE companies SET type = 'non_profit' WHERE type = 'non-profit'")
print(f"Updated {cur.rowcount} records from 'non-profit' to 'non_profit'")

# 3. 'government' to 'agency'
cur.execute("UPDATE companies SET type = 'agency' WHERE type = 'government'")
print(f"Updated {cur.rowcount} records from 'government' to 'agency'")

# 4. 'research' to 'academia'
cur.execute("UPDATE companies SET type = 'academia' WHERE type = 'research'")
print(f"Updated {cur.rowcount} records from 'research' to 'academia'")

conn.commit()
cur.close()
conn.close()
