"""
Resume Analyzer Module
Performs entity extraction, skill identification, section completeness scoring,
and job description alignment for student resumes.
"""

import re
from typing import Dict, List, Any, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import config


def extract_contact_info(text: str) -> Dict[str, Any]:
    """
    Extracts email addresses, phone numbers, and LinkedIn/GitHub links if present.
    """
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}"
    linkedin_pattern = r"linkedin\.com/in/[a-zA-Z0-9_-]+"
    github_pattern = r"github\.com/[a-zA-Z0-9_-]+"

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
    githubs = re.findall(github_pattern, text, re.IGNORECASE)

    # Filter short or invalid phone matches
    valid_phones = [p.strip() for p in phones if len(re.sub(r"\D", "", p)) >= 10]

    return {
        "email": emails[0] if emails else None,
        "phone": valid_phones[0] if valid_phones else None,
        "linkedin": linkedins[0] if linkedins else None,
        "github": githubs[0] if githubs else None
    }


def extract_skills_by_category(text: str) -> Dict[str, List[str]]:
    """
    Scans resume text using word boundary matching against the categorized skill taxonomy.
    Avoids false positives with token-boundary regexes.
    """
    lowered_text = " " + text.lower() + " "
    # Replace common punctuation with spaces for clean tokenization, but preserve .js, c++, c#, .net
    # Tokenization helper:
    normalized = re.sub(r"[,/|;()\[\]{}]", " ", lowered_text)

    found_skills: Dict[str, List[str]] = {}

    for category, skill_list in config.SKILL_DICTIONARY.items():
        found_in_category = []
        for skill in skill_list:
            escaped_skill = re.escape(skill)
            # Handle special symbols like C++, C#, .NET
            if skill in ["c++", "c#", ".net", "node.js", "next.js", "vue.js", "react.js"]:
                pattern = r"(?:^|\s)" + escaped_skill + r"(?:$|\s)"
            else:
                pattern = r"\b" + escaped_skill + r"\b"

            if re.search(pattern, normalized):
                # Standardize casing for display
                display_name = skill.title()
                if skill in ["aws", "gcp", "sql", "css", "html", "nlp", "ci/cd", "rest api", "dbms", "dsa", "oop", "oops"]:
                    display_name = skill.upper()
                elif skill in ["c++", "c#", ".net", "node.js", "next.js", "vue.js", "react.js", "scikit-learn"]:
                    display_name = skill
                found_in_category.append(display_name)

        if found_in_category:
            found_skills[category] = sorted(list(set(found_in_category)))

    return found_skills


def detect_sections(text: str) -> Dict[str, bool]:
    """
    Detects whether essential resume sections are present based on common heading patterns.
    """
    lowered_text = text.lower()
    sections_found = {}

    for section_name, patterns in config.RESUME_SECTIONS_PATTERNS.items():
        found = False
        for pat in patterns:
            if re.search(pat, lowered_text):
                found = True
                break
        sections_found[section_name] = found

    return sections_found


