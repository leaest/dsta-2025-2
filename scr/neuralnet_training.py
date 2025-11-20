def train_neuralnet(model, x_train, y_train, batch_size=128, epochs=15):
    model.compile(
        loss="categorical_crossentropy",
        optimizer="adam",
        metrics=["accuracy"]
    )
    model.fit(
        x_train, 
        y_train, 
        batch_size=batch_size, 
        epochs=epochs, 
        validation_split=0.1
    )
    return model

def save_model(model, filepath="models/CNN_model.keras"):
    model.save(filepath)
    return filepath


