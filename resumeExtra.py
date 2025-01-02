import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from pydantic import BaseModel, EmailStr, ValidationError
# import json

api_key = "Add the KEY"
client = OpenAI(api_key=api_key)


# Main pydantic model
class ResumeDetails(BaseModel):
    name: str
    email: str
    phone: str
    first_work_experience: str
    
# Function to call OpenAI API for resume information extraction
def extract_resume_info_with_openai(text):
    system_prompt = """
    You are an AI assistant that extracts structured information from resumes.

    When given a resume's text, extract the following fields:
    - Name: The candidate's full name.
    - Phone: Candidate's phone number.
    - Email: Candidate's email.
    - Skills: List of skills (if mentioned, otherwise provide an empty list).

    If a field is not present, provide a default value (e.g., "Not Found" for Name, an empty list for Skills).
    Ensure your response is a valid JSON object.

    If the uploaded document is not a resume, then send a message to upload a resume in PDF format.
    """

    # Call the OpenAI API
    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            response_format=ResumeDetails,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": str(e)})

# Streamlit app to handle resume upload and extraction
st.title("Resume Information Extractor 📄")
st.write("Upload your resume in PDF format, and I'll extract key details.")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a resume (PDF format)", type="pdf")
# Utility function to clean and format work experience
def clean_work_experience(experience: str) -> str:
    # Remove unwanted characters and extra spaces
    cleaned_experience = (
        experience.replace(",", "")
                  .replace("|", "")
                  .strip()
                  .replace("  ", " ")  # Replace multiple spaces with a single space
    )
    return cleaned_experience
if uploaded_file:
    with st.spinner("Reading PDF..."):
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

    # Show the extracted text (optional for debugging)
    st.expander("📜 Extracted Text").write(pdf_text)
    
    # Extract structured information using OpenAI
    if st.button("🚀 Extract Information"):
        st.write("Extracting information using OpenAI...")

        with st.spinner("Processing..."):
            extracted_info = extract_resume_info_with_openai(pdf_text)

        try:
            # Validate and parse response directly using Pydantic
            validated_data = ResumeDetails.parse_raw(extracted_info)
            
            # Display the extracted information in an enhanced layout
            st.success("🎉 Information Extracted Successfully!")
            
            st.subheader("🔍 Extracted Information")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Name:** {validated_data.name}")
                st.markdown(f"**Phone:** {validated_data.phone}")
                st.markdown(f"**Email:** {validated_data.email}")
                
            with col2:
                st.markdown("**Experience:**")
                cleaned_experience = clean_work_experience(validated_data.first_work_experience)
                st.write(cleaned_experience)

            # with col2:
            #     st.markdown("**Experience:**")
            #     st.write(", ".join(validated_data.first_work_experience))
        
        except ValidationError as ve:
            st.error("🚨 Validation Error!")
            st.code(ve.json(), language="json")
        except Exception as e:
            st.error("❌ Failed to process the response!")
            st.code(str(e), language="text")
            
