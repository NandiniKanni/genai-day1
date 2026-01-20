from openai import OpenAI
import streamlit as st
from groq import Groq

st.set_page_config("PragyanAI Content Generator", layout="wide")
st.title("📢 Nandini's– Content Generator")

client = Groq(api_key=st.secrets["GROQ"]["GROQ_API_KEY"])
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


col1, col2 = st.columns(2)

with col1:
    product = st.text_input("Product")
    audience = st.text_input("Audience")

    if st.button("Generate Content"):
        prompt = f"Write marketing content for {product} targeting {audience}."
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        st.session_state.text = response.choices[0].message.content

    if st.button("Generate Image"):
        image_prompt = f"Marketing poster for {product} targeting {audience}"

        img = openai_client.images.generate(
            model="gpt-image-1",
            prompt=image_prompt,
            size="1024x1024"
        )

        st.session_state.image_url = img.data[0].url


with col2:
    if "text" in st.session_state:
        content = st.text_area("Generated Content", st.session_state.text, height=300)

        st.download_button(
            label="⬇️ Download as TXT",
            data=content,
            file_name="marketing_copy.txt",
            mime="text/plain"
        )
    else:
        st.info("Generate content first")
           
        
    if "image_url" in st.session_state:
        st.image(
            st.session_state.image_url,
            caption="Generated Marketing Image",
            use_container_width=True
        )

