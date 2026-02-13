import re
import os
import pdfplumber
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
app.secret_key = "supersecretkey"   # Required for session handling

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
# Role Protection Decorator
# ----------------------------------
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "role" not in session or session["role"] != role:
                return render_template("403.html"), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ----------------------------------
# Intelligent Skill Extraction
# ----------------------------------
def extract_skills_from_jd(jd_text):
    jd_text = jd_text.lower()
    extracted = []

    for skill in TECH_SKILLS:
        if skill in jd_text:
            extracted.append(skill)

    return extracted

# ----------------------------------
# AI/ML Feature Vector Extraction
# ----------------------------------
def get_resume_vector(text):
    """
    Create binary skill vector for clustering.
    Experience is NOT included.
    """

    required_skills = extract_skills_from_jd(job_description)

    vector = []

    for skill in required_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            vector.append(1)
        else:
            vector.append(0)

    return vector

@app.route("/debug_vectors")
@role_required("hr")
def debug_vectors():
    """
    Temporary page to check vector extraction for uploaded resumes.
    """
    if job_description == "":
        return render_template("message.html", message="Please submit a Job Description first.")

    required_skills = extract_skills_from_jd(job_description)

    jd_exp_match = re.search(r'(\d+)\s+years', job_description.lower())
    jd_exp = int(jd_exp_match.group(1)) if jd_exp_match else 1

    output = []

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            vector = get_resume_vector(text, jd_exp)
            output.append({
                "resume": filename,
                "vector": vector
            })

    return render_template("debug_vectors.html", vectors=output)

# ----------------------------------
# Login Page
# ----------------------------------
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    role = request.form.get("role")

    if role in ["applicant", "hr"]:
        session["role"] = role
        return redirect(url_for(f"{role}_dashboard"))

    return render_template("message.html", message="Invalid role selected")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ----------------------------------
# Applicant Dashboard
# ----------------------------------
@app.route("/applicant")
@role_required("applicant")
def applicant_dashboard():
    return render_template("applicant.html")

@app.route("/upload", methods=["POST"])
@role_required("applicant")
def upload_resume():
    if "resume" not in request.files:
        return render_template("message.html", message="No file part")

    file = request.files["resume"]

    if file.filename == "":
        return render_template("message.html", message="No selected file")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    return render_template("message.html", message="Resume uploaded successfully!")

# ----------------------------------
# HR Dashboard
# ----------------------------------
@app.route("/hr")
@role_required("hr")
def hr_dashboard():
    return render_template("hr.html")

@app.route("/submit_jd", methods=["POST"])
@role_required("hr")
def submit_jd():
    global job_description
    job_description = request.form["jd_text"]
    return render_template("message.html", message="Job Description Submitted Successfully!")

@app.route("/rank")
@role_required("hr")
def rank_resumes():
    global job_description

    if job_description == "":
        return render_template("message.html", message="Please submit a Job Description first.")

    resumes = []
    resume_names = []
    vectors = []

    # Extract JD experience
    jd_exp_match = re.search(r'(\d+)\s+years', job_description.lower())
    jd_exp = int(jd_exp_match.group(1)) if jd_exp_match else 1

    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            text = ""

            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            text = text.lower()
            resumes.append(text)
            resume_names.append(filename)

            # Generate ML vector
            vector = get_resume_vector(text)
            vectors.append(vector)

    if not resumes:
        return render_template("message.html", message="No resumes uploaded.")

    # -------------------------
    # KMeans Clustering
    # -------------------------
    if len(vectors) >= 2:
        kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(np.array(vectors))
    else:
        cluster_labels = [0] * len(vectors)

    # -------------------------
    # TF-IDF Similarity
    # -------------------------
    documents = [job_description.lower()] + resumes
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:]
    ).flatten()

    required_skills = extract_skills_from_jd(job_description)

    ranked = []

    for i, resume_text in enumerate(resumes):

        matched_skills = []

        for skill in required_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, resume_text):
                matched_skills.append(skill)

        skill_score = (
            len(matched_skills) / len(required_skills)
            if required_skills else 0
        )

        resume_exp_match = re.search(r'(\d+)\s+years', resume_text)

        if resume_exp_match:
            resume_exp = int(resume_exp_match.group(1))
            exp_score = 1 if resume_exp >= jd_exp else resume_exp / jd_exp
        else:
            exp_score = 0.5

        final_score = (
            (0.6 * similarity_scores[i]) +
            (0.3 * skill_score) +
            (0.1 * exp_score)
        )

        ranked.append({
            "name": resume_names[i],
            "final_score": round(final_score, 3),
            "skill_score": round(skill_score, 3),
            "exp_score": round(exp_score, 3),
            "skill_percent": int(skill_score * 100),
            "matched_skills": matched_skills,
            "cluster": int(cluster_labels[i])
        })

    ranked = sorted(ranked, key=lambda x: x["final_score"], reverse=True)

    # -------------------------
    # Cluster Summary Creation
    # -------------------------

    cluster_summary = {}

    for resume in ranked:
        cluster = resume["cluster"]
        cluster_summary.setdefault(cluster, {
            "resumes": [],
            "skills": []
        })

        cluster_summary[cluster]["resumes"].append(resume["name"])
        if resume["skill_score"] > 0:
            cluster_summary[cluster]["skills"].extend(resume["matched_skills"])

    # Compute dominant skills per cluster
    for cluster, data in cluster_summary.items():

        skill_counts = {}

        for skill in data["skills"]:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)

        top_skills = [skill for skill, count in sorted_skills[:3]]

        data["top_skills"] = top_skills
        data["resume_count"] = len(data["resumes"])

    return render_template("results.html", ranked=ranked, cluster_summary=cluster_summary)

@app.route("/clear")
@role_required("hr")
def clear_resumes():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return render_template("message.html", message="All resumes cleared successfully!")
    

if __name__ == "__main__":
    app.run(debug=True)
