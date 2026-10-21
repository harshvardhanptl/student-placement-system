"""
Report Generator Module
Compiles a publication-grade PDF placement & career intelligence dossier using ReportLab.
"""

import io
import os
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
import config


def generate_placement_report(
    student_profile: Dict[str, Any],
    prediction_result: Dict[str, Any],
    eligibility_result: Dict[str, Any],
    skills_gap_result: Dict[str, Any],
    recommendations_result: Dict[str, Any],
    resume_analysis_result: Dict[str, Any] = None
) -> bytes:
    """
    Generates a PDF placement intelligence report in memory.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    NAVY = colors.HexColor("#0F172A")
    ACCENT_BLUE = colors.HexColor("#2563EB")
    SLATE = colors.HexColor("#475569")
    LIGHT_BG = colors.HexColor("#F8FAFC")
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    SUCCESS_COLOR = colors.HexColor("#059669")
    WARNING_COLOR = colors.HexColor("#D97706")
    DANGER_COLOR = colors.HexColor("#DC2626")

    # Typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=NAVY
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=SLATE
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )

    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    tag_style = ParagraphStyle(
        "TagText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=11,
        textColor=colors.HexColor("#64748B")
    )

    elements = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>STUDENT PLACEMENT PREDICTION & CAREER INTELLIGENCE DOSSIER</b>", title_style),
            Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}<br/><b>Project:</b> BCA Final-Year Academic System", subtitle_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT_BLUE, spaceBefore=4, spaceAfter=12))

    # 2. Student Profile Summary & Model Outcome
    elements.append(Paragraph("1. Executive Summary & Placement Prediction", section_heading))

    pred_status = prediction_result.get("status_label", "Under Evaluation")
    pred_prob = prediction_result.get("probability", 0.0)
    readiness_tier = prediction_result.get("readiness_tier", "Assessment Complete")

    cgpa = student_profile.get("cgpa", 0.0)
    aptitude = student_profile.get("aptitude_score", 0)
    projects = student_profile.get("projects_count", 0)
    internships = student_profile.get("internships_count", 0)
    workshops = student_profile.get("workshops_count", 0)
    backlogs = student_profile.get("active_backlogs", 0)
    target_role = student_profile.get("target_role", "Software Engineer")

    prob_color = SUCCESS_COLOR if pred_prob >= 60 else (WARNING_COLOR if pred_prob >= 40 else DANGER_COLOR)

    summary_table_data = [
        [
            Paragraph("<b>Candidate Name / ID:</b>", bold_body),
            Paragraph(str(student_profile.get("student_name", "Student Candidate")), body_style),
            Paragraph("<b>Predicted Status:</b>", bold_body),
            Paragraph(f"<b>{pred_status}</b>", ParagraphStyle("PStatus", parent=bold_body, textColor=prob_color))
        ],
        [
            Paragraph("<b>Target Job Role:</b>", bold_body),
            Paragraph(str(target_role), body_style),
            Paragraph("<b>Model Probability:</b>", bold_body),
            Paragraph(f"<b>{pred_prob}%</b> ({readiness_tier})", body_style)
        ],
        [
            Paragraph("<b>Academic CGPA:</b>", bold_body),
            Paragraph(f"{cgpa:.2f} / 10.0", body_style),
            Paragraph("<b>Aptitude Test Score:</b>", bold_body),
            Paragraph(f"{aptitude} / 100", body_style)
        ],
        [
            Paragraph("<b>Completed Projects:</b>", bold_body),
            Paragraph(str(projects), body_style),
            Paragraph("<b>Active Backlogs:</b>", bold_body),
            Paragraph(f"{backlogs} backlog(s)", body_style)
        ],
        [
            Paragraph("<b>Internships:</b>", bold_body),
            Paragraph(str(internships), body_style),
            Paragraph("<b>Certifications / Workshops:</b>", bold_body),
            Paragraph(str(workshops), body_style)
        ]
    ]

    t_summary = Table(summary_table_data, colWidths=[130, 140, 130, 140])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_summary)
    elements.append(Spacer(1, 10))

    # 3. Academic & Corporate Eligibility Assessment
    elements.append(Paragraph("2. Campus Recruitment Eligibility Assessment", section_heading))
    elig_status = eligibility_result.get("overall_status", "Evaluated")
    company_cat = eligibility_result.get("company_category", "Standard Corporate Benchmark")

    elig_rows = [
        [
            Paragraph("<b>Eligibility Benchmark</b>", bold_body),
            Paragraph("<b>Required Standard</b>", bold_body),
            Paragraph("<b>Candidate Profile</b>", bold_body),
            Paragraph("<b>Evaluation</b>", bold_body)
        ]
    ]

    for chk in eligibility_result.get("checks", []):
        st = chk.get("status", "PASS")
        status_color = SUCCESS_COLOR if st == "PASS" else (WARNING_COLOR if st == "BORDERLINE" else DANGER_COLOR)
        elig_rows.append([
            Paragraph(chk.get("criterion", ""), body_style),
            Paragraph(chk.get("required", ""), body_style),
            Paragraph(chk.get("actual", ""), body_style),
            Paragraph(f"<b>{st}</b>", ParagraphStyle("ESt", parent=bold_body, textColor=status_color))
        ])

    t_elig = Table(elig_rows, colWidths=[160, 120, 130, 130])
    t_elig.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(t_elig)
    elements.append(Spacer(1, 10))

    # 4. Resume Intelligence & ATS Completeness (if available)
    if resume_analysis_result and resume_analysis_result.get("success"):
        elements.append(Paragraph("3. Resume Intelligence & Completeness Audit", section_heading))
        comp = resume_analysis_result.get("completeness", {})
        job_m = resume_analysis_result.get("job_match", {})
        contact = resume_analysis_result.get("contact_info", {})

        res_info_data = [
            [
                Paragraph(f"<b>Completeness Score:</b> {comp.get('score', 0)}/100 ({comp.get('level', 'Evaluated')})", bold_body),
                Paragraph(f"<b>Job Description Alignment:</b> {job_m.get('composite_match_score', 0)}%", bold_body)
            ],
            [
                Paragraph(f"<b>Detected Email:</b> {contact.get('email') or 'Not Detected'}", body_style),
                Paragraph(f"<b>Detected Contact:</b> {contact.get('phone') or 'Not Detected'}", body_style)
            ]
        ]
        t_res = Table(res_info_data, colWidths=[270, 270])
        t_res.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(t_res)
        elements.append(Spacer(1, 10))

    # 5. Skills Gap Analysis
    elements.append(Paragraph(f"4. Skills Gap Analysis for {target_role}", section_heading))
    matching_core = skills_gap_result.get("matching_core_skills", [])
    missing_core = skills_gap_result.get("missing_core_skills", [])
    readiness_pct = skills_gap_result.get("readiness_percentage", 0.0)

    gap_data = [
        [
            Paragraph("<b>Matching Core Competencies:</b>", bold_body),
            Paragraph(", ".join(matching_core) if matching_core else "No core skills detected yet.", body_style)
        ],
        [
            Paragraph("<b>Identified Skill Gaps (High Priority):</b>", bold_body),
            Paragraph(", ".join(missing_core) if missing_core else "All core competencies met!", body_style)
        ],
        [
            Paragraph("<b>Role Readiness Index:</b>", bold_body),
            Paragraph(f"<b>{readiness_pct}%</b> match for target curriculum requirements", body_style)
        ]
    ]
    t_gap = Table(gap_data, colWidths=[200, 340])
    t_gap.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_gap)
    elements.append(Spacer(1, 10))

    # 6. Strategic Improvement Plan (Roadmap)
    elements.append(Paragraph("5. Personalized Actionable Career Plan", section_heading))

    plan_rows = [
        [
            Paragraph("<b>Timeline</b>", bold_body),
            Paragraph("<b>Improvement Focus</b>", bold_body),
            Paragraph("<b>Specific Actionable Step</b>", bold_body),
            Paragraph("<b>Completion Metric</b>", bold_body)
        ]
    ]

    for p in recommendations_result.get("plan_7_days", [])[:2]:
        plan_rows.append([
            Paragraph("<b>7 Days</b>", bold_body),
            Paragraph(p.get("area", ""), body_style),
            Paragraph(p.get("action", ""), body_style),
            Paragraph(p.get("target", ""), body_style)
        ])

    for p in recommendations_result.get("plan_30_days", [])[:2]:
        plan_rows.append([
            Paragraph("<b>30 Days</b>", bold_body),
            Paragraph(p.get("area", ""), body_style),
            Paragraph(p.get("action", ""), body_style),
            Paragraph(p.get("target", ""), body_style)
        ])

    for p in recommendations_result.get("plan_60_days", [])[:2]:
        plan_rows.append([
            Paragraph("<b>60 Days</b>", bold_body),
            Paragraph(p.get("area", ""), body_style),
            Paragraph(p.get("action", ""), body_style),
            Paragraph(p.get("target", ""), body_style)
        ])

    t_plan = Table(plan_rows, colWidths=[65, 130, 205, 140])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t_plan)
    elements.append(Spacer(1, 14))

    # 7. Disclaimer & Model Limitations
    disclaimer_text = (
        "<b>Model Limitations & Academic Disclaimer:</b> This report is generated by the AI-Powered Student Placement Prediction & Career "
        "Intelligence System for academic assessment purposes. Statistical predictions are derived from campus recruitment historical trends "
        "using supervised machine learning. Actual recruitment outcomes depend on hiring cycles, offline technical interviews, problem-solving "
        "rounds, and interpersonal communication. This system does not guarantee employment offers."
    )
    elements.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
