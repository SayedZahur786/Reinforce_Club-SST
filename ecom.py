import streamlit as st
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import cv2
import os

# -------------------------
# Load the MobileNetV2 model
# -------------------------
@st.cache_resource
def load_model():
    base_model = MobileNetV2(weights="imagenet", include_top=True)
    feature_model = MobileNetV2(weights="imagenet", include_top=False, pooling="avg")
    return base_model, feature_model

# -------------------------

# Preprocess the uploaded image
# -------------------------
def preprocess_image(img):
    img = np.array(img)
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

# -------------------------
# Classify the image
# -------------------------
def classify_image(model, img):
    processed = preprocess_image(img)
    preds = model.predict(processed)
    decoded = decode_predictions(preds, top=3)[0]
    return decoded

# -------------------------
# Extract feature embedding
# -------------------------
def extract_features(feature_model, img):
    processed = preprocess_image(img)
    features = feature_model.predict(processed)
    return features.flatten()

# -------------------------
# Load database of product images
# -------------------------
def build_product_database(feature_model, product_dir="products"):
    """
    Loads all product images from given folders (dress, shoes, jewellery)
    and extracts feature vectors for each.
    """
    database = []
    if not os.path.exists(product_dir):
        st.error(f"Product folder '{product_dir}' not found. Please create it next to ecom.py.")
        return database

    for category in ["dress", "shoes", "jewellery"]:
        cat_path = os.path.join(product_dir, category)
        if not os.path.isdir(cat_path):
            continue

        for file in os.listdir(cat_path):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(cat_path, file)
                try:
                    img = Image.open(img_path).convert("RGB")
                    feat = extract_features(feature_model, img)
                    database.append({
                        "category": category,
                        "image_path": img_path,
                        "features": feat
                    })
                except Exception as e:
                    st.warning(f"Could not process image {file}: {e}")

    return database

# -------------------------
# Find similar products
# -------------------------
def recommend_similar_products(upload_features, database, top_n=5):
    if not database:
        return []
    db_features = np.array([item["features"] for item in database])
    similarities = cosine_similarity([upload_features], db_features)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    recommendations = [database[i] for i in top_indices]
    return recommendations

# -------------------------
# Streamlit App
# -------------------------
def main():
    st.set_page_config(page_title="🛍️ Fashion Product Recognition & Recommendations", layout="wide")
    st.title("👗🛒 Fashion Product Recognition & Recommendation System")

    base_model, feature_model = load_model()

    st.write(
        """
        Upload an image of a **dress**, **shoe**, or **piece of jewellery**, 
        and this AI will recognize it and suggest similar products!
        """
    )

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Analyze and Recommend"):
            with st.spinner("Recognizing and searching for similar items..."):
                # Step 1: Classify the image (general recognition)
                predictions = classify_image(base_model, img)
                st.subheader("Top Predictions:")
                for i, (_, label, score) in enumerate(predictions, 1):
                    st.write(f"{i}. **{label.replace('_', ' ').title()}** — Confidence: {score:.2%}")

                # Step 2: Build the feature database
                product_db = build_product_database(feature_model)

                if not product_db:
                    st.error("No product images found. Please ensure 'products/dress', 'products/shoes', and 'products/jewellery' folders have images.")
                    return

                # Step 3: Find similar products
                uploaded_feat = extract_features(feature_model, img)
                recs = recommend_similar_products(uploaded_feat, product_db, top_n=5)

                # Step 4: Display results
                st.subheader("🧩 Recommended Similar Products")

                cols = st.columns(5)
                for col, rec in zip(cols, recs):
                    with col:
                        st.image(rec["image_path"], caption=f"{rec['category'].title()}", use_container_width=True)

                st.info("Recommendations are based on visual similarity using deep learning (MobileNetV2 features).")

if __name__ == "__main__":
    main()
