import os
import json
import base64
import time
import numpy as np
from flask import Flask, request, jsonify
from src.db_utils import init_tables, create_database_if_not_exists, connect_milestone_db, write_to_db, read_from_db
from src.image_utils import deserialize_base_image
from src.model_utils import load_model
import psycopg2


app = Flask(__name__)

# Initialize DB table
create_database_if_not_exists()
init_tables()

# Load model
model = load_model()

# Flask application
@app.route("/")
def home():
    return '''
    <h1>Welcome to our App!</h1>
    <h2>The Website to upload an image would be here</h2>
     <ul>
        <li>POST /predict - Submit an image for classification</li>
        <li>GET /read - View recent predictions</li>
    </ul>
    '''

## Retrieves data form the PostgreSQL database
@app.route('/read', methods=['GET'])
def read():
    """Get recent predictions"""
    try:
        query = """
            SELECT p.id, p.input_id, p.predicted_label 
            FROM predictions p 
            ORDER BY p.id DESC 
            LIMIT 10;
        """
        result = read_from_db(query)
        
        predictions = []
        for row in result:
            predictions.append({
                'id': row[0],
                'input_id': row[1],
                'predicted_label': row[2]
            })
        
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


## Allows clients to send data to be inserted into the database
@app.route("/predict", methods=["POST"])
def predict():
    """Predict digit from image"""
    data = request.get_json()
    
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400
    
    try:
        # Decode image
        image_data = data["image"]
        
        # Handle data URI prefix (from browsers)
        if "base64," in image_data:
            image_data = image_data.split("base64,")[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Deserialize using new function
        image = deserialize_base_image(image_bytes)
        image = image.reshape(1, 28, 28, 1).astype("float32")
        
        # Predict
        prediction = model.predict(image)
        predicted_label = int(np.argmax(prediction))
        
        # Save to database using two-table structure
        conn = connect_milestone_db()
        cur = conn.cursor()
        
        # Insert into input_data and get ID
        cur.execute(
            "INSERT INTO input_data (image) VALUES (%s) RETURNING id;",
            (psycopg2.Binary(image_bytes),)
        )
        input_id = cur.fetchone()[0]
        
        # Insert into predictions with foreign key
        cur.execute(
            "INSERT INTO predictions (input_id, predicted_label) VALUES (%s, %s);",
            (input_id, predicted_label)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"prediction": predicted_label})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)