# 🐍 SphinxATS

### Automated Resume Screening & Ranking System (Flask + NLP)

SphinxATS is a Flask-based web application that automates resume screening and ranking based on job descriptions using Natural Language Processing techniques. This system demonstrates how Machine Learning can assist HR professionals in filtering and ranking candidates efficiently.

📄 **Published:** [*"SphinxATS: A Multi-Attribute AI-based Decision Support System for Automated Resume Screening and Candidate Ranking"* (IEEE ICSSAS 2026)](https://ieeexplore.ieee.org/document/11559449)


---

## 📌 Project Overview

SphinxATS allows:

* HR to submit a Job Description
* Applicants to upload resumes (PDF)
* Automatic ranking of resumes based on:

  * TF-IDF Similarity
  * Skill Matching
  * Experience Matching

The system generates a ranked list of applicants along with:

* Final Score
* Similarity Score
* Skill Match Score
* Experience Score
* Matched Skills

---

## 🧠 Features

* 📄 PDF Resume Upload
* 📝 Job Description Submission
* 🔍 TF-IDF + Cosine Similarity Scoring
* 🧩 Skill-Based Matching (Predefined Technical Skills)
* 🕒 Experience Detection using Regex
* 📊 Weighted Final Score Calculation
* 📋 Ranked Resume Results Table
* 🧹 Clear Uploaded Resumes Option
* 🧑‍💼 HR Dashboard Interface
* ⚙️ Real-time Resume Ranking

---

## ⚙️ Resume Ranking Methodology

Each uploaded resume is evaluated using three major parameters:

### 1️⃣ Similarity Score

Measures how closely a resume matches the Job Description using:

* TF-IDF Vectorization
* Cosine Similarity

### 2️⃣ Skill Match Score

Matches resume content with predefined technical skills such as:

* Python
* Java
* SQL
* Machine Learning
* Data Science
* HTML / CSS / JavaScript
* Flask / Django
* C / C++
* Git
* NLP

### 3️⃣ Experience Score

Detects candidate experience using Regex patterns like:

* "2 years experience"
* "3+ years"
* "Worked for 4 yrs"

Experience score is normalized before contributing to the final score.

---

## 🧮 Final Score Calculation

Final Ranking Score is calculated as:

```
Final Score =
0.6 × Similarity Score +
0.3 × Skill Match Score +
0.1 × Experience Score
```

Resumes are ranked in descending order based on this score.

---

## 🛠️ Technologies Used

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python 3     | Backend Logic              |
| Flask        | Web Framework              |
| scikit-learn | TF-IDF & Cosine Similarity |
| pdfplumber   | PDF Text Extraction        |
| HTML / CSS   | Frontend UI                |
| Bootstrap 5  | UI Styling                 |
| Regex        | Experience Detection       |

---

## 📂 Project Structure

```
SphinxATS/
│
├── app.py
├── requirements.txt
├── README.md
├── uploads/
├── static/
│   └── style.css
├── templates/
│   ├── login.html
│   ├── hr.html
│   ├── applicant.html
│   ├── results.html
│   ├── message.html
│   ├── debug_vectors.html
│   └── 403.html
└── venv/
```

---

## 🚀 Installation & Setup

### 1️⃣ Move into Project Directory

```
cd SphinxATS
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

```
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run Application

```
python app.py
```

Open in Browser:

```
http://127.0.0.1:5000/
```

### Standalone Desktop Executable

The Flask-based ATS system is packaged into a standalone desktop executable using PyInstaller to enable one-click deployment without requiring Python environment setup on the host system.

Double click:

```
SphinxATS.exe
```

📦 Want to Distribute?

```
dist/SphinxATS.exe
```

---

## ⚠️ Limitations

* Uses predefined skill list
* Experience detection based on Regex
* No database integration
* No authentication system
* Runs on local server only

---

## 🔮 Future Improvements

* NLP-based automatic skill extraction
* Resume feedback suggestions
* Database integration (MySQL / MongoDB)
* HR & Applicant Login System
* Cloud Deployment (AWS / Render)

---

## 🎓 Academic Purpose

This project was developed as a **B.Tech Final Year Capstone Project** to demonstrate:

* Web Development using Flask
* Machine Learning Concepts (TF-IDF & Cosine Similarity)
* Natural Language Processing Basics
* Resume Ranking Automation Logic

---
