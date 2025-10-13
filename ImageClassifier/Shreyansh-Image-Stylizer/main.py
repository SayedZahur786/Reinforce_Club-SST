import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="AI Style Transfer", layout="wide")

def load_model():
    model_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    return hub.load(model_url)


def preprocess_image(image, target_size=(256, 256)):
    image = image.resize(target_size)
    image = np.array(image) / 255.0
    image = image.astype(np.float32)
    image = np.expand_dims(image, axis=0)
    return image


def perform_style_transfer(content_img, style_img, model):
    content_tensor = preprocess_image(content_img, (384, 384))
    style_tensor = preprocess_image(style_img, (256, 256))

    stylized_image = model(tf.constant(content_tensor), tf.constant(style_tensor))[0]
    stylized_image = np.squeeze(stylized_image)
    stylized_image = np.clip(stylized_image * 255, 0, 255).astype(np.uint8)

    return Image.fromarray(stylized_image)


st.title("AI Style Transfer by Shreyansh")
st.markdown("Transform your photos with your own styles.")

model = load_model()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Content Image")
    content_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"], key="content")
    if content_file:
        content_image = Image.open(content_file).convert("RGB")
        st.image(content_image, use_container_width=True)

with col2:
    st.subheader("Style Image")
    style_file = st.file_uploader("Upload artistic style", type=["jpg", "jpeg", "png"], key="style")
    if style_file:
        style_image = Image.open(style_file).convert("RGB")
        st.image(style_image, use_container_width=True)

if content_file and style_file:
    if st.button("Apply Style Transfer", type="primary", use_container_width=True):
        with st.spinner("Creating your masterpiece..."):
            result = perform_style_transfer(content_image, style_image, model)

        st.subheader("Stylized Result")
        st.image(result, use_container_width=True)

        buf = io.BytesIO()
        result.save(buf, format="PNG")
        st.download_button(
            label="Download Your stylized version",
            data=buf.getvalue(),
            file_name="stylized_image.png",
            mime="image/png",
            use_container_width=True
        )
else:
    st.info("Upload both content and style images.")
