import streamlit as st
from google import genai
from PIL import Image
import io

# 1. Page Configuration - MUST BE FIRST
# Using the yellow script icon as requested
st.set_page_config(page_title="Scriptox.ai", page_icon="📜", layout="centered")

# 2. Authentication & Client Setup
if "GEMINI_API_KEY" in st.secrets:
    try:
        # Forcing 'v1' to avoid the v1beta 404 error common in 2026 SDKs
        client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"],
            http_options={'api_version': 'v1'}
        )
    except Exception as e:
        st.error(f"Client Init Error: {e}")
        st.stop()
else:
    st.error("🔑 GEMINI_API_KEY not found in Streamlit Secrets!")
    st.stop()

# 3. User Interface
st.title("📜 Scriptox.ai")
st.markdown("### *Handwriting & PDF-to-Code Synthesis Engine*")
st.write("Upload a photo or a scanned PDF of your lab record to digitize code instantly.")

# 4. Multi-Format File Uploader
# Added PDF support because copy-pasting from scanned/dead PDFs is impossible
file_input = st.file_uploader("Upload Lab Record (PDF/JPG/PNG)", type=['pdf', 'jpg', 'png', 'jpeg'])
lang = st.selectbox("Target Programming Language", ["C", "Java", "Python", "C++"])

# 5. Processing Logic
if file_input:
    # Prepare input for Gemini based on file type
    if file_input.type == "application/pdf":
        # Gemini can process PDF bytes directly for multimodal analysis
        input_data = {"mime_type": "application/pdf", "data": file_input.read()}
        st.info("📑 PDF Document detected. Ready for synthesis.")
    else:
        # Standard image processing for handwritten snapshots
        input_data = Image.open(file_input)
        st.image(input_data, caption="Preview of Script", use_container_width=True)

    if st.button("Synthesize Code ✨"):
        with st.spinner(f"Scriptox-AI is extracting your {lang} code..."):
            try:
                # Instructions to OCR and fix syntax errors (e.g., missing semicolons)
                prompt_text = (
                    f"You are an expert {lang} developer. "
                    f"Extract the code from this document. If it is handwritten, "
                    f"correct transcription errors. If it is a scan, fix indentation. "
                    f"Return ONLY the code block."
                )
                
                # Using Gemini 2.5 Flash for high-speed multimodal extraction
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt_text, input_data]
                )

                if response.text:
                    st.success("Synthesis Successful!")
                    st.subheader("🚀 Digital Code:")
                    st.code(response.text, language=lang.lower())
                    
                    # Provide a download option for the student
                    st.download_button(
                        label="Download Source Code",
                        data=response.text,
                        file_name=f"scriptox_output.{lang.lower() if lang != 'C++' else 'cpp'}",
                        mime="text/plain"
                    )
                else:
                    st.warning("No code detected. Please ensure the document is clear.")

            except Exception as e:
                st.error(f"Synthesis Error: {e}")
                st.info("Tip: If you see a 404, check your API key status in Google AI Studio.")