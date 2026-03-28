import sqlalchemy
from sqlalchemy import create_engine, inspect
import os

# Configuration (Defaults found in app/database.py and migrate_railway.py)
LOCAL_URL = os.getenv("DATABASE_URL", "postgresql://space_user:space_password@localhost:5433/space_db")
REMOTE_URL = "postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway"

def get_schema_info(engine):
    """Retrieves schema information from a given SQLAlchemy engine."""
    inspector = inspect(engine)
    schema_info = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema_info[table_name] = {
            col['name']: {
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': str(col['default']) if col['default'] else None
            } for col in columns
        }
    return schema_info

def compare_schemas(local_schema, remote_schema):
    """Compares two schemas and returns the differences."""
    diffs = {
        'missing_tables_in_remote': [],
        'missing_tables_in_local': [],
        'table_diffs': {}
    }
    
    local_tables = set(local_schema.keys())
    remote_tables = set(remote_schema.keys())
    
    diffs['missing_tables_in_remote'] = sorted(list(local_tables - remote_tables))
    diffs['missing_tables_in_local'] = sorted(list(remote_tables - local_tables))
    
    common_tables = local_tables & remote_tables
    
    for table in common_tables:
        table_diff = {
            'missing_cols_in_remote': [],
            'missing_cols_in_local': [],
            'type_mismatches': []
        }
        
        local_cols = local_schema[table]
        remote_cols = remote_schema[table]
        
        local_col_names = set(local_cols.keys())
        remote_col_names = set(remote_cols.keys())
        
        table_diff['missing_cols_in_remote'] = sorted(list(local_col_names - remote_col_names))
        table_diff['missing_cols_in_local'] = sorted(list(remote_col_names - local_col_names))
        
        common_cols = local_col_names & remote_col_names
        for col in common_cols:
            if local_cols[col]['type'] != remote_cols[col]['type']:
                table_diff['type_mismatches'].append({
                    'column': col,
                    'local_type': local_cols[col]['type'],
                    'remote_type': remote_cols[col]['type']
                })
        
        if table_diff['missing_cols_in_remote'] or table_diff['missing_cols_in_local'] or table_diff['type_mismatches']:
            diffs['table_diffs'][table] = table_diff
            
    return diffs

def main():
    print(f"Connecting to Local DB: {LOCAL_URL.split('@')[-1]}", flush=True)
    try:
        local_engine = create_engine(LOCAL_URL)
        local_schema = get_schema_info(local_engine)
    except Exception as e:
        print(f"Error connecting to local DB: {e}", flush=True)
        return

    print(f"Connecting to Remote DB: {REMOTE_URL.split('@')[-1]}", flush=True)
    try:
        remote_engine = create_engine(REMOTE_URL)
        remote_schema = get_schema_info(remote_engine)
    except Exception as e:
        print(f"Error connecting to remote DB: {e}", flush=True)
        return

    diffs = compare_schemas(local_schema, remote_schema)

    print("\n" + "="*50, flush=True)
    print("DATABASE STRUCTURE COMPARISON REPORT", flush=True)
    print("="*50, flush=True)

    if diffs['missing_tables_in_remote']:
        print("\n[!] Tables ONLY in Local (Missing in Remote):", flush=True)
        for t in diffs['missing_tables_in_remote']:
            print(f"  - {t}", flush=True)

    if diffs['missing_tables_in_local']:
        print("\n[!] Tables ONLY in Remote (Missing in Local):", flush=True)
        for t in diffs['missing_tables_in_local']:
            print(f"  - {t}", flush=True)

    if diffs['table_diffs']:
        print("\n[!] Structural differences in common tables:", flush=True)
        for table, diff in diffs['table_diffs'].items():
            print(f"\n  Table: {table}", flush=True)
            if diff['missing_cols_in_remote']:
                print(f"    - Missing columns in Remote: {', '.join(diff['missing_cols_in_remote'])}", flush=True)
            if diff['missing_cols_in_local']:
                print(f"    - Missing columns in Local: {', '.join(diff['missing_cols_in_local'])}", flush=True)
            if diff['type_mismatches']:
                print(f"    - Type mismatches:", flush=True)
                for m in diff['type_mismatches']:
                    print(f"      * {m['column']}: Local {m['local_type']} vs Remote {m['remote_type']}", flush=True)

    if not any([diffs['missing_tables_in_remote'], diffs['missing_tables_in_local'], diffs['table_diffs']]):
        print("\n[✓] Both database structures are identical!", flush=True)
    
    print("\n" + "="*50, flush=True)

if __name__ == "__main__":
    main()
