from dotenv import load_dotenv # type: ignore
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Get API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key is missing. Check your .env file.")
else:
    genai.configure(api_key=api_key)

# Initialize AI Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get AI response
def get_gemini_response(input_text, image):
    if input_text and image:
        response = model.generate_content([input_text, image])
        return response.text
    elif input_text:
        response = model.generate_content(input_text)
        return response.text
    else:
        return "Please provide text or an image."

# Streamlit UI
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

input_text = st.text_input("Input-prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

if submit:
    if not input_text and not image:
        st.warning("Please provide a prompt or an image.")
    else:
        response = get_gemini_response(input_text, image)
        st.subheader("The Response is")
        st.write(response)
