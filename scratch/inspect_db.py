from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not found")
    exit(1)

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

def get_table_info():
    tables = inspector.get_table_names()
    for table_name in tables:
        print(f"\n--- TABLE: {table_name} ---")
        columns = inspector.get_columns(table_name)
        for column in columns:
            name = column['name']
            type_ = column['type']
            nullable = column['nullable']
            default = column.get('default')
            print(f"  Column: {name:20} Type: {str(type_):20} Nullable: {nullable} Default: {default}")

        pk = inspector.get_pk_constraint(table_name)
        print(f"  Primary Key: {pk['constrained_columns']}")

        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            print(f"  Foreign Key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

if __name__ == "__main__":
    try:
        report_path = os.path.join(os.path.dirname(__file__), "db_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            tables = inspector.get_table_names()
            for table_name in tables:
                f.write(f"\n--- TABLE: {table_name} ---\n")
                columns = inspector.get_columns(table_name)
                for column in columns:
                    name = column['name']
                    type_ = column['type']
                    nullable = column['nullable']
                    f.write(f"  Column: {name:20} Type: {str(type_):20} Nullable: {nullable}\n")

                pk = inspector.get_pk_constraint(table_name)
                f.write(f"  Primary Key: {pk['constrained_columns']}\n")

                fks = inspector.get_foreign_keys(table_name)
                for fk in fks:
                    f.write(f"  Foreign Key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}\n")
        print(f"Reporte guardado en: {report_path}")
    except Exception as e:
        print(f"Error: {e}")