def calculate_resume_completeness(
    text: str,
    sections: Dict[str, bool],
    contact_info: Dict[str, Any],
    skills_found: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Computes an objective completeness score (0 to 100) based on:
    - Contact Information (15 pts)
    - Key Sections Presence (40 pts)
    - Skill Diversity & Depth (25 pts)
    - Content Substantiveness / Word count (20 pts)
    """
    score = 0
    feedback = []

    # 1. Contact Information (15 pts)
    contact_pts = 0
    if contact_info.get("email"):
        contact_pts += 6
    else:
        feedback.append("Missing or unreadable email address.")

    if contact_info.get("phone"):
        contact_pts += 5
    else:
        feedback.append("Missing or unreadable phone number.")

    if contact_info.get("linkedin") or contact_info.get("github"):
        contact_pts += 4
    else:
        feedback.append("Add a LinkedIn profile or GitHub repository link for technical credibility.")

    score += contact_pts

    # 2. Section Presence (40 pts: 8 pts each for 5 core sections)
    section_weights = {
        "education": (8, "Education section is missing or lacks clear heading."),
        "skills": (8, "Skills section is missing or not prominently structured."),
        "projects": (10, "Projects section is absent. Academic & hands-on projects are vital for placements."),
        "experience": (8, "Experience / Internship section is missing. Even virtual internships add value."),
        "certifications": (6, "Certifications or training section is absent.")
    }

    for sec, (weight, warning) in section_weights.items():
        if sections.get(sec, False):
            score += weight
        else:
            feedback.append(warning)

    # 3. Skills Coverage (25 pts)
    total_skills = sum(len(s) for s in skills_found.values())
    if total_skills >= 10:
        score += 25
    elif total_skills >= 6:
        score += 18
    elif total_skills >= 3:
        score += 10
        feedback.append("Only a few technical skills detected. Explicitly list core programming languages and tools.")
    else:
        score += 4
        feedback.append("Critically low number of recognized technical skills detected in the document.")

    # 4. Word Count / Depth (20 pts)
    word_count = len(text.split())
    if word_count >= 300:
        score += 20
    elif word_count >= 180:
        score += 14
        feedback.append("Resume content is somewhat brief. Elaborate on project deliverables and tech stacks.")
    elif word_count >= 80:
        score += 8
        feedback.append("Resume appears too sparse (< 180 words). Add project details, responsibilities, and tools.")
    else:
        score += 2
        feedback.append("Document has very low word count (< 80 words). Verify whether the PDF is scanned or empty.")

    # Tier assessment
    if score >= 85:
        level = "Excellent"
        summary = "Resume is comprehensive, well-structured, and placement-ready."
    elif score >= 70:
        level = "Good"
        summary = "Resume has solid foundations but has room for section or skill improvements."
    elif score >= 50:
        level = "Average"
        summary = "Resume has key components but is missing crucial sections or technical depth."
    else:
        level = "Needs Improvement"
        summary = "Resume is sparse or lacks essential industry sections."

    return {
        "score": min(score, 100),
        "level": level,
        "summary": summary,
        "feedback": feedback,
        "word_count": word_count,
        "total_skills_count": total_skills
    }


def analyze_job_match(resume_text: str, target_role: str, custom_jd: str = None) -> Dict[str, Any]:
    """
    Compares the resume against the target role's taxonomy or a user-provided Job Description.
    Uses TF-IDF Cosine Similarity and Keyword Skill Overlap.
    """
    role_info = config.JOB_ROLES_TAXONOMY.get(target_role, {})
    core_role_skills = role_info.get("core_skills", [])
    specialized_role_skills = role_info.get("specialized_skills", [])
    target_all_skills = [s.lower() for s in (core_role_skills + specialized_role_skills)]

    # Extract all skills in resume
    found_categorized = extract_skills_by_category(resume_text)
    all_resume_skills_lower = set()
    for cat_skills in found_categorized.values():
        for s in cat_skills:
            all_resume_skills_lower.add(s.lower())

    # Skill matching
    matching_core = [s for s in core_role_skills if s.lower() in all_resume_skills_lower]
    missing_core = [s for s in core_role_skills if s.lower() not in all_resume_skills_lower]

    matching_specialized = [s for s in specialized_role_skills if s.lower() in all_resume_skills_lower]
    missing_specialized = [s for s in specialized_role_skills if s.lower() not in all_resume_skills_lower]

    total_target = len(core_role_skills) + len(specialized_role_skills)
    total_matched = len(matching_core) + len(matching_specialized)
    skill_coverage_pct = round((total_matched / total_target * 100), 1) if total_target > 0 else 0.0

    # TF-IDF Cosine Similarity with JD or benchmark role text
    reference_text = custom_jd if custom_jd and len(custom_jd.strip()) > 30 else (
        f"{target_role}. Required core competencies: " + ", ".join(core_role_skills) +
        ". Specialized technologies: " + ", ".join(specialized_role_skills) +
        ". Experience with project development, database management, problem solving, algorithms, and git."
    )

    tfidf = TfidfVectorizer(stop_words="english")
    try:
        tfidf_matrix = tfidf.fit_transform([resume_text, reference_text])
        similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        similarity_pct = round(similarity * 100, 1)
    except Exception:
        similarity_pct = 0.0

    # Composite Match Score: 60% Skill Coverage + 40% TF-IDF Cosine Similarity
    composite_match_score = round(0.60 * skill_coverage_pct + 0.40 * similarity_pct, 1)

    return {
        "target_role": target_role,
        "composite_match_score": min(composite_match_score, 100.0),
        "skill_coverage_pct": skill_coverage_pct,
        "cosine_similarity_pct": similarity_pct,
        "matching_core_skills": matching_core,
        "missing_core_skills": missing_core,
        "matching_specialized_skills": matching_specialized,
        "missing_specialized_skills": missing_specialized,
        "role_recommendations": role_info.get("project_recommendations", [])
    }


def analyze_resume(resume_text: str, target_role: str = "Software Development Engineer (SDE)", custom_jd: str = None) -> Dict[str, Any]:
    """
    Main orchestration function for complete resume analysis.
    """
    if not resume_text or len(resume_text.strip()) < 20:
        return {
            "success": False,
            "error": "The resume text is empty or too short for meaningful analysis."
        }

    contact_info = extract_contact_info(resume_text)
    skills_found = extract_skills_by_category(resume_text)
    sections = detect_sections(resume_text)
    completeness = calculate_resume_completeness(resume_text, sections, contact_info, skills_found)
    job_match = analyze_job_match(resume_text, target_role, custom_jd)

    return {
        "success": True,
        "contact_info": contact_info,
        "skills_by_category": skills_found,
        "sections_detected": sections,
        "completeness": completeness,
        "job_match": job_match
    }
