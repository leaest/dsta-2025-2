import numpy as np
import pickle
from PIL import Image
import io

def serialize_image(img_array):
    return pickle.dumps(img_array)

def deserialize_image(data):
    return pickle.loads(data)


# New method for deserializing images from base64
def deserialize_base_image(data):
    img = Image.open(io.BytesIO(data))
    img = img.convert('L')
    img = img.resize((28, 28))
    image_array = np.array(img)
    image_array = image_array.astype('float32') / 255.0
    return image_array