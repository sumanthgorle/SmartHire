# SmartHire - AI-Powered Recruitment Platform

SmartHire is a full-stack recruitment platform built using Python and Django.

It connects candidates with companies and provides resume-based job matching using skill matching and NLP techniques.

---

## Features

### Candidate Features

- Candidate registration and login
- Candidate profile
- Browse available jobs
- View job details
- Upload PDF resume
- Extract skills from resume
- Apply for jobs
- Prevent duplicate applications
- View submitted applications
- Track application status
- View resume-to-job match percentage
- View matched and missing skills
- Receive skill recommendations

### Company Features

- Company registration and login
- Company profile
- Create and post jobs
- View company jobs
- View applicants
- View candidate profile information
- Analyze candidate resumes
- View skill match percentage
- View AI/NLP match percentage
- View final match score
- View matched and missing skills
- Update application status

### AI/NLP Features

SmartHire uses:

- TF-IDF Vectorization
- Cosine Similarity
- Resume text analysis
- Skill extraction
- Rule-based skill matching

The final matching score combines:

- 70% skill matching
- 30% AI/NLP matching

---

## Technologies Used

### Backend

- Python
- Django
- Django REST Framework

### Frontend

- HTML
- CSS
- JavaScript

### Database

- SQLite for the current development setup
- MySQL support configured through `mysqlclient`

### AI/NLP

- Scikit-learn
- TF-IDF
- Cosine Similarity

### Resume Processing

- pypdf

### Development Tools

- VS Code
- Git
- GitHub

---

## Project Structure

```text
SmartHire/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── jobs/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── applications/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── resumes/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── utils.py
│   └── urls.py
│
├── ai_matching/
│   └── services.py
│
├── smarthire/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│
├── static/
│   └── css/
│       └── style.css
│
├── media/
│   └── resumes/
│
└── venv/