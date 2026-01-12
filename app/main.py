from flask import Flask, request, jsonify
from .src.image_utils import deserialize_image
from .src.model_utils import load_model
from .src.db_utils import init_tables

app = Flask(__name__)

# Load model once
model = load_model("models/CNN_model.keras")

# Initialize DB tables
init_tables()

@app.route("/")
def home():
    return "Prediction service is running"

@app.route("/predict", methods=["POST"])
def predict():


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)