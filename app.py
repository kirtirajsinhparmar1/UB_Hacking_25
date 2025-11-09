"""sentinel-ai.app
RiskRadar AI - Enterprise Adverse Media Screening Platform

Professional UI redesign for Buffalo Hackathon 2025
Dark enterprise aesthetic with glassmorphism and sophisticated data visualization
"""

import json
import os
import sys
import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from utils.news_fetcher import NewsFetcher
from models.screener import AdverseMediaScreener

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def check_password():
    """Professional authentication with RiskRadar AI theme"""
    
    def password_entered():
        if st.session_state["password"] == os.getenv("APP_PASSWORD", "demo123"):
            st.session_state["authenticated"] = True
            st.session_state["login_error"] = False
        else:
            st.session_state["authenticated"] = False
            st.session_state["login_error"] = True
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if "login_error" not in st.session_state:
        st.session_state["login_error"] = False
    
    if not st.session_state["authenticated"]:
        # Custom CSS matching RiskRadar AI theme
        st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display: none;}
            
            .stApp {
                background: linear-gradient(180deg, #0a1628 0%, #1a2332 100%);
            }
            
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            
            .stTextInput > label {
                color: #e2e8f0 !important;
                font-weight: 500;
                font-size: 0.95rem;
                margin-bottom: 0.5rem;
            }
            
            .stTextInput > div > div > input {
                background: rgba(15, 23, 42, 0.5) !important;
                border: 1px solid rgba(148, 163, 184, 0.2) !important;
                border-radius: 8px;
                padding: 0.9rem 1rem;
                font-size: 1rem;
                color: #ffffff !important;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #2dd4bf !important;
                box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.1) !important;
                background: rgba(15, 23, 42, 0.7) !important;
            }
            
            .stTextInput > div > div > input::placeholder {
                color: #64748b;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 4vh;'></div>", unsafe_allow_html=True)
        
        st.markdown("""<div style="max-width: 520px; margin: 0 auto; background: rgba(26, 35, 50, 0.6); border: 1px solid rgba(45, 212, 191, 0.1); padding: 3rem 2.5rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); backdrop-filter: blur(10px);"><div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 2.5rem;"><div style="width: 64px; height: 64px; background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 4px 16px rgba(45, 212, 191, 0.3); flex-shrink: 0;">🛡️</div><div><h1 style="font-size: 2.2rem; font-weight: 700; color: #ffffff; margin: 0; letter-spacing: -0.5px;">RiskRadar AI</h1><p style="color: #94a3b8; font-size: 0.95rem; margin: 0.25rem 0 0 0; font-weight: 400;">Enterprise Risk Intelligence</p></div></div><div style="text-align: center; margin-bottom: 2rem;"><h2 style="font-size: 1.75rem; font-weight: 600; color: #ffffff; margin-bottom: 0.5rem;">Adverse Media <span style="color: #2dd4bf;">Screening</span></h2><p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6; max-width: 440px; margin: 0 auto;">AI-powered risk intelligence for compliance and regulatory teams. Analyze entities in real-time with bank-grade accuracy.</p></div>""", unsafe_allow_html=True)
        
        if st.session_state.get("login_error", False):
            st.markdown("""<div style="background: rgba(239, 68, 68, 0.1); border-left: 3px solid #ef4444; padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1.25rem; color: #fca5a5; font-weight: 500; font-size: 0.9rem;">⚠️ Invalid password. Please try again.</div>""", unsafe_allow_html=True)
        
        st.text_input("Password", type="password", on_change=password_entered, key="password", placeholder="Enter your password")
        
        st.markdown("""<div style="background: rgba(45, 212, 191, 0.08); border-left: 3px solid #2dd4bf; padding: 1rem 1.25rem; border-radius: 8px; margin-top: 1.5rem;"><div style="font-weight: 600; color: #2dd4bf; margin-bottom: 0.4rem; font-size: 0.9rem;">🔑 Demo Access</div><p style="color: #cbd5e1; margin: 0; font-size: 0.9rem;">Use password: <code style="background: rgba(45, 212, 191, 0.15); padding: 3px 10px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 0.9rem; color: #2dd4bf; border: 1px solid rgba(45, 212, 191, 0.2);">demo123</code> to access the platform</p></div><div style="text-align: center; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid rgba(148, 163, 184, 0.1);"><div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.75rem;"><span style="color: #2dd4bf; font-weight: bold;">✓</span><span>Secured with enterprise-grade encryption</span></div><p style="color: #64748b; font-size: 0.85rem; margin-top: 0.75rem;">Need help? <a href="#" style="color: #2dd4bf; text-decoration: none; font-weight: 600;">Contact Support</a></p></div></div>""", unsafe_allow_html=True)
        
        return False
    
    return True

# Add at start of main code
if not check_password():
    st.stop()
# Rest of your app continues...



# -----------------------
# Professional Dark Theme CSS
# -----------------------
PROFESSIONAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --slate-950: #020617;
  --slate-900: #0f172a;
  --slate-800: #1e293b;
  --slate-700: #334155;
  --slate-600: #475569;
  --slate-500: #64748b;
  --slate-400: #94a3b8;
  --slate-300: #cbd5e1;
  --emerald-500: #10b981;
  --emerald-400: #34d399;
  --cyan-500: #06b6d4;
  --cyan-400: #22d3ee;
  --orange-500: #f97316;
  --red-500: #ef4444;
  --amber-500: #f59e0b;
}

