import pandas as pd
import numpy as np
import time
from sqlalchemy import text
from db_config import get_engine

num_records = 1_000_000
CHUNK_SIZE = 50000

engine = get_engine()

start_time = time.time()

df = pd.DataFrame({
    'a': np.random.uniform(0.1, 100, num_records),
    'b': np.random.uniform(0.1, 100, num_records),
    'c': np.random.uniform(0.1, 100, num_records),
    'd': np.random.uniform(0.1, 100, num_records)
})

try:
    df.to_sql('t_data',
              con=engine,
              if_exists='append',
              index=False,
              chunksize=CHUNK_SIZE)

    duration_data = time.time() - start_time
    print(f"✅ 1,000,000 רשומות הוכנסו ל-t_data בהצלחה! (זמן: {duration_data:.2f} שניות)")
except Exception as e:
    print(f"❌ שגיאה בהכנסת נתוני t_data: {e}")

insert_values = [
    ('a + b * c', None, None),
    ('a - d', None, None),
    ('a * b', 'a > 5', 'a + b'),
    ('c + 1', 'd < 0', 'd - 1'),
    ('POWER(a, b)', None, None),
    ('SQRT(a * b)', 'a > 0', '0'),
    ('a * (b + c)', 'b > 3', 'a + c'),
    ('(a + b + c) / d', 'd != 0', '0'),
    ('a * b * c', 'a < 10', 'a + b + c'),
    ('d - a', 'd > a', 'a - d'),
]

rows = [
    {
        "targil": r[0],
        "tnai": r[1],
        "false_targil": r[2]
    }
    for r in insert_values
]

query = text("""
INSERT INTO dbo.t_targil (targil, tnai, false_targil)
VALUES (:targil, :tnai, :false_targil)
""")

try:
    with engine.connect() as conn:
        conn.execute(query, rows)
        conn.commit()
except Exception as e:
    print(f"❌ שגיאה בהכנסת נתוני t_targil: {e}")
