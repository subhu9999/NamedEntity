import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import spacy
import subprocess
import sys

def install_model():
    """Function to install en_core_web_trf model if not already installed."""
    try:
        # Try loading the model to check if it's already installed
        spacy.load("en_core_web_trf")
        print("Model is already installed.")
    except OSError:
        # If not installed, install the model
        print("Model not found. Installing en_core_web_trf...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_trf"])


# Function to load the model
def load_model():
    """Load the transformer-based model"""
    install_model()
    nlp = spacy.load("en_core_web_trf")
    return nlp


# Load SpaCy model
#nlp = spacy.load("en_core_web_trf")

nlp = load_model()

# Title and description
st.title("Named Entity Recognization")
st.write("Upload a PDF to scan for names or company names.")


# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Function to extract text from image
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text


# Function to extract names/organizations using SpaCy
def extract_entities(text):
    doc = nlp(text)
    names = []
    companies = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names.append(ent.text)
        elif ent.label_ == "ORG":
            companies.append(ent.text)
    return names, companies


# File upload options
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Process PDF
    if uploaded_file.type == "application/pdf":
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.success("Analysis complete!")

    # Process Image
    else:
        with st.spinner("Extracting text from Image..."):
            extracted_text = extract_text_from_image(uploaded_file)
            st.success("Text extracted from Image!")


    # Analyze text with SpaCy
    with st.spinner("Analyzing text for names and companies..."):
        names, companies = extract_entities(extracted_text)

    # Display warnings
    st.subheader("Entities found")
    if names:
        st.warning(f"Names Detected: {', '.join(set(names))}")
    else:
        st.success("No names detected.")

    if companies:
        st.warning(f"Company Names Detected: {', '.join(set(companies))}")
    else:
        st.success("No company names detected.")

    # Display extracted text
    # st.subheader("Extracted Text")
    # st.text_area("Document Text", extracted_text, height=300)