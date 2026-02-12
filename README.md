# 🐍 SphinxATS  
### Automated Resume Screening & Ranking System

SphinxATS is a Flask-based web application that automates resume screening and ranking based on job descriptions using Natural Language Processing techniques.

---

## 📌 Project Overview

SphinxATS allows:

- HR to submit a Job Description
- Applicants to upload resumes (PDF)
- Automatic ranking of resumes based on:
  - TF-IDF similarity
  - Skill matching
  - Experience matching

The system generates a ranked list with score breakdown and matched skills.

---

## 🧠 Features

- 📄 PDF Resume Upload
- 📝 Job Description Submission
- 🔍 TF-IDF + Cosine Similarity Scoring
- 🧩 Skill-Based Matching (Predefined Skill Set)
- 🕒 Experience-Based Scoring (Regex Detection)
- 📊 Weighted Final Score Calculation
- 📋 Ranked Results Table
- 🧹 Clear Uploaded Resumes
- 🎨 Bootstrap UI with Custom Styling

---

## 🛠️ Technologies Used

- Python 3
- Flask
- scikit-learn
- pdfplumber
- HTML
- Bootstrap 5
- Custom CSS

---

## ⚙️ How It Works

1. Extract text from uploaded PDF resumes.
2. Convert Job Description and resumes into TF-IDF vectors.
3. Compute cosine similarity.
4. Match predefined technical skills.
5. Detect years of experience using regex.
6. Compute final weighted score:

Final Score =  
0.6 × Similarity Score  
+ 0.3 × Skill Match Score  
+ 0.1 × Experience Score  

7. Display ranked results with matched skills.

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
│ └── style.css
├── templates/
│ ├── index.html
│ ├── results.html
│ └── message.html
└── venv/
```


---

## 🚀 Installation & Setup

### 1️⃣ Clone or Copy Project Folder

Move into project directory:

```
cd SphinxATS
```


---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

---

### 3️⃣ Install Required Packages

```
pip install -r requirements.txt
```

---

### 4️⃣ Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000/
```

---

## ⚠️ Limitations

- Uses predefined skill list (not dynamic NLP extraction)
- Experience detection based on simple regex
- No database persistence
- No authentication system

---

## 🔮 Future Improvements

- NLP-based automatic skill extraction
- User authentication (HR & Applicant roles)
- Database integration
- Resume feedback suggestions
- Deployment on cloud platform

---

## 🎓 Academic Purpose

This was developed as a B.Tech capstone project to demonstrate:

- Web development using Flask
- Machine Learning (TF-IDF & Cosine Similarity)
- Text processing & NLP basics
- Resume ranking automation logic

---
