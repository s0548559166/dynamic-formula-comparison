from engine_safe_ast import run_method_safe_ast
from db_sp import run_method_db_sp

def main():
    print("--- Starting Project: Dynamic Formula Calculation ---")
    try:
        total_rows_method_1 = run_method_safe_ast()
        print(f"✅ Method 'safe_ast' finished. Total rows inserted to t_results: {total_rows_method_1}")
    except Exception as e:
        print(f"❌ Error during 'safe_ast' method execution: {e}")

    try:
        total_duration_db, total_rows_db = run_method_db_sp()
        print(f"✅ Method 'DB_SP' finished. Total rows inserted: {total_rows_db}. Total time: {total_duration_db:.4f} seconds.")
    except Exception as e:
        print(f"❌ DB_SP failed.")


    print("\nProject execution finished. Check t_results and t_log for data.")


if __name__ == "__main__":
    main()