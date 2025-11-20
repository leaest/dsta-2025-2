from scr.data_prep import load_data
from scr.neuralnet_architecture import build_neuralnet
from scr.neuralnet_training import train_neuralnet, save_model


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


# Save model
path = save_model(model, "models/CNN_model.keras")
print(f"Model saved at: {path}")
