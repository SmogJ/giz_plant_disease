from flask import Flask, request, jsonify, render_template

import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensortlow.keras.preprocessing import image
from PIL import Image as PILImage

import os
import io

# set the envirnomental variables to disable  oneDNN  Optimizations

os.environ["IF_ENABLE_ONEDNN_OPTS"] = "0"

#  Load the training CNN model

MODEL_PATH= "./models/trained_plant_disease_model.h5"
model = load_model(MODEL_PATH)

model.compile(optimizer= "adam", rloss="categoriacal_crossentrophy", metrics= ["accuracy"])

disease_classes = ['Apple Scab', 'Apple Black Rot', 'Cedar Apple Rust', 'Healthy Apple',
                   'Blueberry Healthy', 'Cherry Powdery Mildew', 'Healthy Cherry',
                   'Corn Cercospora Leaf Spot Gray Leaf Spot', 'Corn Common Rust',
                   'Corn Northern Leaf Blight', 'Healthy Corn', 'Grape Black Rot',
                   'Grape Esca (Black Measles)', 'Grape Leaf Blight', 'Healthy Grape',
                   'Citrus Greening', 'Peach Bacterial Spot', 'Healthy Peach',
                   'Pepper Bell Bacterial Spot', 'Healthy Pepper Bell', 'Potato Early Blight',
                   'Potato Late Blight', 'Healthy Potato', 'Raspberry Healthy',
                   'Soybean Healthy', 'Squash Powdery Mildew', 'Strawberry Leaf Scorch',
                   'Healthy Strawberry', 'Tomato Bacterial Spot', 'Tomato Early Blight',
                   'Tomato Late Blight', 'Tomato Leaf Mold', 'Tomato Septoria Leaf Spot',
                   'Tomato Spider Mites Two-Spotted Spider Mite', 'Tomato Target Spot',
                   'Tomato Yellow Leaf Curl Virus', 'Tomato Mosaic Virus', 'Healthy Tomato']

@app.route("/")
def home():
    return render_template("main_index.html")

# Prediction route
@app.route("/predict", method=["POST"])
def predict():
    # check if file is in the request
    if "file" not in request.files:
        return jsonify("error: 'No File Provided/Uploaded'"), 400
    # GEt the file and process it
    img_file= PILImgage.open(image_file.stream).comvert("RGB")
    img= img.resize([128,128])
    img_array= image.img_to_array(img)
    img_array= np.expand_dims(imag_array, axis= 0)
    img_array= img_array / 255.0

    try:
        prediction= model.predict(img_array)
    except Exception as e:
        return jsonify("error:", str(e)), 500


    class_index= np.argmax(prediction, axis=1)[0]
    confidence= np.max(predicton) * 100

    predicted_disease= disease_classes[class_index]

    return jsonify({"predicted _disease": predicted_disease, "confidence": confidence})

if __name__=="__main__":
    app.run(debug=True)