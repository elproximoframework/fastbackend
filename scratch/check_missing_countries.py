import psycopg2

REGION_COUNTRIES = {
  'Europa': ['ES', 'EU', 'FR', 'FI', 'DE', 'IT', 'UK', 'GB', 'SE', 'NL', 'BE', 'PL', 'PT', 'NO', 'DK', 'AT', 'CH', 'CZ', 'RO', 'GR', 'IE', 'HU', 'BG', 'HR', 'IS', 'LT', 'LU', 'RU', 'SK'],
  'Norteamérica': ['US', 'CA', 'MX'],
  'Asia': ['JP', 'IN', 'CN', 'KR', 'SG', 'TW', 'IL', 'AE', 'SA', 'ID', 'MY', 'TH', 'TR'],
  'Sudamérica': ['BR', 'AR', 'CL', 'CO', 'PE', 'VE'],
  'África': ['ZA', 'NG', 'EG', 'KE', 'MA', 'RW'],
  'Oceanía': ['AU', 'NZ'],
}

all_mapped = []
for region in REGION_COUNTRIES:
    all_mapped.extend(REGION_COUNTRIES[region])

conn = psycopg2.connect('postgresql://space_user:space_password@localhost:5433/space_db')
cur = conn.cursor()
cur.execute('SELECT DISTINCT country FROM companies WHERE show = True')
db_countries = [r[0] for r in cur.fetchall()]
cur.close()
conn.close()

missing = []
for db_c in db_countries:
    if db_c.upper() not in all_mapped:
        missing.append(db_c)

print(f"Mapped codes: {len(all_mapped)}")
print(f"DB codes (show=True): {len(db_countries)}")
print(f"Missing from mapping: {missing}")
