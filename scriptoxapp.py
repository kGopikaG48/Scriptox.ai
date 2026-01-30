import streamlit as st
from google import genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Scriptox.ai", page_icon="📜")

# 2. Secure Authentication
if "GEMINI_API_KEY" in st.secrets:
    try:
        # We force 'v1' to avoid the 404 v1beta error
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"],
            http_options={'api_version': 'v1'}
        )
    except Exception as e:
        st.error(f"Client Init Error: {e}")
        st.stop()
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

# 3. UI Layout
st.title("🧬 Scriptox.ai")
st.write("Convert handwritten lab records to clean digital code.")

img_file = st.file_uploader("Upload Lab Record Image", type=['jpg', 'png', 'jpeg'])
lang = st.selectbox("Select Language", ["C", "Java", "Python", "C++"])

# 4. Processing Logic
if img_file:
    raw_img = Image.open(img_file)
    st.image(raw_img, caption="Scanning Script...", use_container_width=True)
    
    if st.button("Synthesize ✨"):
        with st.spinner(f"Gemini 2.5 Flash is digitizing {lang}..."):
            try:
                # Use the latest stable 2026 model ID
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        f"Extract the handwritten {lang} code. Fix syntax. Return ONLY code.", 
                        raw_img
                    ]
                )
                
                if response.text:
                    st.subheader("✅ Digital Code Output:")
                    st.code(response.text, language=lang.lower())
                else:
                    st.warning("No text detected. Try a clearer photo.")
                    
            except Exception as e:
                st.error(f"Synthesis Error: {e}")
                st.info("Check if your API Key is active at aistudio.google.com")