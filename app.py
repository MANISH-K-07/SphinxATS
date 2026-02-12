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

    # Extract text from all uploaded resumes
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.endswith(".pdf"):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            text = ""

            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            resumes.append(text)
            resume_names.append(filename)

    if not resumes:
        return "No resumes uploaded."

    # Add job description to list
    documents = [job_description] + resumes

    # Convert to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compute similarity between JD and resumes
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Combine names and scores
    ranked = sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True)

    return render_template("results.html", ranked=ranked)


if __name__ == "__main__":
    app.run(debug=True)
