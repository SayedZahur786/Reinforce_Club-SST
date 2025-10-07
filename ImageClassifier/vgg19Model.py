import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.applications import vgg19
from tensorflow.keras.preprocessing.image import img_to_array
import io 

CONTENT_LAYER = 'block5_conv2'
STYLE_LAYERS = [
    'block1_conv1',
    'block2_conv1',
    'block3_conv1',
    'block4_conv1',
    'block5_conv1'
]



def preprocess_image(image, target_size):
    
    img = image.resize(target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
   
    return vgg19.preprocess_input(img)

def deprocess_image(x):
    
    x = x.reshape((x.shape[1], x.shape[2], 3))
   
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    x = x[:, :, ::-1]
    x = np.clip(x, 0, 255).astype('uint8')
    return x



def get_model():
    
    
    vgg = vgg19.VGG19(weights="imagenet", include_top=False)
    vgg.trainable = False
    
    
    content_output = vgg.get_layer(CONTENT_LAYER).output
    style_outputs = [vgg.get_layer(layer_name).output for layer_name in STYLE_LAYERS]
    
    
    return tf.keras.Model(vgg.input, [content_output] + style_outputs)

def gram_matrix(input_tensor):
    
    if len(input_tensor.shape) == 4:
        
        input_tensor = tf.squeeze(input_tensor, axis=0)
    
   
    input_tensor = tf.reshape(input_tensor, [-1, input_tensor.shape[-1]])
    
    
    return tf.matmul(input_tensor, input_tensor, transpose_a=True)

def style_loss(style, combination, num_style_layers):
    
    style_grams = [gram_matrix(s) for s in style]
    combination_grams = [gram_matrix(c) for c in combination]
    
    total_style_loss = 0
    for style_gram, comb_gram in zip(style_grams, combination_grams):
        
        s_size = tf.cast(style_gram.shape[0] * style_gram.shape[1], tf.float32)
        total_style_loss += tf.reduce_sum(tf.square(style_gram - comb_gram)) / s_size
        
    return total_style_loss / num_style_layers

def content_loss(content, combination):
    
    return tf.reduce_sum(tf.square(content - combination))

def total_loss(content_target, style_targets, combination_features, 
               content_weight, style_weight):
    
    content_features = combination_features[0] 
    
    style_features = combination_features[1:]
    
    c_loss = content_loss(content_target[0], content_features) 
   
    s_loss = style_loss(style_targets, style_features, len(STYLE_LAYERS))
    
    return content_weight * c_loss + style_weight * s_loss


@st.cache_resource
def get_style_transfer_model():
    
    return get_model()


def main():
    st.set_page_config(page_title="Neural Style Transfer", layout="wide")
    st.title("Neural Style Transfer with vgg19")
    st.write("Upload a content image and a style image to combine their features.")
    st.warning("This process is computationally intensive and can take several minutes to complete, especially with larger images.")

    col1, col2 = st.columns(2)
    with col1:
        content_file = st.file_uploader("Upload Content Image", type=["jpg", "png", "jpeg"])
    with col2:
        style_file = st.file_uploader("Upload Style Image", type=["jpg", "png", "jpeg"])
        
    if content_file and style_file:
        content_image = Image.open(content_file).convert("RGB")
        style_image = Image.open(style_file).convert("RGB")
        
        st.subheader("Uploaded Images")
        col1, col2 = st.columns(2)
        with col1:
            st.image(content_image, caption="Content Image", use_container_width=True)
        with col2:
            st.image(style_image, caption="Style Image", use_container_width=True)
            
      
        iterations = st.slider("Iterations (higher for better results, slower)", 100, 1000, 200, step=100)
        content_weight = st.slider("Content Weight (Controls content preservation)", 1e-3, 1e-1, 1e-2, format="%.2e")
        style_weight = st.slider("Style Weight (Controls style emphasis)", 1e-1, 1e2, 1e0, format="%.2e")
        
        if st.button("Generate Stylized Image"):
            with st.spinner("Generating image... This may take a while."):
                
              
                model = get_style_transfer_model()
                
               
                img_size = (300, 300)
                content_tensor = preprocess_image(content_image, img_size)
                style_tensor = preprocess_image(style_image, img_size)              
               
                content_target = model(content_tensor)
                style_targets = model(style_tensor)[1:]

                generated_image = tf.Variable(content_tensor, dtype=tf.float32)
                
                optimizer = tf.keras.optimizers.Adam(learning_rate=5.0)

                @tf.function
                def train_step():
                    with tf.GradientTape() as tape:
        
                        combination_features = model(generated_image)
                        loss = total_loss(content_target, style_targets, combination_features, 
                                          content_weight, style_weight)
                    
               
                    grads = tape.gradient(loss, generated_image)
                    optimizer.apply_gradients([(grads, generated_image)])
                   
                    generated_image.assign(tf.clip_by_value(generated_image, 0, 255))

                for i in range(iterations):
                    train_step()

                stylized_output = deprocess_image(generated_image.numpy())
                st.subheader("Stylized Image")
                st.image(stylized_output, caption="Generated Image", use_container_width=True)
                
                result_pil = Image.fromarray(stylized_output)
                buffer = io.BytesIO() 
                result_pil.save(buffer, format="JPEG")
                st.download_button(
                    label="Download Stylized Image",
                    data=buffer.getvalue(),
                    file_name="stylized_image.jpg",
                    mime="image/jpeg"
                )

if __name__ == "__main__":
    main()
