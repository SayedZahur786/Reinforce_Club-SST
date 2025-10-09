import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions # type: ignore
from PIL import Image
import requests, io, os
from dotenv import load_dotenv
load_dotenv()

Pexel_headers = {"Authorization": os.getenv("Pexels_API_Key")}


def load_model():
    model = MobileNetV2(weights="imagenet")
    return model

def preprocess_image(image):
    img = np.array(image) #Converting the image into an rgb array
    img = cv2.resize(img, (224, 224)) #Resizing because of input requirement
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0) #Expanding dimensions
    return img

def classify_image(model, image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        return decoded_predictions
    except Exception as e:
        st.error(f"Error Classifying image: {str(e)}")
        return None
    
def main():
    st.set_page_config(page_title="AI Image Classifier")

    st.title("AI Image Classifier")
    st.write("Upload an image and let AI tell you what is in it!")

    @st.cache_resource #This will cache the below function
    def load_cached_model():
        return load_model()
    
    model = load_cached_model()

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        image = st.image(
            uploaded_file, caption="Uploaded Image", use_container_width=True
        )
        btn = st.button("Classify Image")

        if btn:
            with st.spinner("Analyzing Image..."):
                image = Image.open(uploaded_file)
                predictions = classify_image(model, image)

                @st.cache_data(show_spinner=False)
                def fetch_pexels(query: str):
                    try:
                        search_url = "https://api.pexels.com/v1/search"
                        params = {"query": query, "per_page": 1, "orientation": "square"}
                        r = requests.get(search_url, headers=Pexel_headers, params=params, timeout=10)
                        if r.status_code != 200:
                            st.error(f"Pexels search failed: {r.status_code}")
                            return None
                        data = r.json()
                        if not data["photos"]:
                            return None
                        img_url = data["photos"][0]["src"]["medium"]
                        img_resp = requests.get(img_url, timeout=10)
                        if img_resp.status_code == 200:
                            return Image.open(io.BytesIO(img_resp.content)).convert("RGB")
                    except Exception as e:
                        st.error(f"Pexels error: {e}")
                    return None

                if predictions:
                    st.subheader("Predictions")
                    for _, label, score, in predictions:
                        st.write(f"{label}: {score: .2%}")
                    
                    similar=fetch_pexels(predictions[0][1])
                    if similar:
                        st.image(similar, caption=f"Pexels photo for '{predictions[0][1]}'", width=300)
                    else:
                        st.info("No similar photo found on Pexels.")



if __name__ == "__main__":
    main()


