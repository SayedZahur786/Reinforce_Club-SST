# AI Style Transfer App

This is a web application that transforms your photos into artistic masterpieces using neural style transfer. Upload a content image and a style image, and watch as the AI combines them to create a unique stylized artwork.

## Features

* **Simple Upload Interface**: Easy drag-and-drop for content and style images.
* **Neural Style Transfer**: Uses Google's Magenta arbitrary image stylization model to apply any artistic style to your photos.
* **Instant Results**: Process images in seconds with real-time preview.
* **Download Output**: Save your stylized creations directly from the app.
* **Smart Caching**: Model loads once and stays in memory for faster subsequent transfers.

## How It Works

The application is built with a few key libraries:

* **Streamlit**: The core framework for creating the interactive web application with a clean two-column layout.
* **TensorFlow & TensorFlow Hub**: Provides the pre-trained Magenta style transfer model that analyzes artistic patterns and applies them to your images.
* **Pillow & NumPy**: Used for image processing, resizing, and format conversions.

The model takes two inputs: a content image (your photo at 384x384) and a style image (artwork at 256x256). It extracts the artistic features from the style image and applies them to the content while preserving the original structure.

## File Structure

* `main.py`: The main Streamlit application script that handles the UI, image uploads, model loading, and style transfer processing.
* `requirements.txt`: Lists all the Python dependencies required for the project.
* `README.md`: Project documentation.

## Installation & Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run main.py
   ```

3. Open your browser at `http://localhost:8501`, upload your images, and click "Apply Style Transfer"!