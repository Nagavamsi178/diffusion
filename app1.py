#activate imggen env before running: conda activate imggen

import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# Set device
device = "cpu"

# Load the model (cached)
@st.cache_resource
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to(device)
    return pipe

pipe = load_model()

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of tuples (prompt, image)

# Streamlit UI
st.title("🖼️ AI Image Generator Chat")

prompt = st.text_input("Enter your prompt:", "")

if st.button("Generate Image") and prompt.strip() != "":
    with st.spinner("Generating..."):
        # Generate image
        image = pipe(prompt, num_inference_steps=25, guidance_scale=7.5).images[0]
        # Store prompt and image in chat history
        st.session_state.chat_history.append((prompt, image))

# Display chat history
for i, (p, img) in enumerate(st.session_state.chat_history):
    st.markdown(f"**Prompt {i+1}:** {p}")
    st.image(img, use_column_width=True)


# '''Prompt: "Futuristic city at sunset"
#            │
#            ▼
#      Text Encoder (CLIP)
#            │
#            ▼
#    Text embeddings (vector)
#            │
#            ▼
# Random noise latent ───> U-Net denoising steps guided by embeddings
#            │
#            ▼
#    Final latent
#            │
#            ▼
#    VAE Decoder
#            │
#            ▼
#    Generated Image
# '''