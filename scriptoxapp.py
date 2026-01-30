import streamlit as st
from google import genai
from google.genai import types  # Required for proper PDF handling
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Scriptox.ai", page_icon="📜", layout="centered")

# 2. Authentication & Client Setup
if "GEMINI_API_KEY" in st.secrets:
    try:
        # Initializing the client with stable v1 to avoid common 404 errors
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"],
            http_options={'api_version': 'v1'}
        )
    except Exception as e:
        st.error(f"Client Init Error: {e}")
        st.stop()
else:
    st.error("🔑 API Key not found. Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# 3. User Interface
st.title("📜 Scriptox.ai")
st.markdown("### *Handwriting & PDF-to-Code Synthesis Engine*")
st.info("Bridge the gap between your physical lab records and digital IDE.")

# 4. Multi-Format File Uploader
file_input = st.file_uploader("Upload Lab Record (PDF/JPG/PNG)", type=['pdf', 'jpg', 'png', 'jpeg'])
lang = st.selectbox("Target Programming Language", ["C", "Java", "Python", "C++"])

# 5. Processing Logic
if file_input:
    # Prepare the input for Gemini 2.5 Flash
    if file_input.type == "application/pdf":
        # FIX: Using types.Part.from_bytes to prevent Pydantic validation errors
        input_data = types.Part.from_bytes(
            data=file_input.read(), 
            mime_type="application/pdf"
        )
        st.info("📑 PDF Document detected. Ready for synthesis.")
    else:
        # Standard image processing for handwritten notes
        image_bytes = file_input.read()
        input_data = types.Part.from_bytes(
            data=image_bytes,
            mime_type=file_input.type
        )
        st.image(Image.open(io.BytesIO(image_bytes)), caption="Script Preview", use_container_width=True)

    if st.button("Synthesize Code ✨"):
        with st.spinner(f"Scriptox-AI is analyzing your {lang} code..."):
            try:
                # Optimized prompt for code extraction and syntax repair
                prompt_text = (
                    f"You are an expert {lang} developer. Extract the code from this document. "
                    f"If handwritten, fix transcription errors (like mistaking '1' for 'l'). "
                    f"Ensure perfect indentation and fix any missing semicolons or brackets. "
                    f"Return ONLY the clean code block."
                )
                
                # Gemini 2.5 Flash handles multimodal PDF/Image synthesis natively
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt_text, input_data]
                )

                if response.text:
                    st.success("Synthesis Successful!")
                    st.subheader("🚀 Resulting Source Code:")
                    st.code(response.text, language=lang.lower())
                    
                    # One-click download for student workflow
                    st.download_button(
                        label="Download File",
                        data=response.text,
                        file_name=f"scriptox_output.{lang.lower() if lang != 'C++' else 'cpp'}",
                        mime="text/plain"
                    )
                else:
                    st.warning("No code could be synthesized. Please try a clearer scan.")

            except Exception as e:
                st.error(f"Synthesis Error: {e}")