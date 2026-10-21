# 🎓 PlacementIQ: AI-Powered Student Placement Prediction & Career Intelligence System

> **BCA Final-Year Academic Project**  
> An enterprise-grade, explainable machine learning platform bridging campus placement prediction, resume intelligence, corporate eligibility auditing, skills gap analysis, and personalized 60-day action plans.

---

## 🌟 Key Features

1. **Supervised ML Placement Prediction**
   - Preserves canonical 5-parameter schema: **CGPA, Aptitude Test Score, Completed Projects, Completed Internships, Workshops/Certifications**.
   - Compares **Logistic Regression**, **Decision Trees**, and **Random Forests** using Stratified 5-Fold Cross-Validation.
   - Outputs calibrated placement probabilities and explainable feature contributions.

2. **Resume Intelligence & ATS Audit**
   - Secure, in-memory text parsing for **PDF** (via PyMuPDF) and **DOCX** (via python-docx).
   - Automatically sanitizes documents and warns against scanned/image-only PDFs.
   - Categorizes technical and soft skills across 8 industry domains.
   - Audits essential sections (*Education, Experience, Projects, Skills, Certifications*) and generates an objective 100-point completeness score.

3. **Multi-Tier Corporate Eligibility Pre-Screening**
   - Compares candidate profiles against realistic recruitment criteria:
     - **Tier-1 Product / Tech MNC** (*Google, Microsoft, Amazon*)
     - **Tier-2 Enterprise & Fintech** (*Oracle, Cisco, JPMorgan*)
     - **IT Services & Consultancies** (*TCS, Infosys, Wipro, Accenture*)
     - **High-Growth Tech Startups**
   - Evaluates active backlogs, CGPA thresholds, and portfolio depth.

4. **Role-Based Skills Gap Analysis**
   - Benchmarks student competencies against target roles (*Software Engineer, Full-Stack Developer, Data Scientist / AI Engineer, Cloud & DevOps, Cybersecurity*).
   - Visualizes matching core competencies vs missing high-priority skills.
   - Delivers curated learning roadmaps with recommended repositories and problem sheets.

5. **Personalized 60-Day Career Action Plan**
   - **7-Day Quick Wins:** Immediate fixes for backlog clearance, aptitude speed, and resume formatting.
   - **30-Day Skill Acceleration:** Deep-dive DSA practice and capstone project deployment.
   - **60-Day Placement Readiness:** Commercial internship applications and behavioral/technical mock interviews.

6. **Publication-Grade PDF Dossier Export**
   - One-click PDF generation via **ReportLab**.
   - Includes candidate summary, prediction badge, eligibility audit, skills gap breakdown, and complete action plan.

---

## 📁 System Architecture & Directory Structure

```
student-placement-system/
├── app.py                      # Main Streamlit web application & UI
├── train_model.py              # ML pipeline training, validation & serialization
├── config.py                   # Central constants, taxonomies & eligibility presets
├── requirements.txt            # Reproducible Python dependencies
├── README.md                   # Complete academic documentation & setup guide
├── .gitignore                  # Git ignore rules
├── data/
│   └── placement_dataset.csv   # Statistically validated training dataset
├── models/
│   ├── model_pipeline.pkl      # Fitted Scikit-Learn Scaler + Classifier pipeline
│   └── model_metrics.json      # True evaluated metrics & feature importances
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py        # PDF/DOCX parsing & text sanitization
│   ├── resume_analyzer.py      # Skill extraction, completeness & job matching
│   ├── placement_predictor.py  # Model inference & explainable contributions
│   ├── eligibility_checker.py  # Multi-tier corporate cutoff validation
│   ├── skills_gap_analyzer.py  # Role benchmark & gap detection
│   ├── recommendation_engine.py# 7, 30, and 60-day roadmaps
│   └── report_generator.py     # ReportLab PDF dossier generator
└── tests/
    ├── test_resume_parser.py   # Document validation & security unit tests
    ├── test_prediction.py      # Model bounds & inference tests
    ├── test_eligibility.py     # Academic cutoff & backlog tests
    └── test_skills_gap.py      # Skill matching & roadmap unit tests
```

---

## 🤖 Machine Learning Model Benchmarks

Trained and evaluated on hold-out test records using Stratified 5-Fold Cross Validation:

| Model | Test Accuracy | Precision | Recall | F1-Score | 5-Fold CV F1 |
|---|---|---|---|---|---|
| **Logistic Regression (Best)** | **93.75%** | **87.69%** | **82.61%** | **0.8507** | **0.8733 (±0.041)** |
| Random Forest Classifier | 91.87% | 87.72% | 72.46% | 0.7937 | 0.8222 (±0.030) |
| Decision Tree Classifier | 89.69% | 77.27% | 73.91% | 0.7556 | 0.7634 (±0.043) |

- **Preprocessing:** Features are normalized using `StandardScaler` fitted exclusively on training splits to prevent data leakage.
- **Pipeline:** Preprocessing scaler and model classifier are packaged together in `model_pipeline.pkl`.

---

## 🚀 Installation & Local Execution

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 installed.

### 2. Setup Virtual Environment (Recommended)
```bash
# Navigate to the project directory
cd student-placement-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. (Optional) Re-Train the ML Models
```bash
python train_model.py
```

### 5. Launch the Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Unit Tests

Run the full suite of 17 automated unit tests:
```bash
python -m unittest discover -s tests
```
Output:
```
.................
----------------------------------------------------------------------
Ran 17 tests in 1.1s

OK
```

---

## 🌐 Deployment to Streamlit Cloud

1. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of AI Student Placement Intelligence System"
   git branch -M main
   git remote add origin https://github.com/<your-username>/student-placement-system.git
   git push -u origin main
   ```
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io).
3. Select your repository, branch `main`, and main file path `app.py`.
4. Click **Deploy!**

---

## 🔒 Security & Privacy Practices

- **Zero Data Retention:** Resumes are parsed strictly in memory and discarded after analysis.
- **Input Sanitization:** Text strings are stripped of null bytes and control sequences.
- **Safe Upload Limits:** File size restricted to 5MB, with strict `.pdf` and `.docx` extension verification.
- **No Paid APIs Required:** Entire pipeline runs 100% locally with open-source Scikit-Learn, PyMuPDF, and ReportLab.
