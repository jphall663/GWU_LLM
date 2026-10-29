"""Synthetic sales data and the shared SQLite execution boundary for Lecture 6.

Copyright (c) Patrick Hall (jphall@gwu.edu), 2026-27. MIT License.
Model decisions and orchestration remain visible in text_to_sql.ipynb.
"""
from pathlib import Path
from contextlib import closing
import sqlite3
from time import monotonic

SCHEMA = """customers(customer_id INTEGER PRIMARY KEY, region TEXT)
orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers,
       order_date TEXT, status TEXT)
order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER REFERENCES orders,
            quantity INTEGER, unit_price_cents INTEGER, discount_cents INTEGER)
"""
DEFINITIONS = """Synthetic sales data; all money is USD, stored as integer cents.
Reference date: 2026-10-15. Last quarter: 2026-07-01 <= order_date < 2026-10-01.
Net sales = SUM(quantity * unit_price_cents - COALESCE(discount_cents, 0)) / 100.0.
Discount is the TOTAL discount per line, not a unit discount. NULL discount means zero.
Only orders with status = 'completed' count. Exclude cancelled and pending orders.
Join customers to orders by customer_id; orders to order_items by order_id.
Aggregate item values, not order counts; avoid multiplying totals across joins.
NULL region is reported as 'Unknown'. Order region results by net sales descending.
'Best customers' is ambiguous: ask for a metric and time window before querying.
Profit is unavailable: no cost data. Writes and private data are prohibited.
"""
ALLOWED_TABLES = {'customers', 'orders', 'order_items'}
ALLOWED_FUNCTIONS = {'sum', 'count', 'avg', 'min', 'max', 'round', 'coalesce',
                     'ifnull', 'nullif', 'abs', 'date', 'strftime', 'julianday',
                     'lower', 'upper', 'length'}


def build_database(path: Path):
    """Create a deterministic teaching fixture; never accepts model-written DDL."""
    with sqlite3.connect(path) as con:
        con.executescript('''
        CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, region TEXT);
        CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER
          REFERENCES customers, order_date TEXT, status TEXT);
        CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER
          REFERENCES orders, quantity INTEGER, unit_price_cents INTEGER, discount_cents INTEGER);
        CREATE TABLE private_notes(note TEXT);
        INSERT INTO private_notes VALUES ('Synthetic restricted record; never send to the model.');
        INSERT INTO customers VALUES (1,'East'),(2,'West'),(3,'East'),(4,'South'),(5,NULL);
        INSERT INTO orders VALUES
          (101,1,'2026-07-01','completed'),(102,2,'2026-08-12','completed'),
          (103,3,'2026-09-30','completed'),(104,4,'2026-09-10','cancelled'),
          (105,1,'2026-06-30','completed'),(106,2,'2026-10-01','completed'),
          (107,4,'2026-08-20','completed'),(108,5,'2026-09-05','completed'),
          (109,2,'2026-08-21','pending');
        INSERT INTO order_items VALUES
          (1,101,2,10000,1000),(2,101,1,5000,NULL),(3,102,3,10000,0),
          (4,103,1,20000,2000),(5,104,10,10000,0),(6,105,1,90000,0),
          (7,106,1,80000,0),(8,107,2,5000,1000),(9,108,1,4000,NULL),
          (10,109,10,10000,0);
        ''')


def authorize(action, arg1, arg2, database, trigger):
    """Default deny: SQL syntax alone never grants access."""
    if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_RECURSIVE):
        return sqlite3.SQLITE_OK
    # SQLite may omit the database name for COUNT(*) reads (empty column name).
    if action == sqlite3.SQLITE_READ and arg1 in ALLOWED_TABLES and database in ('main', None):
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_FUNCTION and arg2 in ALLOWED_FUNCTIONS:
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def run_query(path: Path, sql: str, *, row_cap=50, timeout_s=0.2):
    """Execute one statement using engine authorization and a cooperative deadline.

    The extra fetched row detects truncation. The caller must not treat a truncated
    result as a full answer. The progress callback is a teaching resource limit,
    not an OS sandbox or a hard real-time guarantee.
    """
    if not isinstance(sql, str) or not sql.strip() or len(sql) > 10_000:
        return {'ok': False, 'error': 'Expected one SQL statement of 1–10,000 characters.'}
    start = monotonic()
    try:
        # A fresh connection prevents statement-cache authorization surprises.
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)) as con:
            con.execute('PRAGMA query_only=ON')
            con.execute('PRAGMA trusted_schema=OFF')
            con.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 100_000)
            con.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 10_000)
            con.set_authorizer(authorize)
            con.set_progress_handler(lambda: int(monotonic() - start >= timeout_s), 100)
            cursor = con.execute(sql)  # execute rejects multiple statements; no executescript here.
            rows = cursor.fetchmany(row_cap + 1)
            columns = [d[0] for d in cursor.description]
        return {'ok': True, 'columns': columns, 'rows': [list(r) for r in rows[:row_cap]],
                'truncated': len(rows) > row_cap, 'latency_ms': round(1000*(monotonic()-start), 2)}
    except sqlite3.Error as exc:
        # Only synthetic data are used. Redact database errors before production logging.
        return {'ok': False, 'error': str(exc), 'latency_ms': round(1000*(monotonic()-start), 2)}
