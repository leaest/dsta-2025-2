import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import json

# Load config form JSON (saved outside of app hence this path)
with open(os.path.join(os.path.dirname(__file__), '../config.json'), 'r') as f:
    config = json.load(f)

db_config = config['postgres']

def connect_default_db():
    """Connect to the default 'postgres' database to create new DBs."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname="postgres"
    )

def create_database_if_not_exists():
    db_name = os.getenv("DB_NAME")

    conn = connect_default_db()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}';")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    cur.close()
    conn.close()


def connect_milestone_db():
    """Connect to db_milestone5"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )


def init_tables():
    conn = connect_milestone_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS input_data (
            id SERIAL PRIMARY KEY,
            image BYTEA NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            input_id INTEGER REFERENCES input_data(id),
            predicted_label INTEGER NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# Write function
def write_to_db(query, params=None):
    conn = connect_milestone_db()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

# Read function
def read_from_db(query, params=None):
    conn = connect_milestone_db()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result