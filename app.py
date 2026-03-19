import streamlit as st
import os
from PIL import Image
from generate_ddr import create_pdf_report
from generate_ddr import extract_text_from_pdf, generate_report_data, create_pdf_report

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Real Estate Guard",
    page_icon="🏢",
    layout="wide"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.image("assets\logo.png", width=70)
st.sidebar.title("Real Estate Guard")

st.sidebar.markdown("## 📌 Navigation")
st.sidebar.radio("", ["🏠 Dashboard", "📊 Analysis", "📄 Reports"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Contact")
st.sidebar.write("👤 Vishal Jadhav")
st.sidebar.write("📧 realestateguard@gmail.com")
st.sidebar.write("📱 +91-9699987646")
st.sidebar.write("📍 Pune, India")
st.sidebar.markdown("[💻 GitHub](https://github.com/VishalJadhav-codes)")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
col1, col2 = st.columns([1, 8], vertical_alignment="center")

with col1:
    st.image("assets\logo.png", width=95)

with col2:
    st.markdown("""
    <div style="line-height:1.8;">
        <h1 style="margin:0; padding:0;">REAL ESTATE GUARD</h1>
        <p style="margin:3px 0 0 0; color:grey; font-size:14px;">
        AI Property Damage Detection Report Generator
        </p>
    </div>
    """, unsafe_allow_html=True)

# 👇 Reduce space before divider
st.markdown("<div style='margin-top:0px;'></div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# DESCRIPTION
# ---------------------------------------------------
st.markdown("""
This application analyzes **property inspection reports** and **thermal reports**
to detect structural issues automatically.

### Detects:
- Moisture intrusion
- Water leakage
- Structural cracks
- Thermal hotspots
- Dampness

### Steps:
1. Upload Inspection Report  
2. Upload Thermal Report  
3. Click Generate Report  
4. Download AI Report  
""")

st.divider()

# ---------------------------------------------------
# FILE UPLOAD (currently optional)
# ---------------------------------------------------
inspection_file = st.file_uploader("Upload Inspection Report", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal Report", type=["pdf"])

# ---------------------------------------------------
# LOGIC FUNCTIONS
# ---------------------------------------------------
def detect_issues(text):
    issues = []
    text = text.lower()

    if "damp" in text:
        issues.append("Dampness detected")

    if "leak" in text:
        issues.append("Water leakage observed")

    if "crack" in text:
        issues.append("Structural cracks detected")

    if "moisture" in text:
        issues.append("Moisture detected")

    if "temperature" in text:
        issues.append("Thermal hotspot detected")

    return issues


def calculate_risk_level(issues):
    if len(issues) == 0:
        return "LOW"
    elif len(issues) <= 2:
        return "MEDIUM"
    else:
        return "HIGH"


def generate_recommendations(issues):
    rec = []

    for issue in issues:
        if "damp" in issue.lower():
            rec.append("Perform waterproofing")
        if "leak" in issue.lower():
            rec.append("Fix leakage immediately")
        if "crack" in issue.lower():
            rec.append("Repair structural damage")

    return list(set(rec))

# ---------------------------------------------------
# OUTPUT FOLDER
# ---------------------------------------------------
pdf_path = "output/DDR_Report.pdf"
os.makedirs("output", exist_ok=True)

# ---------------------------------------------------
# BUTTON (MAIN LOGIC)
# ---------------------------------------------------
if st.button("🚀 Generate Report"):

    if inspection_file is None or thermal_file is None:
        st.warning("⚠️ Please upload both Inspection and Thermal reports")

    else:
        with st.spinner("Analyzing reports..."):

            # Extract text from uploaded PDFs
            inspection_text_input = extract_text_from_pdf(inspection_file)
            thermal_text_input = extract_text_from_pdf(thermal_file)

            # Generate report data (NEW SAFE FUNCTION)
            risk_level, all_issues, recommendations, inspection_text, thermal_text = generate_report_data(
                inspection_text_input,
                thermal_text_input
            )

            # Create PDF
            create_pdf_report(
                risk_level,
                all_issues,
                recommendations,
                inspection_text,
                thermal_text
            )

        st.success("✅ Report Generated Successfully!")

        # Download
        pdf_path = "output/DDR_Report.pdf"

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as file:
                st.download_button(
                    "📄 Download Report",
                    file,
                    file_name="DDR_Report.pdf"
                )
        else:
            st.error("❌ PDF not generated")