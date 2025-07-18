import streamlit as st
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torch

# Page config
st.set_page_config(page_title="Image Caption Generator", page_icon="🖼️")

# Title
st.title("🖼️ Image Caption Generator using Hugging Face & Streamlit")
st.markdown("Upload an image and get a descriptive caption generated by a pre-trained model.")

# Load model
@st.cache_resource
def load_model():
    model = VisionEncoderDecoderModel.from_pretrained("ydshieh/vit-gpt2-coco-en")
    feature_extractor = ViTImageProcessor.from_pretrained("ydshieh/vit-gpt2-coco-en")
    tokenizer = AutoTokenizer.from_pretrained("ydshieh/vit-gpt2-coco-en")
    return model, feature_extractor, tokenizer

model, feature_extractor, tokenizer = load_model()

# Caption generation function
def generate_caption(image: Image.Image):
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    output_ids = model.generate(pixel_values, max_length=16)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption

# Upload
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            caption = generate_caption(image)
            st.markdown(f"### 📝 Caption: \n> *{caption}*")
