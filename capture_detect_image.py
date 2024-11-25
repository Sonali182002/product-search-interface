import cv2
import os
import time
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import warnings
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions






def capture_image():
    print("Current working directory:", os.getcwd())

    cap = cv2.VideoCapture(0)  # Start capturing from the webcam
    ret, frame = cap.read()

    if ret:
        # Save the image with a timestamp in the name
        image_path = os.path.join(os.getcwd(), 'product.jpg')  # Example: 'product.jpg'
        print(f"Image captured! Saving as: {image_path}")
        
        # Save the image
        success = cv2.imwrite(image_path, frame)
        if success:
            print(f"Image saved at: {image_path}")
        else:
            print("Failed to save image.")
        
        # Optionally, save the image with a timestamp in the name for uniqueness
        image_name = f"product_{int(time.time())}.jpg"
        cv2.imwrite(image_name, frame)
        print(f"Image saved as '{image_name}'")
        
    else:
        print("Failed to capture image")

    cap.release()
    cv2.destroyAllWindows()

    return image_path  # Return the path to the captured image

model = MobileNetV2(weights="imagenet")



# Load the MobileNetV2 model once globally
model = MobileNetV2(weights="imagenet")

def classify_image(image_path):
    try:
        # Open and resize the image
        img = Image.open(image_path).resize((224, 224))
    except FileNotFoundError:
        print(f"Error: The image file at {image_path} was not found.")
        return None

    # Convert the image to a numpy array and preprocess it
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Normalize and preprocess for MobileNetV2

    # Make predictions
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)  # Decode predictions for readability

    # Extract the label and confidence score
    if decoded_predictions and len(decoded_predictions[0]) > 0:
        label, description, confidence = decoded_predictions[0][0]
        return f"Predicted: {description}"
    else:
        return "No predictions found."


