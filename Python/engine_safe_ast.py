import ast
import math
import time
from typing import Dict, Any, List
from sqlalchemy import text
from db_config import get_engine

SAFE_FUNCS = {
    'sqrt': math.sqrt,
    'abs': abs,
    'min': min,
    'max': max,
    'ln': math.log,
    'log': math.log,
    'pow': pow
}

ALLOWED_NODES = {
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
    ast.Name, ast.Load, ast.Call, ast.IfExp, ast.Compare,
    ast.And, ast.Or, ast.Not, ast.BoolOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE
}

def is_safe(node: Any) -> bool:
    if type(node) not in ALLOWED_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not is_safe(child):
            return False
    return True

class SafeFormula:
    def __init__(self, expr_text: str):
        expr = expr_text.replace('^', '**')

        try:
            parsed = ast.parse(expr, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"Syntax error in expr: {expr_text}") from e

        if not is_safe(parsed):
            raise ValueError("Expression contains unsafe nodes.")

        self.code = compile(parsed, '<expr>', 'eval')
        self.expr = expr_text

    def eval(self, vars: Dict) -> float:
        safe_globals = {'__builtins__': None}
        safe_globals.update(SAFE_FUNCS)

        try:
            return eval(self.code, safe_globals, vars)
        except ZeroDivisionError:
            return 0.0
        except ValueError:
            return float('nan')
        except Exception:
            return float('nan')

def get_safe_field(row, field_name: str) -> str:
    try:
        value = getattr(row, field_name)
    except AttributeError:
        return ''

    if value is None:
        return ''

    if isinstance(value, str):
        return value.strip()

    return str(value).strip()

def run_method_safe_ast(method_name: str = 'safe_ast') -> int:

    engine = get_engine()
    total_rows_processed = 0

    with engine.connect() as conn:

        targil_rows = conn.execute(
            text("SELECT targil_id, targil, tnai, false_targil FROM dbo.t_targil")
        ).fetchall()

        print("Reading all data records from DB...")
        data_records = conn.execute(
            text("SELECT data_id, a, b, c, d FROM dbo.t_data")
        ).fetchall()
        print(f"Finished reading {len(data_records)} records.")

        for targil_row in targil_rows:
            targil_id = targil_row.targil_id

            formula_main = get_safe_field(targil_row, 'targil')
            tnai = get_safe_field(targil_row, 'tnai')
            formula_false = get_safe_field(targil_row, 'false_targil')

            if tnai and tnai.upper() not in ('NULL', ''):
                formula_to_run = f"({formula_main}) if ({tnai}) else ({formula_false})"
            else:
                formula_to_run = formula_main
            print(f"\n--- Calculating Targil ID: {targil_id} ({formula_to_run}) ---")

            try:
                formula = SafeFormula(formula_to_run)
            except ValueError as e:
                print(f"❌ ERROR: Targil {targil_id} failed AST compilation: {e}. Skipping.")
                continue

            start_time = time.time()
            results_to_insert: List[Dict[str, Any]] = []

            for r in data_records:
                vars_to_eval = {
                    "a": r.a if r.a is not None else 0.0,
                    "b": r.b if r.b is not None else 0.0,
                    "c": r.c if r.c is not None else 0.0,
                    "d": r.d if r.d is not None else 0.0,
                }

                val = formula.eval(vars_to_eval)

                result_value = float(val)
                if math.isnan(result_value) or math.isinf(result_value):
                    result_value = None

                results_to_insert.append({
                    "targil_id": targil_id,
                    "data_id": r.data_id,
                    "result": result_value,
                    "method": method_name
                })

            duration = time.time() - start_time

            conn.execute(
                text("""
                    INSERT INTO dbo.t_results (targil_id, data_id, result, method)
                    VALUES (:targil_id, :data_id, :result, :method)
                """),
                results_to_insert
            )

            conn.execute(
                text("""
                    INSERT INTO dbo.t_log (targil_id, method, time_run)
                    VALUES (:targil_id, :method, :run_time)
                """),
                {"targil_id": targil_id, "method": method_name, "run_time": duration}
            )

            print(f"Calculation complete in {duration:.4f} seconds. Rows: {len(results_to_insert)}")
            total_rows_processed += len(results_to_insert)

        conn.commit()
    return total_rows_processed