/* Global Dark Theme */
.stApp {
  background: linear-gradient(135deg, var(--slate-900) 0%, var(--slate-950) 50%, var(--slate-900) 100%);
  font-family: 'Inter', -apple-system, system-ui, sans-serif;
  color: white;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Top Navigation Bar */
.nav-bar {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
  padding: 1rem 2rem;
  margin: -5rem -5rem 2rem -5rem;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-container{
  display:flex;
  align-items:center;          
  gap: .625rem;             
}

.brand-icon{
  width: 40px;                 
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--emerald-400), var(--cyan-500));
  display:flex; align-items:center; justify-content:center;
  font-size: 18px; font-weight:700;
  box-shadow: 0 6px 18px rgba(16,185,129,.22);
}

.brand-text h1{
  margin:0;
  font-size: 1.75rem;          
  line-height: 0.5;         
  letter-spacing:-.02em;
}

.brand-text p{
  margin: 1px 0 0;          
  font-size: .9rem;         
  line-height: 1.2;       
  color: var(--slate-400);
  font-weight: 500;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 999px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--emerald-400);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--emerald-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Hero Section */
.hero-section {
  text-align: center;
  padding: 4rem 2rem 3rem;
  max-width: 900px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1rem;
  letter-spacing: -0.03em;
}

.gradient-text {
  background: linear-gradient(135deg, var(--emerald-400), var(--cyan-400));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.125rem;
  color: var(--slate-400);
  max-width: 700px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

/* Glass Card */
.glass-card {
  background: rgba(30, 41, 59, 0.4);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(51, 65, 85, 0.5);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 900px;
  margin: 0 auto 2rem;
}

/* Input Styling */
.stTextInput input {
  background: rgba(15, 23, 42, 0.5) !important;
  border: 1px solid var(--slate-700) !important;
  border-radius: 12px !important;
  color: white !important;
  font-size: 1rem !important;
  padding: 1rem !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}

.stTextInput input:focus {
  outline: none !important;
  border-color: var(--emerald-500) !important;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
}

.stTextInput input::placeholder {
  color: var(--slate-500) !important;
}

/* Primary Button */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--emerald-500), var(--cyan-500)) !important;
  color: white !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 1rem 2rem !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3) !important;
  transition: all 0.3s ease !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 32px rgba(16, 185, 129, 0.4) !important;
}

/* Secondary Buttons (Quick Start) */
.stButton > button:not([kind="primary"]) {
  background: rgba(30, 41, 59, 0.5) !important;
  color: var(--slate-300) !important;
  border: 1px solid var(--slate-700) !important;
  border-radius: 10px !important;
  padding: 0.625rem 1.25rem !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  transition: all 0.3s ease !important;
  text-transform: none !important;
}

