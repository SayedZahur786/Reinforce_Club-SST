# Image Classifier

This project is an AI-powered image classifier using TensorFlow, Streamlit, and the Pexels API. Users upload an image, and the model predicts the top 3 objects. It also fetches a similar image from Pexels for the top prediction.

## Features

- Upload images for classification
- Top-3 predictions using MobileNetV2
- Fetches similar images from Pexels API
- Streamlit web interface

## Setup

1. Add your Pexels API key in `.env`:
   ```
   Pexels_API_Key = "YOUR_API_KEY"
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   python -m streamlit run model.py
   ```

## Files

- `model.py`: Main application code
- `.env`: Stores API key

## Author

Prabhat Ranjan Jha