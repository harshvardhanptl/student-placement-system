"""
Recommendation Engine Module
Generates personalized, structured, and realistic career advancement plans
organized into 7-day, 30-day, and 60-day strategic milestones.
"""

from typing import Dict, Any, List


def generate_recommendations(
    cgpa: float,
    aptitude_score: float,
    projects_count: int,
    internships_count: int,
    workshops_count: int,
    active_backlogs: int,
    target_role: str,
    missing_core_skills: List[str] = None,
    resume_feedback: List[str] = None,
    placement_prob: float = 50.0
) -> Dict[str, Any]:
    """
    Synthesizes academic metrics, prediction risk factors, skill gaps,
    and resume findings to produce structured recommendations.
    """
    missing_core = missing_core_skills or []
    feedback = resume_feedback or []

    plan_7_days = []
    plan_30_days = []
    plan_60_days = []

    # 1. Backlogs Assessment
    if active_backlogs > 0:
        plan_7_days.append({
            "category": "Academic Eligibility",
            "priority": "CRITICAL",
            "area": "Active Backlogs Clearance",
            "reason": f"Active backlogs ({active_backlogs}) immediately disqualify candidates from top campus placement drives.",
            "action": "Schedule dedicated revision hours with course instructors and register for upcoming backlog examination windows.",
            "target": f"Clear {active_backlogs} pending backlog(s) before recruitment drives commence."
        })

    # 2. Aptitude & Screening Assessment
    if aptitude_score < 65:
        plan_7_days.append({
            "category": "Aptitude & Screening",
            "priority": "HIGH",
            "area": "Quantitative & Logical Aptitude",
            "reason": f"Current aptitude score ({aptitude_score}%) is below the typical 65-70% screening cutoff for round-1 tests.",
            "action": "Complete daily 30-minute timed quizzes on IndiaBIX or PrepInsta focusing on Profit & Loss, Percentages, and Syllogisms.",
            "target": "Score consistently above 75% on 5 timed mock tests within 2 weeks."
        })
        plan_30_days.append({
            "category": "Aptitude & Screening",
            "priority": "HIGH",
            "area": "Full-Length Placement Test Simulation",
            "reason": "Speed and negative marking accuracy in round-1 determine who qualifies for technical interviews.",
            "action": "Take 2 full-length simulated company mock tests weekly under strict time limits.",
            "target": "Achieve 80%+ accuracy across Quantitative, Logical, and Verbal sections."
        })
    else:
        plan_7_days.append({
            "category": "Aptitude & Screening",
            "priority": "MODERATE",
            "area": "Aptitude Speed Maintenance",
            "reason": "Solid aptitude base detected; maintenance ensures rapid speed in company screenings.",
            "action": "Take one weekly comprehensive diagnostic aptitude test.",
            "target": "Maintain 75%+ score under tight time constraints."
        })

    # 3. Technical Skills & DSA
    top_missing_skills = missing_core[:3]
    if top_missing_skills:
        skills_str = ", ".join(top_missing_skills)
        plan_7_days.append({
            "category": "Technical Preparation",
            "priority": "HIGH",
            "area": f"Core Skill Foundations ({skills_str})",
            "reason": f"Target role '{target_role}' expects hands-on familiarity with these core technologies.",
            "action": f"Review foundational syntax, standard library documentation, and basic idioms for {skills_str}.",
            "target": "Complete interactive exercises and push beginner implementations to GitHub."
        })

        plan_30_days.append({
            "category": "Technical Preparation",
            "priority": "HIGH",
            "area": "Data Structures & Algorithmic Problem Solving",
            "reason": "Technical coding rounds in software recruitment heavily focus on standard patterns.",
            "action": "Solve 40 targeted LeetCode / HackerRank problems covering Arrays, Hash Maps, Two Pointers, and Binary Search.",
            "target": "Solve at least 2 medium problems independently within 35 minutes each."
        })

    # 4. Project Portfolio
    if projects_count < 2:
        plan_30_days.append({
            "category": "Project Development",
            "priority": "HIGH",
            "area": "Role-Specific Capstone Project",
            "reason": f"Only {projects_count} project(s) listed. Recruiters look for at least 2 robust portfolio projects.",
            "action": f"Build an end-to-end practical project aligned with '{target_role}' featuring database persistence and clean API design.",
            "target": "Deploy live application on Vercel/Render/Streamlit with full GitHub README documentation."
        })
    else:
        plan_30_days.append({
            "category": "Project Development",
            "priority": "MODERATE",
            "area": "Project Architecture & Code Quality Refinement",
            "reason": "Existing projects can be upgraded to demonstrate engineering maturity.",
            "action": "Add automated unit tests, containerize with Docker, and record a 2-minute Loom walkthrough.",
            "target": "Ensure each project has a live demo link, architecture diagram, and clean commit history."
        })

    # 5. Internships & Practical Experience
    if internships_count == 0:
        plan_60_days.append({
            "category": "Practical Experience",
            "priority": "HIGH",
            "area": "Virtual or Startup Internship",
            "reason": "Hands-on commercial or open-source experience significantly enhances resume selection rates.",
            "action": "Apply to curated internships on Internshala, Wellfound, or contribute to recognized open-source repositories.",
            "target": "Secure at least one 1-month or 2-month internship or complete 2 verified virtual experience programs (e.g., Forage)."
        })

    # 6. Resume & Profile Polish
    if feedback:
        plan_7_days.append({
            "category": "Resume Enhancement",
            "priority": "HIGH",
            "area": "Resume Formatting & Section Refinement",
            "reason": "Automated ATS scanners and recruiters reject resumes lacking standard sections or clear metrics.",
            "action": f"Address detected resume gaps: {'; '.join(feedback[:2])}.",
            "target": "Update resume to single-page ATS-compliant format with quantified XYZ bullet points."
        })
    else:
        plan_7_days.append({
            "category": "Resume Enhancement",
            "priority": "MODERATE",
            "area": "Bullet Point Impact Optimization",
            "reason": "Action-oriented bullet points (Accomplished [X], measured by [Y], by doing [Z]) boost callback rates.",
            "action": "Rewrite project bullets to highlight quantifiable impact, technologies used, and business outcome.",
            "target": "Include metrics (e.g., 'reduced load time by 30%', 'processed 500+ records') on all project descriptions."
        })

    # 7. Mock Interviews & Final Phase (60 Days)
    plan_60_days.append({
        "category": "Interview Readiness",
        "priority": "CRITICAL",
        "area": "Technical & Behavioral Mock Interviews",
        "reason": "Translating knowledge into confident, articulate technical explanations under pressure is the final hurdle.",
        "action": "Conduct at least 5 peer or mentor mock interviews using Pramp, Interviewing.io, or college placement cell.",
        "target": "Master the STAR method (Situation, Task, Action, Result) for HR behavioral questions and live coding articulation."
    })

    return {
        "summary": (
            f"Personalized Career Advancement Strategy for {target_role}. "
            "Follow these structured milestones to systematically elevate academic eligibility, "
            "technical proficiency, and interview readiness."
        ),
        "placement_readiness_indicator": f"{placement_prob:.1f}% estimated probability",
        "plan_7_days": plan_7_days,
        "plan_30_days": plan_30_days,
        "plan_60_days": plan_60_days,
        "disclaimer": (
            "Disclaimer: This improvement plan is an actionable academic advisory framework designed to maximize placement preparation. "
            "It does not guarantee employment or placement offers, which depend on individual interview performance and dynamic market conditions."
        )
    }
