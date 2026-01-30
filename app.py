import streamlit as st
from google import genai
from PIL import Image

# 1. Initialize the Gemini Client
# Using st.secrets keeps your API key hidden from GitHub
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")
    st.stop()

# 2. UI Layout
st.title("🧬 Scriptox.ai")
st.markdown("### *Handwriting-to-Digital Logic Synthesis*")

# 3. File Input
img_file = st.file_uploader("Scan Lab Record", type=['jpg', 'png', 'jpeg'])
lang = st.selectbox("Select Target Language", ["C", "Java", "Python", "C++"])

# 4. Processing Logic
if img_file:
    # Convert uploaded file to PIL Image for the SDK
    raw_img = Image.open(img_file)
    st.image(raw_img, caption="Script Captured", use_container_width=True)
    
    if st.button("Synthesize Code ✨"):
        with st.spinner(f"Gemini 1.5 Flash is analyzing {lang} syntax..."):
            try:
                # The Gemini 1.5 Flash Multimodal Call
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[
                        f"Identify and OCR the handwritten {lang} code in this image. "
                        f"Correct any syntax errors and return ONLY the code block.",
                        raw_img
                    ]
                )
                
                # 5. Display Result
                st.subheader("✅ Synthesized Output:")
                st.code(response.text, language=lang.lower())
                st.balloons()
                
            except Exception as e:
                st.error(f"Error during synthesis: {e}")