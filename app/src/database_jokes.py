import os
import psycopg


# Connect to default postgres DB (used to create other databases)
def connect_default_db():
    return psycopg.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        autocommit=True  # Necessary for CREATE DATABASE to work
    )


# Create database if it doesnt exist
def create_database_if_not_exists(db_name):
    with connect_default_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,)
            )
            exists = cur.fetchone()

            if not exists:
                cur.execute(f"CREATE DATABASE {db_name};")
                print(f'1. Database "{db_name}" created')
            else:
                print(f'1. Database "{db_name}" already exists')


# Connect to "dsta_ms3" database
def connect_db():
    db_name = os.getenv("DB_NAME", "dsta_ms3")
    return psycopg.connect(
        dbname=db_name,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Create "jokes" table in "dsta_ms3" database
def init_jokes_table():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS jokes (
                    ID serial PRIMARY KEY,
                    Joke text
                );
                """
            )
            conn.commit()
            print("2. Table 'jokes' created (if not exists)")


# Insert a joke into "jokes" table
def insert_joke(joke):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO jokes (Joke) VALUES (%s)",
                (joke,)
            )
            conn.commit()
            print(f"3. Inserted joke")


# Fetch a specific joke by its ID from the "jokes" table
def fetch_joke_by_id(joke_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT Joke FROM jokes WHERE ID = %s", (joke_id,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None


# Execute
db_name = os.getenv("DB_NAME", "dsta_ms3")
create_database_if_not_exists(db_name)
init_jokes_table()
insert_joke(
    "A SQL query walks into a bar, walks up to two tables, and asks, "
    "“Can I join you?”"
)

# Fetch joke and print it
joke = fetch_joke_by_id(1)
if joke:
    print(f"My favourite joke is: {joke}")
else:
    print("No joke found with this ID")