import psycopg
import keras
import numpy as np
from PIL import Image
import io


num_classes = 10
input_shape = (28, 28, 1)

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_test = x_test.astype("float32") / 255
x_test = np.expand_dims(x_test, -1)
y_test = keras.utils.to_categorical(y_test, num_classes)

sample_image = x_test[50]
sample_label = y_test[50]

img = Image.fromarray((sample_image.squeeze() * 255).astype(np.uint8))
buffer = io.BytesIO()
img.save(buffer, format="PNG")
image_bytes = buffer.getvalue()


image_data = (sample_image * 255).astype(np.uint8).tobytes()
label_data = np.argmax(sample_label)

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
                SELECT 1 FROM pg_database WHERE datname = 'ms3_mnist'
            ) THEN
                PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE ms3_mnist');
            END IF;
        END $$;
        """
        cur.execute(do_block)

# Connect to new database
with psycopg.connect(
    dbname="ms3_mnist",
    user="postgres",
    password="dsta25-p4ss",
    host="localhost",
    port=5432
) as conn:

    with conn.cursor() as cur:

        # Create the table "mnist"
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mnist (
                ID serial PRIMARY KEY,
                Image bytea,
                Label integer)
            """)
        
        # Insert  Data
        cur.execute(
            "INSERT INTO mnist (Image, Label) VALUES (%s,%s)",
            (image_bytes, label_data,))
        
