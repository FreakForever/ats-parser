from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy
from PyPDF2 import PdfReader
import streamlit as st
import matplotlib.pyplot as plt

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Function to extract name from text
def extract_name(text):
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    return match.group() if match else "Name not found"

# Text preprocessing function
def text_preprocess(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

# Extract sections of resume
def extract_sections(text):
    sections = {
        'skills': re.search(r'Skills:?(.*?)(Experience|Education|$)', text, re.S),
        'experience': re.search(r'Experience:?(.*?)(Skills|Education|$)', text, re.S),
        'education': re.search(r'Education:?(.*?)(Experience|Skills|$)', text, re.S)
    }
    return {key: match.group(1).strip() if match else '' for key, match in sections.items()}

# Calculate similarity
def calculate_similarity(resume_text, job_text):
    resume_text = text_preprocess(resume_text)
    job_text = text_preprocess(job_text)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2]).flatten()[0]
    return similarity * 100  # Convert to percentage

# Streamlit UI
st.title("🎯 Resume Matching Tool")

st.sidebar.title("📄 Upload Your Resume")
uploaded_file = st.sidebar.file_uploader("Choose a resume PDF file", type="pdf")

st.sidebar.title("📝 Enter Job Description")
job_description = st.sidebar.text_area("Enter the job description here:")

# Main Content
st.write("Upload your resume and input the job description to check the similarity score.")

if uploaded_file is not None:
    # Extract resume text from PDF
    pdf_reader = PdfReader(uploaded_file)
    resume_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        resume_text += page.extract_text() or ""

    st.write("✅ Resume Uploaded Successfully!")
    st.write("### Extracted Resume Text (Optional Preview):")
    st.text_area("Resume Text", resume_text, height=150)
else:
    st.write("📂 Please upload a PDF resume.")

if st.sidebar.button("Calculate Similarity"):
    if uploaded_file is not None and job_description:
        # Extract sections and calculate similarity
        sections = extract_sections(resume_text)
        skills_experience = sections['skills'] + ' ' + sections['experience']

        # Calculate similarity
        with st.spinner("Analyzing the resume..."):
            similarity_score = calculate_similarity(skills_experience, job_description)

        # Display similarity score
        st.success("✅ Analysis Complete!")
        st.write(f"### Similarity Score: **{similarity_score:.2f}%** 🎉")

        # Provide feedback based on the score
        if similarity_score >= 70:
            feedback = "🟢 Very Good: Your resume matches well with the job description!"
        elif 40 <= similarity_score < 70:
            feedback = "🟡 Decent: Consider adding more relevant skills and experience."
        else:
            feedback = "🔴 Needs Improvement: Add more relevant projects and skills."

        st.write(f"### Feedback: {feedback}")

        # Plot the score with predefined ranges
        ranges = ['Not Good (<40%)', 'Decent (40%-69%)', 'Very Good (70%-100%)']
        scores = [30, 55, 85]  # Average values for each range
        colors = ['red', 'yellow', 'green']
        current_score_index = 0 if similarity_score < 40 else (1 if similarity_score < 70 else 2)

        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(ranges, scores, color=colors, alpha=0.7)
        bars[current_score_index].set_color('blue')  # Highlight the current range
        ax.bar_label(bars, fmt='%.0f%%')
        ax.set_title("Resume Match Feedback")
        ax.set_ylabel("Percentage")
        ax.set_ylim(0, 100)

        st.pyplot(fig)

    else:
        st.error("🚫 Please upload a resume and enter a job description to calculate similarity.")

# Footer for better engagement
st.sidebar.info("🔍 Powered by SpaCy, PyPDF2, Matplotlib, and Streamlit.")
