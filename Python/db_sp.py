import time
from sqlalchemy import text
from db_config import get_engine

def run_method_db_sp(method_name='DB_SP'):
    engine = get_engine()
    print(f"Executing Method 2: {method_name} (SQL Stored Procedure)")

    start_time = time.time()

    with engine.connect() as conn:
        try:
            conn.execute(text("EXEC dbo.Calculate_Dynamic_DB_SP"))
            conn.commit()
        except Exception as e:
            print(f"❌ Error during DB_SP execution: {e}")
            raise

    duration = time.time() - start_time

    with engine.connect() as conn:
        total_rows_processed = conn.execute(
            text("SELECT COUNT(*) FROM t_results WHERE method = :method"),
            {"method": method_name}
        ).scalar()

    return duration, total_rows_processed