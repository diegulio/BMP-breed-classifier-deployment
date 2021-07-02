import json
import numpy as np
import os
from tensorflow.keras.models import load_model  
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import pickle as pkl

__model = None
__class_indices = None

def load_model_():
    global __model
    global __class_indices
    if __model is None:
        __model = load_model('model.h5')

    a_file = open("class_indices-v3.pkl", "rb")
    __class_indices = pkl.load(a_file)
    a_file.close()
    
    print("loading saved artifacts...done")


def decode_pred(pred):
    # diccionario 'id' : 'raza'
    temp_class_indices = dict = {value:key for key, value in __class_indices.items()}
    best_3 = pred.argsort()[-3:][::-1] # Se obtienen los indices de los mejores 3 valores de pred
    top_3 = np.sort(pred*100)[-3:][::-1].astype(int) # Se obtienen las probabilidades de los mejores 3 pred
    
    result = {
        'top1': [temp_class_indices[best_3[0]], top_3[0]], 
        'top2': [temp_class_indices[best_3[1]], top_3[1]], 
        'top3': [temp_class_indices[best_3[2]], top_3[2]], 
        
    }
    return result


def get_prediction(path_image):

    img = load_img(path_image, target_size = (600,600))
    x = tf.expand_dims(img_to_array(img), axis = 0)
    pred = __model.predict(x)[0]

    
    result = decode_pred(pred)


    return result


load_model_()


    
