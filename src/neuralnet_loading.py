from keras.models import load_model


def load_trained_model(path="models/CNN_model.keras"):
    model = load_model(path)
    return model