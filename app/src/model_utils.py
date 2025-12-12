import tensorflow as tf

MODEL_PATH = "/app/models/CNN_model.keras"

import time
import os
import tensorflow as tf

MODEL_PATH = "/app/models/CNN_model.keras"

def load_model():
    print(f"Loading model from: {MODEL_PATH}")

    # Wait until the model file exists
    while not os.path.exists(MODEL_PATH):
        print("Model not found yet. Waiting for trainer to finish...")
        time.sleep(60)

    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
    return model

