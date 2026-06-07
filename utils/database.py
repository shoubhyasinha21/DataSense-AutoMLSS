import sqlite3
import time
from datetime import datetime

DB_NAME = "datasense.db"


def get_connection():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=30,
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA busy_timeout=30000;")
    return conn


def execute_query(query, params=(), fetch=False, retries=5):
    for attempt in range(retries):
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(query, params)

            data = cur.fetchall() if fetch else None

            conn.commit()
            return data

        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower():
                time.sleep(1)
            else:
                raise e

        finally:
            if conn:
                conn.close()

    raise sqlite3.OperationalError("Database is locked after multiple retries.")


def init_db():
    execute_query("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        plan TEXT DEFAULT 'free',
        is_admin INTEGER DEFAULT 0,
        created_at TEXT,
        last_login TEXT
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        login_time TEXT
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS dataset_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        dataset_name TEXT,
        task_type TEXT,
        best_model TEXT,
        created_at TEXT
    )
    """)

    execute_query("""
    CREATE TABLE IF NOT EXISTS training_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        target_column TEXT,
        task_type TEXT,
        best_model TEXT,
        score REAL,
        timestamp TEXT
    )
    """)


def create_user(name, email, password, is_admin=0, plan="free"):
    execute_query("""
    INSERT INTO users (
        name, email, password, plan, is_admin, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        password,
        plan,
        is_admin,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))


def create_admin_if_not_exists(name, email, password):
    user = execute_query(
        "SELECT id FROM users WHERE email=?",
        (email,),
        fetch=True
    )

    if not user:
        create_user(
            name=name,
            email=email,
            password=password,
            is_admin=1,
            plan="premium"
        )


def login_user(email, password):
    user = execute_query("""
    SELECT
        id,
        name,
        email,
        password,
        plan,
        is_admin,
        created_at,
        last_login
    FROM users
    WHERE email=? AND password=?
    """, (email, password), fetch=True)

    if not user:
        return None

    user = user[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    execute_query("""
    UPDATE users
    SET last_login=?
    WHERE email=?
    """, (now, email))

    execute_query("""
    INSERT INTO login_history (
        user_email, login_time
    )
    VALUES (?, ?)
    """, (email, now))

    return user


def logout_user():
    pass


def save_history(user_email, dataset_name, task_type, best_model):
    execute_query("""
    INSERT INTO dataset_history (
        user_email,
        dataset_name,
        task_type,
        best_model,
        created_at
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_email,
        dataset_name,
        task_type,
        best_model,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))


def load_history():
    return execute_query("""
    SELECT
        user_email,
        dataset_name,
        task_type,
        best_model,
        created_at
    FROM dataset_history
    ORDER BY created_at DESC
    """, fetch=True)


def save_training_run(email, target_column, task_type, best_model, score):
    execute_query("""
    INSERT INTO training_history (
        email,
        target_column,
        task_type,
        best_model,
        score,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email,
        target_column,
        task_type,
        best_model,
        score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))


def get_training_history():
    return execute_query("""
    SELECT
        email,
        target_column,
        task_type,
        best_model,
        score,
        timestamp
    FROM training_history
    ORDER BY timestamp DESC
    """, fetch=True)


def total_users():
    result = execute_query("SELECT COUNT(*) FROM users", fetch=True)
    return result[0][0]


def total_logins():
    result = execute_query("SELECT COUNT(*) FROM login_history", fetch=True)
    return result[0][0]


def total_admins():
    result = execute_query("SELECT COUNT(*) FROM users WHERE is_admin=1", fetch=True)
    return result[0][0]


def total_premium_users():
    result = execute_query("SELECT COUNT(*) FROM users WHERE plan='premium'", fetch=True)
    return result[0][0]


def get_all_users():
    return execute_query("""
    SELECT
        id,
        name,
        email,
        plan,
        is_admin,
        created_at,
        last_login
    FROM users
    ORDER BY id DESC
    """, fetch=True)


def get_login_history():
    return execute_query("""
    SELECT
        user_email,
        login_time
    FROM login_history
    ORDER BY login_time DESC
    """, fetch=True)


def update_user_plan(email, plan):
    execute_query("""
    UPDATE users
    SET plan=?
    WHERE email=?
    """, (plan, email))


def delete_user(email):
    execute_query("DELETE FROM users WHERE email=?", (email,))

def clear_login_history():
    execute_query("DELETE FROM login_history")    

    
  