import streamlit as st
import json
import time
from main import GhostTermsAuditor, TINYFISH_API_KEY

st.set_page_config(
    page_title="GhostTerms | Deceptive UX & Legal Trap Bounty Agent",
    page_icon="🛡️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0b0f19; }
    .metric-card {
        background-color: #1a2234;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2d3748;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ GhostTerms: Autonomous Dark-Pattern Bounty Agent")
st.caption("AI/ML Track — Open Innovation | Team: DeceptiveDefense | Powered by TinyFish Infrastructure")

# Sidebar
with st.sidebar:
    st.header("⚙️ Engine Configuration")
    st.write("**Active Infrastructure:**")
    st.success("✅ TinyFish Fetch API (DOM Sanitizer)")
    st.success("✅ TinyFish Web Agent (Funnel Traversal)")
    st.write("---")
    st.markdown("**Compliance Standards:**")
    st.info("FTC Deceptive Design Guidelines\nEU Digital Services Act (DSA)")

# Main Input
col1, col2 = st.columns([3, 1])
with col1:
    target_url = st.text_input(
        "Enter Target Platform Checkout or Terms URL:",
        value="https://example.com/subscription-terms"
    )
with col2:
    st.write("")
    st.write("")
    scan_button = st.button("🚀 Audit with TinyFish", use_container_width=True)

if scan_button:
    if not TINYFISH_API_KEY:
        st.error("TINYFISH_API_KEY not found in .env file! Please check configuration.")
    else:
        with st.spinner("Dispatching TinyFish Agent to traverse DOM and extract funnels..."):
            auditor = GhostTermsAuditor(api_key=TINYFISH_API_KEY)
            # Fetch & Audit
            content = auditor.fetch_page_content(target_url)
            time.sleep(1)  # Smooth transition for demo
            report = auditor.audit_dark_patterns(content)

        st.success("Audit Complete!")
        
        # Top Metrics
        m1, m2, m3, m4 = st.columns(4)
        score = report["dark_pattern_index"]
        
        with m1:
            st.metric("Dark Pattern Index", f"{score}/100", delta="-HIGH RISK" if score >= 50 else "NORMAL", delta_color="inverse")
        with m2:
            st.metric("Risk Tier", report["risk_tier"])
        with m3:
            st.metric("Deceptive Clauses", report["findings_count"])
        with m4:
            st.metric("Regulatory Ready", "YES (FTC/DSA)" if report["regulatory_complaint_ready"] else "NO")

        st.write("---")

        # Detailed Breakdown
        left_col, right_col = st.columns(2)
        
        with left_col:
            st.subheader("⚠️ Detected Violations & Evidence")
            for item in report.get("violations", []):
                with st.expander(f"🚩 {item['category']} (Severity: {item['severity']})", expanded=True):
                    st.write(f"**Penalty Added:** +{item['penalty_points']} points")
                    st.write("**Matched Evidence in Live Funnel:**")
                    for evidence in item["matched_evidence"]:
                        st.code(f'"{evidence}"', language="markdown")

        with right_col:
            st.subheader("📄 Automated Regulatory Complaint Dossier")
            st.json(report)
            st.download_button(
                label="📥 Export Dossier for Regulatory Submission (JSON)",
                data=json.dumps(report, indent=2),
                file_name="ghostterms_complaint_dossier.json",
                mime="application/json"
            )