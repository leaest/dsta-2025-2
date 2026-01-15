import base64
import requests
from tensorflow import keras
from PIL import Image
import io

print("="*60)
print("Testing Flask Prediction API")
print("="*60)

# Load a real MNIST image
print("\n[1] Loading MNIST dataset...")
(_, _), (x_test, y_test) = keras.datasets.mnist.load_data()

# Get first test image
sample_image = x_test[0]
true_label = y_test[0]

print(f"[2] Selected test image - True label: {true_label}")

# Convert to PNG bytes
img = Image.fromarray(sample_image)
buffer = io.BytesIO()
img.save(buffer, format='PNG')
img_bytes = buffer.getvalue()

# Save image so you can see it
img.save('test_digit.png')
print(f"[3] Saved image as 'test_digit.png'")

# Encode to base64
base64_image = base64.b64encode(img_bytes).decode('utf-8')
base64_image = f"data:image/png;base64,{base64_image}"

# Send to Flask API
print("\n[4] Sending POST request to http://localhost:5000/predict...")
response = requests.post(
    "http://localhost:5000/predict",
    json={"image": base64_image},
    headers={"Content-Type": "application/json"}
)

print(f"[5] Response Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print("\n" + "="*60)
    print("✓ SUCCESS!")
    print("="*60)
    print(f"Predicted Digit: {data['prediction']}")
    print(f"True Label:      {true_label}")
    print(f"Match:           {'✓ CORRECT' if data['prediction'] == true_label else '✗ INCORRECT'}")
    print("="*60)
else:
    print(f"\n✗ ERROR: {response.text}")