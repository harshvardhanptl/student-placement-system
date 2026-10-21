"""
Application Configuration and Constants
Student Placement Prediction & Career Intelligence System
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "generated_reports")

DATASET_PATH = os.path.join(DATA_DIR, "placement_dataset.csv")
MODEL_PIPELINE_PATH = os.path.join(MODELS_DIR, "model_pipeline.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")

# Security & Upload Constraints
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = [".pdf", ".docx"]

# Feature Definitions for Prediction Model
MODEL_FEATURES = [
    "CGPA",
    "AptitudeTestScore",
    "Projects",
    "Internships",
    "WorkshopsCertifications"
]

# Standard Company Eligibility Criteria Presets
ELIGIBILITY_PRESETS = {
    "Tier-1 Product / Tech MNC (e.g., Google, Microsoft, Amazon)": {
        "min_cgpa": 7.5,
        "min_aptitude": 75,
        "max_backlogs": 0,
        "min_projects": 2,
        "min_internships": 1,
        "description": "Rigorous filtering, strict no-backlog policy, emphasis on DSA and system design."
    },
    "Tier-2 Enterprise & Fintech (e.g., Oracle, Cisco, JPMorgan)": {
        "min_cgpa": 7.0,
        "min_aptitude": 65,
        "max_backlogs": 0,
        "min_projects": 2,
        "min_internships": 0,
        "description": "Standard corporate eligibility, strong fundamentals in OOP, DBMS, and aptitude."
    },
    "IT Services & Consultancies (e.g., TCS Digital, Infosys, Wipro, Accenture)": {
        "min_cgpa": 6.0,
        "min_aptitude": 55,
        "max_backlogs": 1,
        "min_projects": 1,
        "min_internships": 0,
        "description": "Mass campus drive benchmark; permits cleared backlogs, general aptitude assessment."
    },
    "High-Growth Tech Startups": {
        "min_cgpa": 6.5,
        "min_aptitude": 60,
        "max_backlogs": 1,
        "min_projects": 3,
        "min_internships": 1,
        "description": "Heavy emphasis on practical project portfolios, tech stack proficiency, and internships."
    }
}

# Industry Job Roles and Skill Taxonomies
JOB_ROLES_TAXONOMY = {
    "Software Development Engineer (SDE)": {
        "core_skills": ["Data Structures", "Algorithms", "Java", "Python", "C++", "OOP", "DBMS", "Git"],
        "specialized_skills": ["System Design", "SQL", "Linux", "REST APIs", "Unit Testing", "Docker"],
        "recommended_certifications": ["AWS Certified Developer", "Oracle Certified Java Associate"],
        "aptitude_weight": "High (Technical & Quantitative Aptitude required)",
        "project_recommendations": [
            "Build an end-to-end full-stack web application with user authentication and database persistence.",
            "Implement a scalable distributed task queue or URL shortener focusing on caching and concurrency."
        ]
    },
    "Full-Stack Web Developer": {
        "core_skills": ["JavaScript", "TypeScript", "React", "Node.js", "HTML", "CSS", "SQL", "Git"],
        "specialized_skills": ["MongoDB", "Express", "Next.js", "Docker", "Tailwind CSS", "REST APIs", "GraphQL"],
        "recommended_certifications": ["Meta Front-End/Back-End Professional Certificate"],
        "aptitude_weight": "Moderate (Problem-solving and practical coding assessments)",
        "project_recommendations": [
            "Develop an E-Commerce portal with payment gateway integration, responsive UI, and state management.",
            "Create a collaborative real-time Kanban project management tool using WebSockets."
        ]
    },
    "Data Scientist / AI Engineer": {
        "core_skills": ["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-Learn", "SQL", "Statistics"],
        "specialized_skills": ["Deep Learning", "TensorFlow", "PyTorch", "Data Visualization", "Matplotlib", "Seaborn", "NLP", "Power BI"],
        "recommended_certifications": ["Google Data Analytics Professional Certificate", "IBM AI Engineering"],
        "aptitude_weight": "High (Statistical, Logical, and Quantitative emphasis)",
        "project_recommendations": [
            "Build a production machine learning pipeline with automated data ingestion, model training, and API deployment.",
            "Develop an NLP text analytics or conversational agent application using transformer models."
        ]
    },
    "Cloud & DevOps Engineer": {
        "core_skills": ["Linux", "Bash", "Python", "Git", "Networking", "Docker", "Kubernetes"],
        "specialized_skills": ["AWS", "Azure", "Terraform", "CI/CD", "Jenkins", "Ansible", "Prometheus", "Grafana"],
        "recommended_certifications": ["AWS Certified Solutions Architect Associate", "CKA (Kubernetes Administrator)"],
        "aptitude_weight": "Moderate (Logical reasoning and systems troubleshooting)",
        "project_recommendations": [
            "Automate infrastructure provisioning using Terraform and set up a CI/CD pipeline on GitHub Actions.",
            "Deploy a microservices application on Kubernetes with auto-scaling and monitoring dashboards."
        ]
    },
    "Cybersecurity Analyst": {
        "core_skills": ["Computer Networks", "Linux", "Python", "Cryptography", "Information Security", "Network Protocols"],
        "specialized_skills": ["Wireshark", "Metasploit", "Penetration Testing", "SIEM", "Firewalls", "Vulnerability Assessment", "SOC"],
        "recommended_certifications": ["CompTIA Security+", "Certified Ethical Hacker (CEH)"],
        "aptitude_weight": "Moderate to High (Analytical problem-solving and diagnostic skills)",
        "project_recommendations": [
            "Implement a network packet sniffer and intrusion detection monitor with alert mechanisms.",
            "Perform vulnerability assessments on a mock target environment and document a remediation report."
        ]
    }
}

# Comprehensive Skill Catalog for Resume Parsing
SKILL_DICTIONARY = {
    "Programming Languages": [
        "python", "java", "c", "c++", "c#", "javascript", "typescript", "php", "ruby", "golang",
        "go", "rust", "kotlin", "swift", "dart", "r", "scala", "shell", "bash"
    ],
    "Web & Frontend Technologies": [
        "html", "html5", "css", "css3", "bootstrap", "tailwind", "tailwind css", "javascript", "typescript",
        "react", "react.js", "angular", "angularjs", "vue", "vue.js", "next.js", "redux", "jquery", "sass"
    ],
    "Backend & Frameworks": [
        "node.js", "express", "express.js", "django", "flask", "fastapi", "spring", "spring boot",
        ".net", "asp.net", "laravel", "ruby on rails", "graphql", "rest api", "restful apis", "microservices"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "postgres", "sqlite", "mongodb", "redis", "oracle", "cassandra",
        "mariadb", "firebase", "supabase", "dynamodb", "ms sql server"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes",
        "git", "github", "gitlab", "ci/cd", "jenkins", "terraform", "ansible", "linux", "unix", "nginx"
    ],
    "Data Science & AI": [
        "machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision",
        "data analysis", "pandas", "numpy", "scikit-learn", "scipy", "tensorflow", "keras", "pytorch",
        "matplotlib", "seaborn", "tableau", "power bi", "opencv", "excel"
    ],
    "Core Computer Science": [
        "data structures", "algorithms", "dsa", "object oriented programming", "oop", "oops",
        "dbms", "database management", "operating systems", "computer networks", "software engineering",
        "system design", "agile", "scrum"
    ],
    "Soft Skills": [
        "communication", "teamwork", "leadership", "problem solving", "critical thinking",
        "adaptability", "time management", "collaboration", "presentation", "work ethic", "decision making"
    ]
}

# Resume Section Headers
RESUME_SECTIONS_PATTERNS = {
    "education": [r"\beducation\b", r"\bacademics\b", r"\bacemic background\b", r"\bqualifications\b"],
    "experience": [r"\bexperience\b", r"\bwork experience\b", r"\binternships?\b", r"\bemployment\b"],
    "projects": [r"\bprojects\b", r"\bacademic projects\b", r"\bpersonal projects\b", r"\bkey projects\b"],
    "skills": [r"\bskills\b", r"\btechnical skills\b", r"\bcore competencies\b", r"\btechnologies\b"],
    "certifications": [r"\bcertifications?\b", r"\bcertificates?\b", r"\bcourses?\b", r"\btrainings?\b", r"\bworkshops?\b"],
    "achievements": [r"\bachievements?\b", r"\bawards?\b", r"\bhackathons?\b", r"\bextracurricular\b"]
}
