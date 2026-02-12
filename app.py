import re
import os
import pdfplumber
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Store job description temporarily
job_description = ""

# ----------------------------------
# Master Technical Skills Dataset
# ----------------------------------
TECH_SKILLS = [
    "python", "java", "c++", "c programming", "sql",
    "machine learning", "deep learning",
    "data science", "data analysis",
    "flask", "django", "react", "angular",
    "node", "nodejs", "javascript",
    "html", "css", "bootstrap",
    "tensorflow", "pytorch", "keras",
    "aws", "azure", "gcp",
    "docker", "kubernetes",
    "mongodb", "mysql", "postgresql",
    "git", "linux", "pandas", "numpy",
    "opencv", "nlp", "power bi", "tableau"
]

# ----------------------------------
# Intelligent Skill Extraction
# ----------------------------------
def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    extracted = []

    for skill in TECH_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_text):
            extracted.append(skill)

    return extracted


# ----------------------------------
# Smarter Experience Extraction
# ----------------------------------
def extract_experience(text):
    text = text.lower()

    # Handles: 2 years, 2+ years, 3 yrs, 4 yr, etc.
    pattern = r'(\d+)\s*\+?\s*(years|year|yrs|yr)'

    matches = re.findall(pattern, text)

    if not matches:
        return None

    years = [int(match[0]) for match in matches]

    return max(years)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return "No file part"

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return f"Resume uploaded successfully: {file.filename}"

    return "Upload failed"


@app.route("/submit_jd", methods=["POST"])
def submit_jd():
    global job_description
    job_description = request.form["jd_text"]
    return "Job Description Submitted Successfully!"


@app.route("/rank")
def rank_resumes():
    global job_description

    if job_description == "":
        return render_template("message.html", message="Please submit a Job Description first.")

    resumes = []
    resume_names = []

    # Extract text from resumes
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            text = ""

            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            resumes.append(text.lower())
            resume_names.append(filename)

    if not resumes:
        return render_template("message.html", message="No resumes uploaded.")

    # ----------------------------------
    # Extract Required Skills
    # ----------------------------------
    required_skills = extract_skills_from_jd(job_description)

    # ----------------------------------
    # TF-IDF Similarity
    # ----------------------------------
    documents = [job_description.lower()] + resumes
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:]
    ).flatten()

    ranked = []

    for i, resume_text in enumerate(resumes):

        # ----------------------------------
        # Skill Matching (Safe Regex)
        # ----------------------------------
        matched_skills = []

        for skill in required_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, resume_text):
                matched_skills.append(skill)

        skill_score = (
            len(matched_skills) / len(required_skills)
            if required_skills else 0
        )

        # ----------------------------------
        # Experience Scoring (Improved)
        # ----------------------------------
        jd_exp = extract_experience(job_description)
        resume_exp = extract_experience(resume_text)

        if jd_exp and resume_exp:
            if resume_exp >= jd_exp:
                exp_score = 1
            else:
                exp_score = resume_exp / jd_exp
        else:
            exp_score = 0.5  # default if unclear

        # ----------------------------------
        # Final Weighted Score
        # ----------------------------------
        final_score = (
            (0.6 * similarity_scores[i]) +
            (0.3 * skill_score) +
            (0.1 * exp_score)
        )

        ranked.append((
            resume_names[i],
            round(final_score, 3),
            round(skill_score, 3),
            matched_skills,
            round(exp_score, 3)
        ))

    # Sort by final score
    ranked = sorted(ranked, key=lambda x: x[1], reverse=True)

    return render_template(
        "results.html",
        ranked=ranked,
        required_skills=required_skills
    )


@app.route("/clear")
def clear_resumes():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return "All resumes cleared successfully! <br><br><a href='/'>Go Back</a>"


if __name__ == "__main__":
    app.run(debug=True)
