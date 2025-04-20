import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
import tempfile
import os
import shutil

tesseract_path = shutil.which('tesseract')
st.write("🔍 Tesseract path found:", tesseract_path)

if not tesseract_path:
    st.error("❌ Tesseract is not installed or not found in PATH!")
else:
    st.success("✅ Tesseract is installed and found.")
# Title
st.title("OCR & Translation App ")
st.markdown("Upload an image or PDF, extract English text and translate it to Hindi.")

# Upload file
uploaded_file = st.file_uploader("Choose an image or PDF file", type=["png", "jpg", "jpeg", "pdf"])

# Translator
translator = Translator()

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def translate_to_hindi(text):
    try:
        translated = translator.translate(text, src='en', dest='hi')
        return translated.text
    except Exception as e:
        return f"Translation Error: {e}"

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_ext in ['.png', '.jpg', '.jpeg']:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image)
            st.subheader("Extracted Text")
            st.text(extracted_text)

        with st.spinner("Translating to Hindi..."):
            hindi_text = translate_to_hindi(extracted_text)
            st.subheader("Translated Text (Hindi)")
            st.text(hindi_text)

    elif file_ext == '.pdf':
        from pdf2image import convert_from_bytes
        with st.spinner("Converting PDF to image..."):
            images = convert_from_bytes(uploaded_file.read(), dpi=300)
            for i, img in enumerate(images):
                st.image(img, caption=f'Page {i+1}', use_column_width=True)
                extracted_text = extract_text_from_image(img)
                st.subheader(f"Extracted Text - Page {i+1}")
                st.text(extracted_text)

                hindi_text = translate_to_hindi(extracted_text)
                st.subheader(f"Translated Text (Hindi) - Page {i+1}")
                st.text(hindi_text)

    else:
        st.error("Unsupported file format.")

