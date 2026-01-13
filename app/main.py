import os
import json
import base64
import time
import numpy as np
from flask import Flask, request, jsonify
from .src.db_utils import init_tables, create_database_if_not_exists, connect_milestone_db, write_to_db, read_from_db
from .src.image_utils import deserialize_image
from .src.model_utils import load_model


app = Flask(__name__)


# Load configuration form JSON file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

db_table = config["postgres"]["db_table"]
host = config["postgres"]["host"]
port = config["postgres"]["port"]

# Initialize DB table
create_database_if_not_exists()
init_tables()

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/CNN_model.keras')

def model_loading_process(path):
    while not os.path.exists(path):
        print(f"Model not in {path}, Waiting 10 seconds...")
        time.sleep(10)
    return load_model(path)

model = model_loading_process(MODEL_PATH)
print("Model loaded!")

# Flask application
@app.route("/")
def home():
    return '<h1>Welcome to our App!<h1>'

## Retrieves data form the PostgreSQL database (not sure if we need this and if JSON format is the right choice)
@app.route('/read', methods=['GET'])
def read():
    try:
        query = f"SELECT * FROM {db_table};"
        result = read_from_db(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

## Allows clients to send data to be inserted into the database
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Decode image
        image_bytes = base64.b64decode(data["image"])
        image = deserialize_image(image_bytes)
        image = image.reshape(1, 28, 28, 1).astype("float32") / 255

        # Predict
        prediction = model.predict(image)
        predicted_label = int(np.argmax(prediction))

        true_label = data.get("label")  # not necessary i think?

        # Store in DB
        query = f"INSERT INTO {db_table} (image, label, pred_label) VALUES (%s, %s, %s);"
        write_to_db(query, (image_bytes, true_label, predicted_label))

        return jsonify({"prediction": predicted_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# deebug=True enables auto-reload (disable for production)