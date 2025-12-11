import psycopg

# Connect to database (default)
with psycopg.connect(
    dbname="postgres",
    user="postgres",
    password="dsta25-p4ss",
    host="localhost",
    port=5432
) as conn:
    
    # For CREATE DATABASE to work
    conn.autocommit = True

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

    # Make dblink available
        cur.execute("CREATE EXTENSION IF NOT EXISTS dblink;")
    
    # DO block to create database if it doesn't exist
        do_block = """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_database WHERE datname = 'ms3_jokes'
            ) THEN
                PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE ms3_jokes');
            END IF;
        END $$;
        """
        cur.execute(do_block)

# Connect to new database
with psycopg.connect(
    dbname="ms3_jokes",
    user="postgres",
    password="dsta25-p4ss",
    host="localhost",
    port=5432
) as conn:

    with conn.cursor() as cur:

        # Create the table "jokes"
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jokes (
                ID serial PRIMARY KEY,
                JOKE text)
            """)
        
        # Insert joke
        cur.execute(
            "INSERT INTO jokes (JOKE) VALUES (%s)",
            ("A SQL query walks into a bar, walks up to two tables, and asks, “Can I join you?”",))
        
        
        # Select joke and fetch back
        cur.execute("SELECT JOKE FROM jokes")
        print(cur.fetchone()[0])


