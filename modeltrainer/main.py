# Import libraries to train the model
import os
import sys
import numpy as np

# To be able to use W&B we need wandb library and functions from wandb.keras
import wandb
from wandb.integration.keras import WandbMetricsLogger, WandbModelCheckpoint

# Import from src
from src.data_prep import load_data
from src.neuralnet_architecture import build_neuralnet
from src.neuralnet_training import train_neuralnet, save_model
from src.neuralnet_loading import load_trained_model
from src.neuralnet_predicion import predict_sample

MODEL_PATH = "/app/models/CNN_model.keras"   # match docker-compose volume

# Start a run, tracking hyperparameters
wandb.init(
    # set the wandb project where this run will be logged
    project="milestone4_modeltrainer",
    entity="DSTA-2025",


    # track hyperparameters and run metadata with wandb.config
    config={
        "layer_1": 512,
        "activation_1": "relu",
        "dropout": 0.3,
        "layer_2": 10,
        "activation_2": "softmax",
        "optimizer": "adam",
        "loss": "categorical_crossentropy",
        "metric": "accuracy",
        "epochs": 8,
        "batch_size": 256
    }
)

# [optional] use wandb.config as your config
config = wandb.config

# Check if model already exists

if os.path.exists(MODEL_PATH):
    print(f"Model already exists at {MODEL_PATH}. Skipping training.")
    model = load_trained_model(MODEL_PATH)
    print("Model loaded successfully!")
    sys.exit(0)  

else:
    print(f"No model found at {MODEL_PATH}. Training will start now.")


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
model = train_neuralnet(
    model,
    x_train,
    y_train,
    batch_size=config.batch_size,
    epochs=config.epochs,
    optimizer=config.optimizer,
    loss=config.loss,
    metrics=[config.metric]
)
print("Model trained successfully!")


## Evaluate trained model
score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Log metrics to w&b
wandb.log({
    "test_loss": score[0],
    "test_accuracy": score[1]
})


# Save model
# Change path with: path = "models/Name_your_model.keras"
# and save_model(model, path)
save_model(model)
print("Model saved successfully!")


# Load model
# Changed path: load_trained_model(path)
model = load_trained_model()
print("Model loaded successfully!")


# Predict
pred_class, true_class = predict_sample(model, x_test[:10], y_test[:10])
table = np.column_stack((pred_class, true_class))
print("Pred.  True")
print(table)

# Save predictions to file
y_pred = np.argmax(model.predict(x_test), axis=1)
np.savetxt("predictions.csv", np.column_stack((y_test, y_pred)), delimiter=",", header="true,pred", comments="")

# Upload file to W&B
wandb.save("predictions.csv")
wandb.finish()
