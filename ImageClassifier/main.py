import numpy as np
import streamlit as st
import tensorflow as tf
import cv2
import tensorflow_hub as hub
from PIL import Image, ImageDraw, ImageFont


def load_model():
    model_url="https://tfhub.dev/tensorflow/efficientdet/d0/1"
    return hub.load(model_url)

def load_labels():
    #COCO labes(90 classes)--->prediction output to string label
    labels_path=tf.keras.utils.get_file(
        "coco_labels.txt",
        "https://raw.githubusercontent.com/amikelive/coco-labels/master/coco-labels-paper.txt"
    )
    with open(labels_path, "r") as f:
        labels = f.read().splitlines()
        #f.read-->read the entire file at once
        #splitlines-->make every line a single element of a list,since each line here has a single word like(cat,dag car)
        #hence we get a list of all id(objects in a picture which might be present)
        return labels
    
def run_detector(model,image):
    img=np.array(image)
    img_tensor=tf.convert_to_tensor(img,dtype=tf.uint8)
    img_tensor = tf.expand_dims(img_tensor, axis=0)

    output=model(img_tensor)  #similar to model.predict in mobileNet it returns the output

    #it returns a dictionary with multiple outputs(detection_boxes,detection_classes,detection_scores)
    

    # Extract the results for the first image in the batch
    boxes = output["detection_boxes"][0].numpy()        # [ymin, xmin, ymax, xmax], normalized
    class_ids = output["detection_classes"][0].numpy().astype(int)  # Convert float to int
    scores = output["detection_scores"][0].numpy()      # Confidence scores between 0-1
    
    return boxes,class_ids,scores

def draw_boxes(image,boxes,class_ids,scores,labels):
    img=np.array(image)
    height,width,_=img.shape

    for box,cls_id,score in zip(boxes,class_ids,scores):
        if score<0.5:
            continue

        ymin,xmin,ymax,xmax=box
        start_point=(int(xmin*width),int(ymin*height))
        end_point=(int(xmax*width),int(ymax*height))
        
        color=(0,255,0)  #green
        cv2.rectangle(img,start_point,end_point,color,2)

        label = labels[cls_id - 1] if 0 < cls_id <= len(labels) else str(cls_id)
        text = f"{label}: {score:.2f}"
        cv2.putText(
            img,
            text,
            (start_point[0], max(0, start_point[1]-5)),  # Text above the box
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,  # Font scale
            color,
            1  # Thickness
        )
    return Image.fromarray(img)  #converts numpyarray back to pil image

def main():
    st.title("EfficientDet Object Detection 🖼️")
    st.write("Upload an image and detect objects!")

    @st.cache_resource
    def load_cached_model():
        return load_model()
    
    model = load_cached_model()
    labels = load_labels()

    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Run Detection"):
            with st.spinner("Detecting objects..."):
                boxes, class_ids, scores = run_detector(model, image)
                result_img = draw_boxes(image, boxes, class_ids, scores, labels)
                st.image(result_img, caption="Detection Result", use_container_width=True)

if __name__ == "__main__":
    main()