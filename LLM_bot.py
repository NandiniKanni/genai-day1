import streamlit as st
import requests
from groq import Groq

# ---------------- PAGE SETUP ----------------
st.set_page_config("PragyanAI Content Generator", layout="wide")
st.title("📢 Nandini's Content Generator")

# ---------------- CLIENTS ----------------
groq_client = Groq(api_key=st.secrets["GROQ"]["GROQ_API_KEY"])
HF_API_KEY = st.secrets["HF"]["HF_API_KEY"]

# ---------------- IMAGE FUNCTION ----------------
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return None

    return response.content

# ---------------- UI ----------------
col1, col2 = st.columns(2)

with col1:
    product = st.text_input("Product")
    audience = st.text_input("Audience")

    if st.button("Generate Content"):
        if not product or not audience:
            st.warning("Please enter Product and Audience")
        else:
            prompt = f"Write marketing content for {product} targeting {audience}."
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.text = response.choices[0].message.content

    if st.button("Generate Image"):
        if not product or not audience:
            st.warning("Please enter Product and Audience")
        else:
            image_prompt = f"Professional marketing poster for {product}, targeting {audience}, clean design, high quality"
            img_bytes = generate_image(image_prompt)

            if img_bytes:
                st.session_state.image = img_bytes
            else:
                st.error("Image generation failed. Try again.")

with col2:
    if "text" in st.session_state:
        st.text_area(
            "Generated Content",
            st.session_state.text,
            height=300
        )

        st.download_button(
            "⬇️ Download Content",
            st.session_state.text,
            "marketing_copy.txt"
        )
    else:
        st.info("Generate content first")

    if "image" in st.session_state:
        st.image(
            st.session_state.image,
            caption="Generated Marketing Image",
            use_container_width=True
        )
