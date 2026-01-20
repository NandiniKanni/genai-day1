import streamlit as st
from groq import Groq
import urllib.parse

st.set_page_config("My Content Generator", layout="wide")
st.title("📢 Nandini's Content Generator")

# Groq client
client = Groq(api_key=st.secrets["GROQ"]["GROQ_API_KEY"])

col1, col2 = st.columns(2)

with col1:
    product = st.text_input("Product")
    audience = st.text_input("Audience")

    if st.button("Generate Content"):
        if product and audience:
            prompt = f"Write marketing content for {product} targeting {audience}."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.text = response.choices[0].message.content
        else:
            st.warning("Enter product and audience")

    if st.button("Generate Image"):
        if product and audience:
            image_prompt = f"Professional marketing poster for {product}, targeting {audience}, clean design"
            encoded_prompt = urllib.parse.quote(image_prompt)

            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024"

            st.session_state.image_url = image_url
        else:
            st.warning("Enter product and audience")

with col2:
    if "text" in st.session_state:
        st.text_area("Generated Content", st.session_state.text, height=300)

        st.download_button(
            "⬇️ Download Content",
            st.session_state.text,
            "marketing_copy.txt"
        )

    if "image_url" in st.session_state:
        st.image(
            st.session_state.image_url,
            caption="Generated Marketing Image",
            use_container_width=True
        )

