import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions
)
from PIL import Image

@st.cache_resource
def load_model():
    model = MobileNetV2(weights="imagenet")
    return model

def preprocess_image(image):
    img = np.array(image)
    img = cv2.resize(img, (224, 224))
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def classify_image(model, image):
    try:
        processed_image = preprocess_image(image)
        predictions = model.predict(processed_image)
        decoded_predictions = decode_predictions(predictions, top=5)[0]
        return decoded_predictions
    except Exception as e:
        st.error(f"Error classifying image: {str(e)}")
        return None

def filter_animal_predictions(predictions):
    animal_predictions = []
    animal_keywords = [
    "dog", "cat", "elephant", "lion", "tiger", "leopard", "cheetah", "bear", "wolf", "fox",
    "rabbit", "deer", "moose", "bison", "buffalo", "cow", "goat", "sheep", "horse", "donkey",
    "pig", "monkey", "gorilla", "chimpanzee", "orangutan", "baboon", "lemur", "koala", "kangaroo", "opossum",
    "hedgehog", "bat", "otter", "beaver", "squirrel", "chipmunk", "rat", "mouse", "hamster", "porcupine",
    "camel", "llama", "alpaca", "reindeer", "zebra", "hippopotamus", "rhinoceros", "whale", "dolphin", "seal",
    "sea lion", "walrus", "panda", "sloth", "antelope", "gazelle", "giraffe", "jaguar", "cougar", "lynx",
    "eagle", "falcon", "hawk", "owl", "crow", "raven", "pigeon", "sparrow", "parrot", "macaw",
    "cockatoo", "flamingo", "peacock", "penguin", "swan", "duck", "goose", "chicken", "rooster", "turkey",
    "vulture", "stork", "crane", "heron", "hummingbird", "woodpecker", "kingfisher", "ostrich", "emu", "kiwi",
    "snake", "python", "cobra", "viper", "boa", "lizard", "gecko", "chameleon", "iguana", "monitor lizard",
    "crocodile", "alligator", "turtle", "tortoise", "terrapin", "skink", "komodo dragon", "anole", "gila monster", "tuatara",
    "frog", "toad", "salamander", "newt", "axolotl", "caecilian",
    "shark", "salmon", "tuna", "trout", "goldfish", "carp", "catfish", "barracuda", "mackerel", "cod",
    "snapper", "perch", "anchovy", "sardine", "eel", "clownfish", "seahorse", "stingray", "piranha", "betta",
    "ant", "bee", "wasp", "butterfly", "moth", "spider", "scorpion", "crab", "lobster", "shrimp",
    "jellyfish", "octopus", "squid", "snail", "slug", "earthworm", "leech", "starfish", "sea urchin", "coral",
    "centipede", "millipede", "beetle", "grasshopper", "locust", "dragonfly", "ladybug", "termite", "cockroach", "firefly",
    "seal", "sea otter", "sea turtle", "manatee", "dugong", "narwhal", "orca", "blue whale", "crayfish", "clam",
    "oyster", "mussel", "sea cucumber", "plankton", "krill", "barnacle", "anemone", "sponge", "coral polyp", "urchin",
    "axolotl", "capybara", "pangolin", "aardvark", "armadillo", "meerkat", "quokka", "tapir", "okapi", "wombat",
    "emu", "cassowary", "shoebill", "hoatzin", "kakapo", "ibis", "toucan", "parakeet", "lorikeet", "crow pheasant"
]


    for pred in predictions:
        wn_id, label, prob = pred
        if any(keyword in label.lower() for keyword in animal_keywords):
            animal_predictions.append(pred)
    return animal_predictions

def main():
    st.set_page_config(page_title="Animal Image Identifier")
    st.title("Animal Image Identifier")
    st.write("Upload an image of an animal, and the AI will identify it!")

    model = load_model()

    uploaded_file = st.file_uploader("Choose an animal image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Identify Animal"):
            with st.spinner("Identifying..."):
                predictions = classify_image(model, image)
                if predictions:
                    animal_preds = filter_animal_predictions(predictions)
                    if animal_preds:
                        st.subheader("Animal Predictions:")
                        for _, label, score in animal_preds:
                            st.write(f"{label}: {score:.2%}")
                    else:
                        st.warning("No animal detected in the top predictions. Try another image.")


if __name__ == "__main__":
    main()