import os
import numpy as np
from tensorflow import keras
from keras import layers
from keras.preprocessing import image
from pathlib import Path
import joblib


def load_img(img_path) -> str:
    """loads the image from image filepath"""
    img_path = Path(img_path)
    img = image.load_img(img_path)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    return img


def preprocess_layers(img):
    """keras layers to transform image"""
    # set image size height, width (default=256x256)
    image_size = (256, 256) 

    # define image preprocessing layers pipeline
    image_preprocessing_layers = [  
        # resizing layer
        keras.layers.Resizing(
            image_size[0], # height in pixels
            image_size[1], # width in pixels
            interpolation = 'lanczos5',
            crop_to_aspect_ratio = True,
        ),
        # rescaling layer
        keras.layers.Rescaling(
            1./255
        )
    ]
    
    # apply all layers to image
    for layer in image_preprocessing_layers:
        img = layer(img)
    return img


def preprocess_image(img_path):
     """apply loading and layer functions"""
     img = load_img(img_path)
     preprocessed_image = preprocess_layers(img)
     return preprocessed_image

   
def make_prediction(model_path, preprocessed_image):
    """make prediction using preprocessed data"""
    # load model 
    model = joblib.load(model_path)

    # make prediction
    prediction = model.predict(preprocessed_image)

    # store predictions into percentages of benign and malignant
    benign_pred = round(100 * (1 - prediction[0][0]),2)
    malignant_pred = 100 - benign_pred

    # return predictions
    return (f"{benign_pred:.2f}% Benign, {malignant_pred:.2f}% Malignant")

