import streamlit as st

APP_NAME = "DataSense AutoMLSS"


def sidebar():
    with st.sidebar:
        st.markdown(f"## 🚀 {APP_NAME}")
        st.markdown("---")
        st.markdown("### Navigation")
        st.markdown("""
        🏠 Dashboard  
        📊 Dataset Analysis  
        ❤️ Dataset Health  
        📈 Visualizations  
        🤖 AutoML Training  
        📥 Reports  
        """)
        st.markdown("---")
        st.info("Upload → Analyze → Train → Download")


def hero_section():
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{APP_NAME}</div>
            <div class="hero-subtitle">
                A premium no-code AutoML platform for dataset profiling, health scoring,
                feature analysis, visual dashboards, model training, and professional report generation.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def linkedin_card():
    st.markdown("""
    <div style="
    margin-top:30px;
    margin-bottom:20px;
    padding:35px;
    border-radius:24px;
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 8px 32px rgba(0,0,0,0.3);
    text-align:center;
    ">

    <h1 style="
    margin-bottom:10px;
    font-size:36px;
    background:linear-gradient(90deg,#60a5fa,#a855f7);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-weight:800;
    ">
    🚀 Connect With The Creator
    </h1>

    <p style="font-size:18px;color:#cbd5e1;margin-bottom:25px;">
    Built by <b>Shoubhya Sinha</b><br>
    ML Engineer • Data Scientist • AI Developer
    </p>

    <a href="https://www.linkedin.com/in/shoubhya-sinha-135199380/"
    target="_blank"
    style="
    display:inline-block;
    padding:14px 30px;
    background:linear-gradient(135deg,#0ea5e9,#2563eb);
    color:white;
    font-size:18px;
    font-weight:700;
    border-radius:14px;
    text-decoration:none;
    box-shadow:0 8px 25px rgba(37,99,235,0.4);
    ">
    💼 Connect on LinkedIn
    </a>

    <p style="margin-top:20px;color:#94a3b8;font-size:14px;">
    Let's collaborate on AI, Machine Learning, Data Science, and Research Projects.
    </p>

    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("""
    <div style="
    text-align:center;
    padding:25px;
    color:#64748b;
    font-size:15px;
    ">
    🚀 <b>DataSense AutoMLSS</b><br><br>
    AI-Powered Dataset Analyzer • AutoML • Report Generator<br><br>
    Built with ❤️ by
    <a href="https://www.linkedin.com/in/shoubhya-sinha-135199380/"
    target="_blank">
    Shoubhya Sinha
    </a><br><br>
    © 2026 DataSense AutoMLSS
    </div>
    """, unsafe_allow_html=True)


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        """,
        unsafe_allow_html=True,
    )