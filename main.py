import numpy as np

from src.data_prep import load_data
from src.neuralnet_architecture import build_neuralnet
from src.neuralnet_training import train_neuralnet, save_model
from src.neuralnet_loading import load_trained_model
from src.neuralnet_predicion import predict_sample


# Load data
x_train, y_train, x_test, y_test = load_data()
print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)
print("x_test shape:", x_test.shape)
print("y_test shape:", y_test.shape)


# Build model
model = build_neuralnet()
model.summary()


# Train model
model = train_neuralnet(model, x_train, y_train)


## Evaluate trained model
score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])


# Save model
path = "models/CNN_model.keras"
save_model(model, path)
print(f"Model saved successfully at: {path}")


# Load model
model = load_trained_model(path)
print(f"Model loaded successfully from: {path}")


# Predict
pred_class, true_class = predict_sample(model, x_test[:10], y_test[:10])
table = np.column_stack((pred_class, true_class))
print("Pred.  True")
print(table)