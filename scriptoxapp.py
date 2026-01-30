import streamlit as st
from google import genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Scriptox.ai", page_icon="🧬")

# 2. Authentication
# This pulls from your .streamlit/secrets.toml locally or Streamlit Cloud Secrets
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found!")
    st.stop()

# 3. UI
st.title("🧬 Scriptox.ai")
st.write("Turn handwritten lab records into digital code.")

img_file = st.file_uploader("Upload image", type=['jpg', 'png', 'jpeg'])
lang = st.selectbox("Language", ["C", "Java", "Python", "C++"])

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Captured Script")
    
    if st.button("Synthesize ✨"):
        with st.spinner("Analyzing..."):
            try:
                # Use 'gemini-1.5-flash' - the modern string for the new SDK
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[
                        f"Extract the handwritten {lang} code. Fix syntax. Return ONLY code.", 
                        img
                    ]
                )
                
                # Display output
                st.subheader("✅ Digital Output:")
                st.code(response.text, language=lang.lower())
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Tip: Try checking if your API key is active in Google AI Studio.")