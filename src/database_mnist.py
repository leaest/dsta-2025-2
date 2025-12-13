import os
import psycopg
import keras
import numpy as np
from PIL import Image
import io

# Connect to postgres DB
def connect_default_db():
    return psycopg.connect(
        dbname="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        autocommit=True
    )

# Create database if it doesnt exist
def create_database_if_not_exists():
    db_name = os.getenv("DB_NAME")

    with connect_default_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s;",
                (db_name,)
            )
            exists = cur.fetchone()

            if not exists:
                cur.execute(f"CREATE DATABASE {db_name};")
                print(f"1. Database '{db_name}' created.")
            else:
                print(f"1. Database '{db_name}' already exists.")


# Connect to "ms3_mnist" database
def connect_mnist_db():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"), # ms3_mnist
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Create "mnist" table in "ms3_mnist" database
def init_table():
    with connect_mnist_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mnist (
                    id SERIAL PRIMARY KEY,
                    image BYTEA NOT NULL,
                    label INTEGER NOT NULL
                );
            """)
            conn.commit()
            print("2. Table 'mnist' created (if not exists).")


def insert_samples(image_list, label_list):
    with connect_mnist_db() as conn:
        with conn.cursor() as cur:
            for img_bytes, label in zip(image_list, label_list):
                cur.execute(
                    "INSERT INTO mnist (image, label) VALUES (%s, %s)",
                    (img_bytes, label)
                )
            conn.commit()
            print(f"3. Inserted samples")


def get_random_image():
    with connect_mnist_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT image, label FROM mnist ORDER BY RANDOM() LIMIT 1"
            )
            print(f"4. Got random image")
            return cur.fetchone()
            
        


# Load and process mnist data
num_classes = 10
num_sample = 10

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_test = x_test.astype("float32") / 255
x_test = np.expand_dims(x_test, -1)
y_test = keras.utils.to_categorical(y_test, num_classes)

image_list = []
label_list = []

for i in range(num_sample):
    sample_image = x_test[i]
    sample_label = y_test[i]

    # Convert back
    img = Image.fromarray((sample_image.squeeze() * 255).astype(np.uint8))

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    image_list.append(image_bytes)
    label_list.append(np.argmax(sample_label))


# Execute
create_database_if_not_exists()
init_table()
insert_samples(image_list, label_list)

retrieved_bytes, retrieved_label = get_random_image()

print("Label:", retrieved_label)

img = Image.open(io.BytesIO(retrieved_bytes))
name_img = "retrieved_image.png"
img.save(name_img)
print(f'Image saved as: "{name_img}"')
img.show()
