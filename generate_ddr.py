import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import fitz

# ---------------------------------------------------
# ENSURE OUTPUT FOLDER EXISTS
# ---------------------------------------------------
os.makedirs("output", exist_ok=True)

# ---------------------------------------------------
# READ TEXT FILES
# ---------------------------------------------------
def read_text_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

inspection_text = read_text_file("output/inspection_text.txt")
thermal_text = read_text_file("output/thermal_text.txt")

# ---------------------------------------------------
# ISSUE DETECTION
# ---------------------------------------------------
def detect_issues(text):
    issues = []
    text = text.lower()

    if "damp" in text:
        issues.append("Dampness detected in walls or flooring")

    if "leak" in text:
        issues.append("Water leakage observed")

    if "crack" in text:
        issues.append("Structural cracks detected")

    if "moisture" in text:
        issues.append("High moisture level found")

    if "hotspot" in text or "temperature" in text:
        issues.append("Thermal hotspot detected")

    return issues

# ---------------------------------------------------
# RISK LEVEL
# ---------------------------------------------------
def calculate_risk_level(issues):
    if len(issues) == 0:
        return "LOW"
    elif len(issues) <= 2:
        return "MEDIUM"
    else:
        return "HIGH"

# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------
def generate_recommendations(issues):
    rec = []

    for issue in issues:
        if "damp" in issue.lower():
            rec.append("Perform waterproofing treatment.")

        if "leak" in issue.lower():
            rec.append("Inspect plumbing and repair leakage.")

        if "crack" in issue.lower():
            rec.append("Conduct structural inspection.")

        if "moisture" in issue.lower():
            rec.append("Improve ventilation and waterproofing.")

        if "thermal" in issue.lower():
            rec.append("Inspect insulation and moisture sources.")

    return list(set(rec))

# ---------------------------------------------------
# MAIN PROCESS FUNCTION (IMPORTANT)
# ---------------------------------------------------
def generate_report_data(inspection_text_input=None, thermal_text_input=None):

    # Use uploaded text if available, else fallback to old text
    inspection_data = inspection_text_input if inspection_text_input else inspection_text
    thermal_data = thermal_text_input if thermal_text_input else thermal_text

    inspection_issues = detect_issues(inspection_data)
    thermal_issues = detect_issues(thermal_data)

    all_issues = inspection_issues + thermal_issues

    risk_level = calculate_risk_level(all_issues)
    recommendations = generate_recommendations(all_issues)

    return risk_level, all_issues, recommendations, inspection_data, thermal_data

import fitz  # pip install pymupdf

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ---------------------------------------------------
# CLEAN PDF GENERATOR
# ---------------------------------------------------
def create_pdf_report(risk_level, issues, recommendations, inspection_text, thermal_text):

    pdf_path = "output/DDR_Report.pdf"
    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()
    story = []

    # ---------------------------------------------------
    # LOGO
    # ---------------------------------------------------
    logo_path = os.path.join("assets", "logo.png")

    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.2*inch, height=1.2*inch))
    else:
        story.append(Paragraph("Logo: NA", styles["Normal"]))

    story.append(Spacer(1, 10))

    # ---------------------------------------------------
    # COMPANY DETAILS
    # ---------------------------------------------------
    story.append(Paragraph("<b>REAL ESTATE GUARD</b>", styles["Title"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("AI Property Damage Detection Report", styles["Normal"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("📍 Pune, India", styles["Normal"]))
    story.append(Paragraph("📧 realestateguard@gmail.com", styles["Normal"]))
    story.append(Paragraph("📞 +91-9699987646", styles["Normal"]))

    story.append(Spacer(1, 20))

    # ---------------------------------------------------
    # RISK LEVEL
    # ---------------------------------------------------
    story.append(Paragraph("<b>RISK LEVEL</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    if not risk_level:
        story.append(Paragraph("NA", styles["Normal"]))
    else:
        color = "green"
        if risk_level == "HIGH":
            color = "red"
        elif risk_level == "MEDIUM":
            color = "orange"

        story.append(Paragraph(f"<font color='{color}'><b>{risk_level}</b></font>", styles["Normal"]))

    story.append(Spacer(1, 16))

    # ---------------------------------------------------
    # DETECTED ISSUES
    # ---------------------------------------------------
    story.append(Paragraph("<b>DETECTED ISSUES</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    if issues:
        for i, issue in enumerate(issues, 1):
            story.append(Paragraph(f"{i}. {issue}", styles["Normal"]))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("NA", styles["Normal"]))

    story.append(Spacer(1, 16))

    # ---------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------
    story.append(Paragraph("<b>RECOMMENDATIONS</b>", styles["Heading2"]))
    story.append(Spacer(1, 6))

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", styles["Normal"]))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("NA", styles["Normal"]))

    story.append(Spacer(1, 20))

    # ---------------------------------------------------
    # INSPECTION SUMMARY
    # ---------------------------------------------------
    story.append(Paragraph("<b>INSPECTION SUMMARY</b>", styles["Heading3"]))
    story.append(Spacer(1, 6))

    if inspection_text.strip():
        story.append(Paragraph(inspection_text[:300], styles["Normal"]))
    else:
        story.append(Paragraph("NA", styles["Normal"]))

    story.append(Spacer(1, 12))

    # ---------------------------------------------------
    # THERMAL SUMMARY
    # ---------------------------------------------------
    story.append(Paragraph("<b>THERMAL SUMMARY</b>", styles["Heading3"]))
    story.append(Spacer(1, 6))

    if thermal_text.strip():
        story.append(Paragraph(thermal_text[:200], styles["Normal"]))
    else:
        story.append(Paragraph("NA", styles["Normal"]))

    story.append(Spacer(1, 20))

    # ---------------------------------------------------
    # FOOTER
    # ---------------------------------------------------
    story.append(Paragraph("Generated by Real Estate Guard AI", styles["Italic"]))

    doc.build(story)

    print("✅ PDF Generated Successfully")