# 🎯 ATS parser

A Streamlit-based web application that compares a job description with a resume to calculate a similarity percentage and provides insightful visual feedback.

---

## 🚀 Features

- Upload your resume as a PDF.
- Input a job description.
- Get a similarity percentage score.
- View graphical insights:
  - Resume quality categorized into Excellent, Decent, or Needs Improvement.
  - Suggestions to enhance skills or projects.
- Extract key sections from the resume (e.g., Skills, Experience, Education).
- Highlight the candidate's name extracted from the resume.

---

## 🛠️ Technologies Used

- **Streamlit**: For building the web interface.
- **Python**: Backend processing.
- **spaCy**: Natural Language Processing.
- **scikit-learn**: Cosine similarity for text matching.
- **PyPDF2**: PDF parsing.
- **Matplotlib**: Graphical visualizations.


---

## 📝 How to Run Locally

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/resume-matching-tool.git
   cd resume-matching-tool

---
Install dependencies: ```pip install -r requirements.txt```

---
Run the Streamlit app:```streamlit run app.py```

