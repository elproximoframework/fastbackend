from sqlalchemy import create_engine, text
engine = create_engine('postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway')
with engine.connect() as conn:
    result = conn.execute(text("SELECT name, slug, rutainformacion FROM companies WHERE slug='spacex'"))
    print('Remote DB spacex:', result.fetchone())
