import streamlit as st
import re
import io
from pypdf import PdfReader

st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Legal Document Analyzer")
st.write("Upload a legal document to extract important information.")

uploaded_file = st.file_uploader(
    "Upload your legal document",
    type=["pdf", "txt"]
)

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8", errors="ignore")

def analyze_document(text):

    dates = re.findall(
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        text
    )

    amounts = re.findall(
        r'(?:₹|Rs\.?|INR|\$)\s?[\d,]+(?:\.\d{1,2})?',
        text,
        re.IGNORECASE
    )

    keywords = [
        "Agreement", "Payment", "Termination",
        "Confidentiality", "Liability",
        "Jurisdiction", "Obligation"
    ]

    clauses = []
    for keyword in keywords:
        if keyword.lower() in text.lower():
            clauses.append(keyword)

    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary = " ".join(sentences[:5])

    return dates, amounts, clauses, summary

if uploaded_file:
    try:
        document_text = extract_text(uploaded_file)

        if not document_text.strip():
            st.warning("No readable text found in this document.")
        else:
            dates, amounts, clauses, summary = analyze_document(
                document_text
            )

            st.success("Document analyzed successfully!")

            st.subheader("Document Summary")
            st.write(summary)

            st.subheader("Extracted Dates")
            st.write(dates if dates else "No dates found.")

            st.subheader("Extracted Amounts")
            st.write(amounts if amounts else "No amounts found.")

            st.subheader("Important Clauses")
            st.write(clauses if clauses else "No matching clauses found.")

            with st.expander("View Full Extracted Text"):
                st.text(document_text)

    except Exception as error:
        st.error(f"Unable to analyze document: {error}")

st.caption(
    "This tool provides basic text extraction, not legal advice."
)
