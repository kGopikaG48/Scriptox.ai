import streamlit as st
from google import genai
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Scriptox.ai", page_icon="🧬", layout="centered")

# 2. Authentication & Client Setup
# We use the 'v1' api_version to fix the 404 error found in the beta endpoint
if "GEMINI_API_KEY" in st.secrets:
    try:
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"],
            http_options={'api_version': 'v1'}
        )
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
        st.stop()
else:
    st.error("🔑 GEMINI_API_KEY not found! Add it to your .streamlit/secrets.toml")
    st.stop()

# 3. User Interface
st.title("🧬 Scriptox.ai")
st.markdown("### *Handwriting-to-Code Synthesis Engine*")
st.write("Upload a photo of your handwritten lab record to digitize the code instantly.")

# 4. Inputs
col1, col2 = st.columns([2, 1])
with col1:
    img_file = st.file_uploader("Upload Image (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
with col2:
    lang = st.selectbox("Language", ["C", "Java", "Python", "C++"])

# 5. Execution Logic
if img_file:
    # Display the image preview
    input_image = Image.open(img_file)
    st.image(input_image, caption="Captured Script", use_container_width=True)
    
    if st.button("Synthesize Code ✨"):
        with st.spinner(f"Scriptox.ai is analyzing your {lang} code..."):
            try:
                # Prompt Engineering for high-accuracy code extraction
                prompt_text = (
                    f"You are a professional {lang} developer. "
                    f"OCR the handwritten code in this image. "
                    f"Correct minor syntax errors (missing semicolons, brackets). "
                    f"Return ONLY the code. Do not include any conversational text."
                )
                
                # Multi-modal generation call
                response = client.models.generate_content(
                    model='gemini-1.5-flash', 
                    contents=[prompt_text, input_image]
                )

                # Output formatting
                if response.text:
                    st.success("Synthesis Successful!")
                    st.subheader("🚀 Digital Code:")
                    st.code(response.text, language=lang.lower())
                    
                    # Download button for the user
                    st.download_button(
                        label="Download .txt",
                        data=response.text,
                        file_name=f"scriptox_output.txt",
                        mime="text/plain"
                    )
                else:
                    st.warning("Could not extract text. Please ensure the image is clear.")

            except Exception as e:
                st.error(f"Synthesis Error: {e}")
                st.info("Check if your API key is restricted or if the model is busy.")

# 6. Footer
st.markdown("---")
st.caption("Powered by Google Gemini 1.5 Flash")