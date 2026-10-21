"""
Skills Gap Analyzer Module
Performs deep role-based gap analysis comparing student technical competencies
against industry job role benchmarks.
"""

from typing import List, Dict, Any, Set
import config


# Curated learning resources mapped to common tech skills
SKILL_LEARNING_RESOURCES = {
    "Data Structures": {
        "focus": "Arrays, Strings, Linked Lists, Trees, Graphs, Hash Maps",
        "resource": "NeetCode 150 / LeetCode Top Interview 150",
        "action": "Solve 2 LeetCode easy/medium problems daily focusing on time and space complexity."
    },
    "Algorithms": {
        "focus": "Binary Search, Two Pointers, Dynamic Programming, Backtracking",
        "resource": "Grokking the Coding Interview / Striver's A2Z DSA Sheet",
        "action": "Master sliding window and graph traversal patterns (BFS/DFS)."
    },
    "SQL": {
        "focus": "Joins, Aggregations, Subqueries, Window Functions, Indexing",
        "resource": "Mode Analytics SQL Tutorial / SQLZoo",
        "action": "Practice 30 complex multi-table JOIN queries and window functions."
    },
    "DBMS": {
        "focus": "ACID properties, Normalization (1NF to BCNF), Transactions, Indexing",
        "resource": "Gate Smashers DBMS Playlist / GeeksforGeeks DBMS",
        "action": "Review indexing mechanisms (B+ trees) and transaction concurrency control."
    },
    "OOP": {
        "focus": "Encapsulation, Inheritance, Polymorphism, Abstraction, SOLID principles",
        "resource": "Refactoring Guru - Design Patterns & SOLID",
        "action": "Implement classic design patterns (Factory, Singleton, Strategy) in Java or Python."
    },
    "Git": {
        "focus": "Branching, Merging, Rebasing, Pull Requests, Merge Conflict Resolution",
        "resource": "Pro Git Book / GitHub Learning Lab",
        "action": "Publish all academic projects to a clean GitHub profile with documented README files."
    },
    "Docker": {
        "focus": "Dockerfiles, Images, Containers, Multi-stage builds, Docker Compose",
        "resource": "Docker for Beginners - TechWorld with Nana",
        "action": "Containerize your primary full-stack or machine learning project with Docker Compose."
    },
    "REST APIs": {
        "focus": "HTTP methods, Status codes, Authentication (JWT), API Versioning, Rate Limiting",
        "resource": "Postman Student Expert Program / Fastify or Express Docs",
        "action": "Design and document a RESTful service following OpenAPI/Swagger standards."
    },
    "React": {
        "focus": "Hooks (useState, useEffect, useMemo), Context API, Component Lifecycle",
        "resource": "React.dev Official Interactive Tutorial / FullStackOpen",
        "action": "Build a responsive single-page application integrating third-party APIs and state management."
    },
    "Machine Learning": {
        "focus": "Supervised & Unsupervised Learning, Cross-validation, Hyperparameter Tuning",
        "resource": "Coursera Andrew Ng Machine Learning Specialization",
        "action": "Train, evaluate, and deploy a predictive ML model using Scikit-Learn and FastAPI."
    }
}


def analyze_skills_gap(
    student_skills: List[str],
    target_role: str = "Software Development Engineer (SDE)"
) -> Dict[str, Any]:
    """
    Performs gap analysis for student skills against the selected role.
    """
    role_data = config.JOB_ROLES_TAXONOMY.get(
        target_role,
        config.JOB_ROLES_TAXONOMY["Software Development Engineer (SDE)"]
    )

    core_skills = role_data.get("core_skills", [])
    specialized_skills = role_data.get("specialized_skills", [])

    # Normalize student skills for case-insensitive matching
    student_skills_clean = [s.strip() for s in student_skills if s.strip()]
    student_skills_lower = set(s.lower() for s in student_skills_clean)

    # Core skills evaluation (Weight = 1.5)
    matching_core = []
    missing_core = []
    for skill in core_skills:
        if skill.lower() in student_skills_lower:
            matching_core.append(skill)
        else:
            missing_core.append(skill)

    # Specialized skills evaluation (Weight = 1.0)
    matching_specialized = []
    missing_specialized = []
    for skill in specialized_skills:
        if skill.lower() in student_skills_lower:
            matching_specialized.append(skill)
        else:
            missing_specialized.append(skill)

    # Weighted Role Readiness Percentage
    total_weight = len(core_skills) * 1.5 + len(specialized_skills) * 1.0
    earned_weight = len(matching_core) * 1.5 + len(matching_specialized) * 1.0
    readiness_pct = round((earned_weight / total_weight) * 100, 1) if total_weight > 0 else 0.0

    # Categorize readiness tier
    if readiness_pct >= 80:
        readiness_badge = "Job-Ready (High Match)"
        readiness_color = "#10B981"
    elif readiness_pct >= 55:
        readiness_badge = "Moderately Prepared (Bridgeable Gaps)"
        readiness_color = "#3B82F6"
    elif readiness_pct >= 35:
        readiness_badge = "Developing (Key Gaps Exist)"
        readiness_color = "#F59E0B"
    else:
        readiness_badge = "Foundational Stage (Significant Preparation Needed)"
        readiness_color = "#EF4444"

    # Actionable learning recommendations for top missing skills
    learning_recommendations = []
    for missing_s in (missing_core + missing_specialized):
        if missing_s in SKILL_LEARNING_RESOURCES:
            info = SKILL_LEARNING_RESOURCES[missing_s]
            learning_recommendations.append({
                "skill": missing_s,
                "priority": "HIGH (Core Requirement)" if missing_s in missing_core else "MEDIUM (Elective/Specialized)",
                "focus_topics": info["focus"],
                "recommended_resource": info["resource"],
                "suggested_action": info["action"]
            })
        else:
            # General fallback action
            priority = "HIGH (Core Requirement)" if missing_s in missing_core else "MEDIUM (Specialized)"
            learning_recommendations.append({
                "skill": missing_s,
                "priority": priority,
                "focus_topics": f"Core concepts and practical application of {missing_s}",
                "recommended_resource": f"Official documentation & hands-on tutorials for {missing_s}",
                "suggested_action": f"Build a mini project demonstrating practical proficiency in {missing_s}."
            })

    return {
        "target_role": target_role,
        "readiness_percentage": min(readiness_pct, 100.0),
        "readiness_badge": readiness_badge,
        "readiness_color": readiness_color,
        "matching_core_skills": matching_core,
        "missing_core_skills": missing_core,
        "matching_specialized_skills": matching_specialized,
        "missing_specialized_skills": missing_specialized,
        "total_target_skills_count": len(core_skills) + len(specialized_skills),
        "student_skills_provided": student_skills_clean,
        "learning_recommendations": learning_recommendations,
        "recommended_projects": role_data.get("project_recommendations", []),
        "recommended_certifications": role_data.get("recommended_certifications", [])
    }
