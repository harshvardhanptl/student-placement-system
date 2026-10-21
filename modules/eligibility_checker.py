"""
Eligibility Checker Module
Evaluates student academic profile against corporate recruitment criteria and cutoffs.
"""

from typing import Dict, Any, List
import config


def check_eligibility(
    cgpa: float,
    aptitude_score: float,
    active_backlogs: int,
    projects_count: int = 0,
    internships_count: int = 0,
    company_category: str = "Tier-2 Enterprise & Fintech (e.g., Oracle, Cisco, JPMorgan)",
    custom_criteria: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Evaluates student profile against industry recruitment eligibility benchmarks.
    """
    if custom_criteria:
        criteria = custom_criteria
        category_name = "Custom Company Policy"
        description = criteria.get("description", "Custom placement eligibility rules.")
    else:
        criteria = config.ELIGIBILITY_PRESETS.get(
            company_category,
            config.ELIGIBILITY_PRESETS["Tier-2 Enterprise & Fintech (e.g., Oracle, Cisco, JPMorgan)"]
        )
        category_name = company_category
        description = criteria.get("description", "")

    min_cgpa = criteria.get("min_cgpa", 6.5)
    min_aptitude = criteria.get("min_aptitude", 60)
    max_backlogs = criteria.get("max_backlogs", 0)
    min_projects = criteria.get("min_projects", 1)
    min_internships = criteria.get("min_internships", 0)

    checks = []
    failed_reasons = []
    warnings = []

    # 1. CGPA Check
    cgpa_pass = cgpa >= min_cgpa
    checks.append({
        "criterion": "Minimum CGPA",
        "required": f">= {min_cgpa}",
        "actual": f"{cgpa:.2f}",
        "status": "PASS" if cgpa_pass else "FAIL",
        "detail": f"Student CGPA is {cgpa:.2f} (Required: {min_cgpa})"
    })
    if not cgpa_pass:
        failed_reasons.append(f"CGPA ({cgpa:.2f}) is below minimum threshold ({min_cgpa}).")

    # 2. Backlogs Check (Strict gating parameter in campus hiring)
    backlog_pass = active_backlogs <= max_backlogs
    checks.append({
        "criterion": "Active Backlogs",
        "required": f"<= {max_backlogs}",
        "actual": str(active_backlogs),
        "status": "PASS" if backlog_pass else "FAIL",
        "detail": f"Active backlogs: {active_backlogs} (Max allowed: {max_backlogs})"
    })
    if not backlog_pass:
        failed_reasons.append(
            f"Active backlogs ({active_backlogs}) exceed the allowed maximum ({max_backlogs}). "
            "Most top-tier recruiters require 0 active backlogs at the time of drive."
        )

    # 3. Aptitude Test Cutoff
    aptitude_pass = aptitude_score >= min_aptitude
    checks.append({
        "criterion": "Aptitude Score Cutoff",
        "required": f">= {min_aptitude}%",
        "actual": f"{aptitude_score}%",
        "status": "PASS" if aptitude_pass else ("BORDERLINE" if aptitude_score >= (min_aptitude - 5) else "FAIL"),
        "detail": f"Aptitude score is {aptitude_score}% (Cutoff: {min_aptitude}%)"
    })
    if not aptitude_pass:
        if aptitude_score >= (min_aptitude - 5):
            warnings.append(f"Aptitude score ({aptitude_score}%) is close to cutoff ({min_aptitude}%). Revision recommended.")
        else:
            failed_reasons.append(f"Aptitude score ({aptitude_score}%) is below round-1 screening cutoff ({min_aptitude}%).")

    # 4. Project Portfolio
    project_pass = projects_count >= min_projects
    checks.append({
        "criterion": "Completed Projects",
        "required": f">= {min_projects}",
        "actual": str(projects_count),
        "status": "PASS" if project_pass else "BORDERLINE",
        "detail": f"Completed projects: {projects_count} (Recommended: {min_projects})"
    })
    if not project_pass:
        warnings.append(f"Developing at least {min_projects} practical projects is recommended for technical interview rounds.")

    # 5. Internship Experience
    internship_pass = internships_count >= min_internships
    checks.append({
        "criterion": "Internships Completed",
        "required": f">= {min_internships}",
        "actual": str(internships_count),
        "status": "PASS" if internship_pass else "BORDERLINE",
        "detail": f"Completed internships: {internships_count} (Recommended: {min_internships})"
    })
    if not internship_pass and min_internships > 0:
        warnings.append("Internship experience strengthens resume shortlisting during competitive screening.")

    # Determine Overall Eligibility Status
    # Hard criteria: CGPA & Backlogs are non-negotiable for campus drives
    if not cgpa_pass or not backlog_pass or (not aptitude_pass and aptitude_score < min_aptitude - 5):
        overall_status = "Ineligible"
        badge_color = "#EF4444"
        summary = "Profile currently does not meet standard qualification thresholds for this recruitment tier."
    elif not aptitude_pass or not project_pass or not internship_pass:
        overall_status = "Borderline / Conditionally Eligible"
        badge_color = "#F59E0B"
        summary = "Profile satisfies basic academic criteria but requires improvement in aptitude or portfolio readiness."
    else:
        overall_status = "Fully Eligible"
        badge_color = "#10B981"
        summary = "Profile satisfies all academic and technical eligibility criteria for campus recruitment drives."

    return {
        "company_category": category_name,
        "description": description,
        "overall_status": overall_status,
        "badge_color": badge_color,
        "summary": summary,
        "checks": checks,
        "failed_reasons": failed_reasons,
        "warnings": warnings,
        "is_eligible": overall_status == "Fully Eligible"
    }


def evaluate_all_tiers(cgpa: float, aptitude: float, backlogs: int, projects: int, internships: int) -> List[Dict[str, Any]]:
    """Evaluates the student profile against all company tiers for comparative display."""
    tier_results = []
    for tier_name in config.ELIGIBILITY_PRESETS.keys():
        res = check_eligibility(
            cgpa=cgpa,
            aptitude_score=aptitude,
            active_backlogs=backlogs,
            projects_count=projects,
            internships_count=internships,
            company_category=tier_name
        )
        tier_results.append({
            "tier": tier_name,
            "status": res["overall_status"],
            "badge_color": res["badge_color"],
            "summary": res["summary"]
        })
    return tier_results
