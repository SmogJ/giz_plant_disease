from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
from PIL import Image as PILImage

# Set environment variable to disable oneDNN optimizations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

app = Flask(__name__)

# Load the trained CNN model
MODEL_PATH = './models/trained_plant_disease_model_1.h5'
model = load_model(MODEL_PATH)

# Compile the model to avoid warnings
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define the disease classes (based on PlantVillage dataset)
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
                   'Tomato Yellow Leaf Curl Virus', 'Tomato Mosaic Virus', 'Healthy Tomato']

# Home route to serve the form page
@app.route('/')
def home():
    return render_template('index_1.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    # Get the file and preprocess it
    img_file = request.files['file']
    
    # Use PIL to open the image
    img = PILImage.open(img_file.stream).convert('RGB')
    img = img.resize((128, 128))  # Resize image
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Prepare the image for prediction
    img_array = img_array / 255.0  # Normalize the image

    # Make the prediction
    try:
        prediction = model.predict(img_array)
        print("Raw prediction probabilities:", prediction)  # Log raw probabilities
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    class_index = np.argmax(prediction, axis=1)[0]
    confidence = float(np.max(prediction) * 100)  # Get the prediction confidence percentage
    
    # Get the predicted disease
    predicted_disease = disease_classes[class_index]
    print(f"Predicted Disease: {predicted_disease} (Confidence: {confidence:.2f}%)")  # Log the prediction

    # Return the result as JSON
    return jsonify({'predicted_disease': predicted_disease, 'confidence': confidence})

if __name__ == '__main__':
    app.run(debug=True)