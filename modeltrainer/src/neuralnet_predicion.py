import numpy as np


def predict_sample(model, x_sample, y_true):
    pred = model.predict(x_sample)
    pred_class = np.argmax(pred, axis=1)
    true_class = np.argmax(y_true, axis=1)
    return pred_class, true_class