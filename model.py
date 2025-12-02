import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions,
)
from PIL import Image

st.set_page_config(
    page_title="AI Image Classifier",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #000000;
    background-image: linear-gradient(147deg, #000000 0%, #434343 74%);
    color: white;
}
.st-emotion-cache-10trblm {
    color: #FFFFFF;
    text-align: center;
}
p, .st-emotion-cache-1r4qj8v {
    text-align: center;
    color: #E0E0E0;
}
.stButton>button {
    color: #FFFFFF;
    background-color: #2a2a72;
    background-image: linear-gradient(315deg, #2a2a72 0%, #009ffd 74%);
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 18px;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 4px 15px 0 rgba(49, 196, 190, 0.75);
}
.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px 0 rgba(49, 196, 190, 0.85);
    background-image: linear-gradient(315deg, #009ffd 0%, #2a2a72 74%);
}
.stButton>button:active {
    transform: translateY(-1px);
}
.stFileUploader {
    border: 2px dashed #009ffd;
    border-radius: 15px;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
}
.results-box {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    text-align: center;
}
.results-box h3 {
    color: #FFFFFF;
}
.results-box p {
    font-size: 1.1rem;
    color: #F0F0F0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model = MobileNetV2(weights="imagenet")
    return model

def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img)
    
    if img_array.ndim == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    if img_array.shape[2] == 4:
        img_array = img_array[..., :3]

    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

def classify_image(model, image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        return decoded_predictions
    except Exception as e:
        st.error(f"Error Classifying Image: {str(e)}")
        return None

def main():
    st.title("🖼️ AI Image Classifier")
    st.write("Upload an image and let our AI tell you what's inside!")

    model = load_model()

    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(
                uploaded_file, caption="Uploaded Image", use_column_width=True
            )
        
        with col2:
            st.write("")
            st.write("")
            if st.button("✨ Classify Image"):
                with st.spinner("🔍 Analyzing Image..."):
                    image = Image.open(uploaded_file)
                    predictions = classify_image(model, image)

                    if predictions:
                        # Display results in the styled box
                        st.markdown("<div class='results-box'><h3>Predictions</h3>", unsafe_allow_html=True)
                        for _, label, score in predictions:
                            st.markdown(f"<p>{label.replace('_', ' ').title()}: {score:.2%}</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
