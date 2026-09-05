"""Database connection module with graceful fallback."""

import mysql.connector
from mysql.connector import pooling, Error
from config import Config

# Connection pool (created on first use)
_pool = None


def _get_pool():
    """Create connection pool lazily."""
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name="sih_pool",
                pool_size=5,
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
        except Error as e:
            print(f"[DB] Could not create connection pool: {e}")
            return None
    return _pool


def get_connection():
    """Get a connection from the pool. Returns None if DB is unavailable."""
    pool = _get_pool()
    if pool is None:
        return None
    try:
        return pool.get_connection()
    except Error as e:
        print(f"[DB] Connection error: {e}")
        return None


def execute_query(query, params=None, fetch=False, fetch_one=False):
    """Execute a parameterized query safely.

    Args:
        query: SQL query string with %s placeholders
        params: tuple of parameters
        fetch: if True, return all rows
        fetch_one: if True, return single row

    Returns:
        Rows (list/dict) for SELECT, lastrowid for INSERT, rowcount for UPDATE/DELETE.
        None if database is unavailable.
    """
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch or fetch_one:
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            return result

        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount

    except Error as e:
        print(f"[DB] Query error: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def check_connection():
    """Test if database is reachable. Returns True/False."""
    conn = get_connection()
    if conn is None:
        return False
    try:
        conn.ping(reconnect=True)
        return True
    except Error:
        return False
    finally:
        conn.close()