.stButton > button:not([kind="primary"]):hover {
  border-color: var(--slate-600) !important;
  background: rgba(30, 41, 59, 0.7) !important;
}

/* Expander (Advanced Options) */
.stExpander {
  background: transparent !important;
  border: 1px solid rgba(51, 65, 85, 0.3) !important;
  border-radius: 12px !important;
}

.stExpander summary {
  color: var(--slate-400) !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  padding: 0.75rem !important;
}

.stExpander summary:hover {
  color: var(--emerald-400) !important;
}

.stExpander[open] {
  border-color: rgba(51, 65, 85, 0.5) !important;
}

/* Select / Dropdown */
.stSelectbox > div > div {
  background: rgba(15, 23, 42, 0.5) !important;
  border: 1px solid var(--slate-700) !important;
  border-radius: 10px !important;
  color: white !important;
}

.stSelectbox label {
  color: var(--slate-400) !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

/* Slider */
.stSlider label {
  color: var(--slate-400) !important;
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}

.stSlider [data-baseweb="slider"] {
  padding-top: 1rem;
}

.stSlider [data-baseweb="slider"] > div {
  background: rgba(100, 116, 139, 0.3) !important;
  height: 4px;
}

.stSlider [data-baseweb="slider"] > div > div {
  background: linear-gradient(90deg, var(--emerald-500), var(--cyan-500)) !important;
  height: 4px;
}

.stSlider [data-baseweb="slider"] button {
  background: white !important;
  border: 2px solid var(--emerald-500) !important;
  width: 16px !important;
  height: 16px !important;
}

/* KPI Metric Cards */
.metric-card {
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(51, 65, 85, 0.5);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.metric-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  transform: translateY(-4px);
}

.metric-label {
  color: var(--slate-400);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

.metric-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  line-height: 1;
  margin-bottom: 0.75rem;
}

.severity-badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-low {
  background: rgba(16, 185, 129, 0.15);
  color: var(--emerald-400);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-medium {
  background: rgba(245, 158, 11, 0.15);
  color: var(--amber-500);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-high {
  background: rgba(249, 115, 22, 0.15);
  color: var(--orange-500);
  border: 1px solid rgba(249, 115, 22, 0.3);
}

.badge-critical {
  background: rgba(239, 68, 68, 0.15);
  color: var(--red-500);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  gap: 1rem;
  border-bottom: 1px solid rgba(51, 65, 85, 0.5);
  padding-bottom: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
  color: var(--slate-500) !important;
  font-weight: 600 !important;
  font-size: 0.875rem !important;
  padding: 0.75rem 1rem !important;
  border: none !important;
  background: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
  color: var(--slate-300) !important;
}

.stTabs [aria-selected="true"] {
  color: var(--emerald-400) !important;
  border-bottom: 2px solid var(--emerald-400) !important;
}

/* Risk Progress Bars */
.risk-row {
  margin: 1rem 0;
}

.risk-label {
  color: var(--slate-300);
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.risk-bar-container {
  height: 10px;
  background: rgba(15, 23, 42, 0.5);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
}

.risk-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 1s ease-out;
}

/* Download Buttons */
.stDownloadButton button {
  background: rgba(30, 41, 59, 0.5) !important;
  color: white !important;
  border: 1px solid var(--slate-700) !important;
  border-radius: 12px !important;
  padding: 0.875rem 1.5rem !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.stDownloadButton button:hover {
  border-color: var(--slate-600) !important;
  background: rgba(30, 41, 59, 0.7) !important;
}

/* Progress Bar */
.stProgress > div > div {
  background: linear-gradient(90deg, var(--emerald-500), var(--cyan-500)) !important;
}

/* Info/Success/Error Messages */
.stAlert {
  background: rgba(30, 41, 59, 0.5) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(51, 65, 85, 0.5) !important;
  border-radius: 12px !important;
  color: white !important;
}

/* Footer */
.footer {
  text-align: center;
  padding: 3rem 0 2rem;
  color: var(--slate-500);
  font-size: 0.875rem;
  border-top: 1px solid rgba(51, 65, 85, 0.3);
  margin-top: 4rem;
}

.sponsor-list {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-top: 0.75rem;
  color: var(--slate-600);
  font-size: 0.8125rem;
}

/* Results Container */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.results-title {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin: 0;
}

.results-meta {
  color: var(--slate-400);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Markdown overrides */
div[data-testid="stMarkdownContainer"] p {
  color: var(--slate-300);
}

div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3 {
  color: white;
}

/* Section spacing */
.section-spacing {
  margin: 2rem 0;
}
</style>
"""

st.set_page_config(
    page_title="RiskRadar AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)


# -----------------------
# Helper Functions
# -----------------------
def _safe_entity_fragment(name: str) -> str:
    if not isinstance(name, str):
        name = str(name or "unknown")
    return name.strip().replace(" ", "_")


def _export_filename(entity_name: str, ext: str = "json") -> str:
    fragment = _safe_entity_fragment(entity_name)
    return f"sentinel_{fragment}_{datetime.now().strftime('%Y%m%d')}.{ext}"


# -----------------------
# Session State
# -----------------------
if "screening_result" not in st.session_state:
    st.session_state.screening_result = None
if "screening_history" not in st.session_state:
    st.session_state.screening_history = []
if "entity_input" not in st.session_state:
    st.session_state["entity_input"] = ""
if st.session_state.get("pending_quickstart"):
    st.session_state["entity_input"] = st.session_state.pop("pending_quickstart")
    st.session_state["queued_quickstart"] = True
elif "queued_quickstart" not in st.session_state:
    st.session_state["queued_quickstart"] = False


@st.cache_data(show_spinner=False, ttl=3600)
def _cached_articles(entity_name: str, days_back: int, max_articles: int):
    fetcher = NewsFetcher()
    return fetcher.fetch_all_news(entity_name, days_back, max_articles)


# -----------------------
# Top Navigation Bar
# -----------------------
st.markdown("""
<div class="nav-bar">
  <div class="nav-content">
    <div class="brand-container">
      <div class="brand-icon">🛡️</div>
      <div class="brand-text">
        <h1>RiskRadar AI</h1>
        <p>Enterprise Risk Intelligence</p>
      </div>
    </div>
    
  </div>
</div>
""", unsafe_allow_html=True)


# -----------------------
# Main Content
# -----------------------
if not st.session_state.screening_result:
    # Hero Section
    st.markdown("""
    <div class="hero-section">
      <h1 class="hero-title">
        Adverse Media <span class="gradient-text">Screening</span>
      </h1>
      <p class="hero-subtitle">
        AI-powered risk intelligence for compliance and regulatory teams. 
        Analyze entities in real-time with bank-grade accuracy.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Input Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    scan_clicked = False
    cols = st.columns([4, 1])
    
    with cols[0]:
        entity_name_widget = st.text_input(
            "Entity Name",
            placeholder="Enter company or individual (e.g., Tesla, JP Morgan)",
            label_visibility="collapsed",
            key="entity_input"
        )
    
    with cols[1]:
        scan_clicked = st.button("Initiate Screening", type="primary", use_container_width=True)
    
    # Advanced Options
    with st.expander("⚙️ Advanced Configuration"):
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        with adv_col1:
            days_back = st.select_slider(
                "Time Range",
                options=[7, 30, 60, 90, 180, 365],
                value=90,
                format_func=lambda x: f"{x} days",
                key="days_back"
            )
        with adv_col2:
            max_articles = st.select_slider(
                "Max Articles",
                options=[10, 25, 50, 75, 100],
                value=50,
                key="max_articles"
            )
        with adv_col3:
            model_choice = st.selectbox(
                "AI Model",
                options=[
                    "openai/gpt-3.5-turbo",
                    "openai/gpt-4o",
                    "anthropic/claude-3-haiku",
                    "anthropic/claude-3.5-sonnet"
                ],
                index=0,
                key="model_choice"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Start
    st.markdown('<div class="section-spacing">', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:var(--slate-500); font-size:0.875rem; margin-bottom:1rem;">Quick Start</p>', unsafe_allow_html=True)
    
    example_cols = st.columns(5)
    examples = ["Tesla", "JP Morgan", "Wells Fargo", "Binance", "Bank of America"]
    for col, example in zip(example_cols, examples):
        with col:
            if st.button(example, key=f"example_{example}", use_container_width=True):
                st.session_state["pending_quickstart"] = example
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.pop("queued_quickstart", False):
        scan_clicked = True
    
    # Process Scan
    if scan_clicked and st.session_state.get("entity_input"):
        entity_name = st.session_state.get("entity_input")
        progress = st.progress(0)
        status = st.empty()
        
        try:
            status.info("📰 Collecting recent publications")
            progress.progress(20)
            
            articles = _cached_articles(entity_name, days_back, max_articles)
            
            if not articles:
                status.error(f"No articles found for '{entity_name}'. Try a wider time range.")
                progress.empty()
                st.stop()
            
            status.info(f"🤖 Analyzing {len(articles)} articles")
            progress.progress(50)
            time.sleep(0.25)
            
            screener = AdverseMediaScreener(model=model_choice)
            result = screener.screen_entity(articles, entity_name)
            
            st.session_state.screening_result = result
            st.session_state.screening_history.append({
                "entity": entity_name,
                "timestamp": datetime.now().isoformat(),
                "severity": result.get("overall_severity")
            })
            
            progress.progress(100)
            status.success("✅ Analysis complete")
            time.sleep(0.25)
            progress.empty()
            status.empty()
            st.rerun()
        
        except Exception as exc:
            status.error(f"Unable to complete screening: {exc}")
            progress.empty()
            st.stop()

# -----------------------
# Results View
# -----------------------
if st.session_state.screening_result:
    result = st.session_state.screening_result
    
    # Header
    st.markdown('<div class="section-spacing">', unsafe_allow_html=True)
    header_col, action_col = st.columns([4, 1])
    with header_col:
        st.markdown(f'<h2 class="results-title">Risk Assessment Report</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="results-meta">{result["entity_name"]} • {result.get("articles_analyzed", 0)} articles analyzed</p>', unsafe_allow_html=True)
    with action_col:
        if st.button("New Screening", use_container_width=True):
            st.session_state.screening_result = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Severity Logic
    severity = result.get("overall_severity", 0)
    if severity > 75:
        badge_class, severity_label = "badge-critical", "CRITICAL"
    elif severity > 50:
        badge_class, severity_label = "badge-high", "HIGH"
    elif severity > 25:
        badge_class, severity_label = "badge-medium", "MEDIUM"
    else:
        badge_class, severity_label = "badge-low", "LOW"
    
    # KPI Metrics
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Overall Severity</div>
          <div class="metric-value">{severity}/100</div>
          <span class="severity-badge {badge_class}">{severity_label}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        articles_count = result.get("articles_analyzed", 0)
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Articles Screened</div>
          <div class="metric-value">{articles_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        high_count = len(result.get("high_risk_articles", []))
        pct = (high_count / articles_count * 100) if articles_count else 0
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">High-Risk Alerts</div>
          <div class="metric-value">{high_count}</div>
          <p style="color:var(--slate-500); font-size:0.8125rem; margin:0;">{pct:.1f}% flagged</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        primary = result.get("primary_risk", "N/A").replace("_", " ").title()
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">Primary Risk</div>
          <div class="metric-value" style="font-size:1.25rem;">{primary}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Risk Breakdown", "Alerts", "Analytics", "Export"])
    
    with tab1:
        risk_scores = result.get("risk_scores", {})
        
        # Bar Chart
        df_risks = pd.DataFrame({
            "Category": [k.replace("_", " ").title() for k in risk_scores.keys()],
            "Score": list(risk_scores.values())
        }).sort_values("Score", ascending=True)
        
        fig = px.bar(
            df_risks,
            y="Category",
            x="Score",
            orientation="h",
            text="Score",
            color="Score",
            color_continuous_scale=["#10b981", "#f59e0b", "#ef4444"]
        )
        fig.update_layout(
            title="Risk Category Distribution",
            xaxis_title="Score (0-100)",
            yaxis_title="",
            height=420,
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5e1", size=13),
            showlegend=False
        )
        fig.update_traces(texttemplate="%{text}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        
        # Progress Bars
        for cat, score in sorted(risk_scores.items(), key=lambda x: x[1], reverse=True):
            if score > 60:
                color = "#ef4444"
            elif score > 30:
                color = "#f59e0b"
            else:
                color = "#10b981"
            
            st.markdown(f"""
            <div class="risk-row">
              <div class="risk-label">
                <span>{cat.replace('_', ' ').title()}</span>
                <span>{score}/100</span>
              </div>
              <div class="risk-bar-container">
                <div class="risk-bar-fill" style="width:{score}%; background:{color};"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        high_articles = result.get("high_risk_articles", [])
        if high_articles:
            st.markdown(f"### High-Risk Articles ({len(high_articles)})")
            for art in sorted(high_articles, key=lambda x: x.get("overall_severity", 0), reverse=True)[:15]:
                sev = art.get("overall_severity", 0)
                title = art.get("article_title", "Untitled")
                with st.expander(f"Severity {sev}/100 • {title[:100]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Source:** {art.get('source', 'Unknown')}")
                        st.markdown(f"**Date:** {art.get('publish_date', '')[:10]}")
                    with col2:
                        st.markdown(f"**Primary Risk:** {art.get('primary_risk', 'N/A').replace('_', ' ').title()}")
                    
                    st.markdown("**Key Evidence:**")
                    for sent in art.get("key_sentences", [])[:3]:
                        if isinstance(sent, dict):
                            st.markdown(f"- {sent.get('sentence', '')}")
                    
                    st.info(art.get("explanation", "No explanation"))
                    if art.get("article_url"):
                        st.markdown(f"[View Full Article]({art.get('article_url')})")
        else:
            st.success("No high-risk articles detected.")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            labels = [k.replace("_", " ").title() for k in risk_scores.keys()]
            values = list(risk_scores.values())
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
            fig_pie.update_layout(
                title="Risk Distribution",
                height=380,
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5e1")
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            all_sev = [a.get("overall_severity", 0) for a in result.get("all_assessments", [])]
            fig_hist = go.Figure(data=[go.Histogram(x=all_sev, nbinsx=20, marker_color="#10b981")])
            fig_hist.update_layout(
                title="Severity Distribution",
                xaxis_title="Severity Score",
                yaxis_title="Article Count",
                height=380,
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5e1")
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab4:
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            json_data = json.dumps(result, indent=2)
            st.download_button(
                "📥 Download JSON",
                data=json_data,
                file_name=_export_filename(result.get("entity_name", "entity"), ext="json"),
                mime="application/json",
                key="download_json",
                use_container_width=True
            )
        with col2:
            summary_df = pd.DataFrame([{
                "Entity": result.get("entity_name"),
                "Date": result.get("screening_date", "")[:10],
                "Severity": result.get("overall_severity"),
                "Primary_Risk": result.get("primary_risk"),
                **result.get("risk_scores", {})
            }])
            st.download_button(
                "📊 Download CSV",
                data=summary_df.to_csv(index=False),
                file_name=_export_filename(result.get("entity_name", "entity"), ext="csv"),
                mime="text/csv",
                key="download_csv",
                use_container_width=True
            )
        with col3:
            st.markdown('<p style="color:var(--slate-400); font-size:0.875rem;">Export screening results for downstream compliance reporting and audit trails.</p>', unsafe_allow_html=True)

# -----------------------
# Footer
# -----------------------
st.markdown("""
<div class="footer">
  <p><strong>RiskRadar AI</strong> — Enterprise Adverse Media Screening</p>
  <div class="sponsor-list">
    <span>UB Hacking 2025</span>
    <span>•</span>
    <span>M&T Tech</span>
    <span>•</span>
    <span>Valmar Holdings</span>
    <span>•</span>
    <span>Odoo</span>
    <span>•</span>
    <span>Radial Ventures</span>
  </div>
</div>
""", unsafe_allow_html=True)