import streamlit as st


def load_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.15), transparent 30%),
        radial-gradient(circle at top right, rgba(168,85,247,0.15), transparent 30%),
        linear-gradient(
            135deg,
            #020617 0%,
            #0f172a 50%,
            #111827 100%
        );

    color: white !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

/* Hide default header line */
header {
    background: transparent !important;
}

/* Hero */
.hero {
    padding: 42px;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(37,99,235,0.95), rgba(147,51,234,0.92)),
        url("https://www.transparenttextures.com/patterns/cubes.png");
    color: white;
    box-shadow: 0 25px 60px rgba(37,99,235,0.35);
    margin-bottom: 32px;
}

.hero-title {
    font-size: 56px;
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 12px;
}

.hero-subtitle {
    font-size: 19px;
    color: #e0e7ff;
    max-width: 900px;
}

/* Section headings */
.section-title {
    font-size: 30px;
    font-weight: 850;
    margin-top: 35px;
    margin-bottom: 18px;
    color: #111827;
}

/* Cards */
.metric-card {
    background: rgba(255,255,255,0.86);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 15px 35px rgba(15,23,42,0.08);
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 22px 45px rgba(37,99,235,0.18);
}

.metric-label {
    font-size: 14px;
    color: #64748b;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
}

.metric-value {
    font-size: 34px;
    color: #111827;
    font-weight: 900;
    margin-top: 8px;
}

/* Streamlit buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: #ddd6fe ;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1.4rem;
    font-weight: 800;
    box-shadow: 0 12px 30px rgba(37,99,235,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 38px rgba(124,58,237,0.35);
    color: white;
}

/* Download buttons */
.stDownloadButton > button {
    background: linear-gradient(90deg, #059669, #10b981);
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 800;
}

/* Inputs */
.stSelectbox div[data-baseweb="select"],
.stTextInput input,
.stNumberInput input {
    border-radius: 14px;
}

/* Plotly chart container - remove white border */
[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border-radius: 0px !important;
    padding: 0px !important;
    box-shadow: none !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e1b4b);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Alerts */
.stAlert {
    border-radius: 18px;
}

/* Radio */
.stRadio > div {
    background: rgba(255,255,255,0.65);
    padding: 14px;
    border-radius: 16px;
}

/* Slider */
.stSlider {
    background: rgba(255,255,255,0.55);
    padding: 14px;
    border-radius: 16px;
}
                [data-testid="stFileUploaderDropzone"] {
    background: #ffffff !important;
    color: #111827 !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #111827 !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploader"] label {
    color: #111827 !important;
    font-weight: 800 !important;
}
                /* Force Purple Browse Button */

.stFileUploader button,
[data-testid="stBaseButton-secondary"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.35) !important;
}
                
</style>
""", unsafe_allow_html=True)