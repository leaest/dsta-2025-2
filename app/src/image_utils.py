import numpy as np
import pickle

def serialize_image(img_array):
    return pickle.dumps(img_array)

def deserialize_image(data):
    return pickle.loads(data)
