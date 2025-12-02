🧠✨ AI Image Classifier

A smart and interactive web app built with Streamlit that uses deep learning to recognize what’s inside your images — in just seconds! 🚀

🌐 Live Demo

🔗 Try it now: https://ai-image-classifier-yw8jmptfdt64yxxyxprabj.streamlit.app/

🖼️ About The Project

The AI Image Classifier is a lightweight, web-based tool that allows you to upload any image (JPG/PNG) and instantly get predictions about what’s in it 🤖.

It harnesses the power of MobileNetV2, a pre-trained convolutional neural network, to analyze images and display the top 3 predictions with their confidence scores 📊.

Whether it’s a 🐶 dog, 🚗 car, or ☕ coffee cup — this app figures it out instantly! ⚡

⚙️ Tech Stack & Tools

🧩 Python – The backbone of the entire project.
🎨 Streamlit – For building a smooth, interactive, and modern web UI.
🧠 TensorFlow / Keras – To load and run the pre-trained MobileNetV2 model.
🖼️ OpenCV – For image preprocessing (resizing and formatting).
📷 Pillow (PIL) – To handle uploaded image files seamlessly.

🔍 How It Works

1️⃣ Upload an Image
➡️ Choose any image file (JPG or PNG) from your device.

2️⃣ Model Preprocessing
🧮 The image is resized and normalized using OpenCV and preprocess_input().

3️⃣ Prediction Time
🤖 The MobileNetV2 model runs inference on the processed image.

4️⃣ Results Displayed
📊 The app shows the top 3 predicted labels along with their confidence percentages.

5️⃣ Visual Output
🖼️ You see your uploaded image alongside the predictions — neat and instant! ⚡
