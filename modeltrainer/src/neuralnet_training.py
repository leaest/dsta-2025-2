#Library for w&b logging
from wandb.integration.keras import WandbMetricsLogger


def train_neuralnet(model, x_train, y_train, batch_size, epochs, optimizer, loss, metrics):
    model.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=metrics
    )

# model.compile(
#     loss="categorical_crossentropy",
#     optimizer="adam",
#     metrics=["accuracy"]
# )

    model.fit(
        x_train, 
        y_train, 
        batch_size=batch_size, 
        epochs=epochs, 
        validation_split=0.1,
        callbacks=[WandbMetricsLogger()] #this logs the metrics
    )
    return model

def save_model(model, path="models/CNN_model.keras"):
    model.save(path)


