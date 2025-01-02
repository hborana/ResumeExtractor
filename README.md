# Resume Information Extractor 📄

A Streamlit-based web application to extract structured information from resumes using OpenAI's API and Pydantic for data validation. Upload a PDF resume, and this tool will extract key details like name, phone number, email, and experience.

## Features
- Extracts key details (name, email, phone, and experience) from resumes.
- Simple interface for uploading PDF resumes.
- Error handling and validation using Pydantic.
- Clean and well-structured output displayed in a user-friendly layout.

## Installation

Follow these steps to set up and run the application:

### Prerequisites
Ensure the following tools and libraries are installed:
- Python (>= 3.8)
- [pip](https://pip.pypa.io/en/stable/)

### Required Libraries
Install the dependencies by running:

```bash
pip install streamlit openai pydantic pypdf2

Run the Application

streamlit run app.py
