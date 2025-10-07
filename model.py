import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image

# Function to load the pre-trained model
def load_model():
    """Loads the pre-trained MobileNetV2 model."""
    model = MobileNetV2(weights="imagenet")
    return model

# Function to preprocess the image for the model
def preprocess_image(image):
    """
    Preprocesses the uploaded image to the format required by MobileNetV2.
    - Converts to RGB if it's RGBA.
    - Resizes to 224x224 pixels.
    - Applies model-specific preprocessing.
    - Expands dimensions for batch prediction.
    """
    img = np.array(image)
    # Ensure image is 3-channel (RGB)
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

# Function to classify the image
def classify_image(model, image):
    """
    Classifies the image using the loaded model.
    Returns the top 3 predictions.
    """
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        return decoded_predictions
    except Exception as e:
        st.error(f"Error classifying image: {str(e)}")
        return None

# Main function for the Streamlit app layout and logic
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="AI Image Classifier")

    st.title("AI Image Classifier")
    st.write("Upload an image and let the AI tell you what's in it!")

    # Cache the model so it doesn't reload on every interaction
    @st.cache_resource
    def load_cached_model():
        return load_model()

    model = load_cached_model()

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # We need to open the image with PIL for display and processing
        image_to_process = Image.open(uploaded_file)
        
        st.image(
            image_to_process, caption="Uploaded Image", use_column_width=True
        )
        
        # Button to trigger the classification
        if st.button("Classify Image"):
            with st.spinner("Analyzing Image..."):
                predictions = classify_image(model, image_to_process)

                if predictions:
                    st.subheader("Predictions:")
                    for _, label, score in predictions:
                        # Format the label for better readability
                        formatted_label = label.replace("_", " ").title()
                        st.write(f"- {formatted_label}: {score:.2%}")

# Entry point for the script
if __name__ == "__main__":
    main()
