import streamlit as st
import cv2
import numpy as np
import time
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from PIL import Image

@st.cache_resource
def load_model():
    model = MobileNetV2(weights='imagenet')
    return model

model = load_model()

st.set_page_config(page_title="Real-Time Object Detector", layout="centered")
st.title("🎥 Real-Time Object Detection using MobileNetV2")
st.markdown("Detect objects in real-time using your webcam or upload images. Only predictions above your chosen confidence will be displayed.")

threshold = st.slider("Set Confidence Threshold (%)", 0, 100, 20, 5)

mode = st.radio("Select Input Mode:", ["📸 Webcam", "🖼 Upload Image"])

if mode == "🖼 Upload Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        img = np.array(image.resize((224, 224)))
        img = preprocess_input(np.expand_dims(img, axis=0))
        preds = model.predict(img)
        decoded = decode_predictions(preds, top=3)[0]

        st.subheader("Predictions:")
        found = False
        for (imagenet_id, label, score) in decoded:
            if score * 100 >= threshold:
                st.write(f"**{label.capitalize()}** – {score*100:.2f}% confidence")
                found = True
        if not found:
            st.warning(f"No predictions above {threshold}% confidence.")

else:
    st.info("Click the checkbox below to start your webcam feed and detect objects in real time.")
    run = st.checkbox("🎬 Start Webcam Detection")

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    prev_time = 0

    while run:
        ret, frame = camera.read()
        if not ret:
            st.warning("⚠️ Could not access camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb_frame, (224, 224))
        x = preprocess_input(np.expand_dims(resized, axis=0))

        preds = model.predict(x)
        decoded = decode_predictions(preds, top=3)[0]

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        y_offset = 40
        shown = False
        for i, (_, label, score) in enumerate(decoded):
            conf = score * 100
            if conf >= threshold:
                shown = True
                text = f"{label}: {conf:.1f}%"
                color = (0, 255 - i * 60, i * 80)

                h, w, _ = rgb_frame.shape
                box_w, box_h = int(w * 0.5), int(h * 0.5)
                x1, y1 = (w - box_w) // 2, (h - box_h) // 2
                x2, y2 = x1 + box_w, y1 + box_h
                cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), color, 3)
                cv2.putText(rgb_frame, text, (x1 + 10, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)

        cv2.putText(rgb_frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

        if not shown:
            cv2.putText(rgb_frame, f"No object > {threshold}%", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 50, 50), 2, cv2.LINE_AA)

        FRAME_WINDOW.image(rgb_frame)

    else:
        camera.release()
