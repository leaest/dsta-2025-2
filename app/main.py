from flask import Flask, request, jsonify
import json
import base64
import numpy as np

from app.src.image_utils import deserialize_image
from app.src.model_utils import load_model
from app.src.db_utils import init_tables, write_to_db, read_from_db

app = Flask(__name__) #OK


# Load configuration form JSON file
with open("config.json", "r") as f:
    config = json.load(f)

db_table = config["postgres"]["db_table"]

# Load model
model = load_model()

# Initialize DB table
init_tables()

# Flask application
#OK
@app.route("/")
def home():
    return '<h1>Welcome to our App!<h1>'

@app.route('/read', methods=['GET'])
def read():
    try:
        query = f"SELECT * FROM {db_table};"
        result = read_from_db(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

        true_label = data.get("label")  # optional

        # Store in DB
        query = f"""
            INSERT INTO {db_table} (image, label, pred_label)
            VALUES (%s, %s, %s);
        """
        write_to_db(query, (image_bytes, true_label, predicted_label))

        return jsonify({"prediction": predicted_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#OK (host and port in JSON file)
if __name__ == "__main__":
    app.run(debug=True)