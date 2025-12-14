import numpy as np
from tensorflow.keras.datasets import mnist

from src.db_utils import create_database_if_not_exists, init_tables, connect_milestone_db
from src.model_utils import load_model
from src.image_utils import serialize_image, deserialize_image

# 1. Ensure database exists
create_database_if_not_exists()

# 2. Ensure tables exist
init_tables()

# 3. Load model
model = load_model()

# 4. Load one sample image
(_, _), (x_test, y_test) = mnist.load_data()
sample_img = x_test[0]
true_label = y_test[0]

# Preprocess for Neural Net
sample_img_processed = sample_img.reshape(1, 28, 28, 1).astype("float32") / 255

# Serialize image
img_serialized = serialize_image(sample_img)

# Insert into DB
conn = connect_milestone_db()
cur = conn.cursor()

cur.execute(
    "INSERT INTO input_data (image) VALUES (%s) RETURNING id;",
    (img_serialized,)
)
input_id = cur.fetchone()[0]
conn.commit()

# Predict
pred = model.predict(sample_img_processed)
pred_label = int(np.argmax(pred))

# Store prediction with foreign key
cur.execute(
    "INSERT INTO predictions (input_id, predicted_label) VALUES (%s, %s);",
    (input_id, pred_label)
)
conn.commit()

print("Saved input id:", input_id)
print("Predicted:", pred_label, "| True:", true_label)

cur.close()
conn.close()
