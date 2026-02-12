import os
import pdfplumber
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Predefined skill set
SKILL_SET = [
    "python", "java", "c++", "sql", "machine learning",
    "data science", "django", "flask", "react",
    "node", "javascript", "html", "css",
    "tensorflow", "pytorch", "aws", "docker"
]

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Store job description temporarily
job_description = ""

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
        return "Please submit a Job Description first."

    resumes = []
    resume_names = []
    resume_texts = []

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
        return "No resumes uploaded."

    # TF-IDF Similarity
    documents = [job_description.lower()] + resumes
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    ranked = []

    for i, resume_text in enumerate(resumes):
        matched_skills = []

        for skill in SKILL_SET:
            if skill in job_description.lower() and skill in resume_text:
                matched_skills.append(skill)

        # Count required skills in JD
        required_skills = [skill for skill in SKILL_SET if skill in job_description.lower()]

        if len(required_skills) == 0:
            skill_score = 0
        else:
            skill_score = len(matched_skills) / len(required_skills)

        # Final score (weighted)
        final_score = (0.7 * similarity_scores[i]) + (0.3 * skill_score)

        ranked.append((resume_names[i], final_score, skill_score))

    # Sort by final score
    ranked = sorted(ranked, key=lambda x: x[1], reverse=True)

    return render_template("results.html", ranked=ranked)


if __name__ == "__main__":
    app.run(debug=True)