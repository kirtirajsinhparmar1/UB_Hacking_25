"""
Screen Entity Page
Sentinel AI
"""
import streamlit as st
from datetime import datetime
import time

def show():
    st.markdown("""
    <div class="page-header">
        <h1>🔍 Screen Entity</h1>
        <p>Perform comprehensive adverse media analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        entity_name = st.text_input(
            "Entity Name",
            placeholder="Enter company or individual name",
            label_visibility="collapsed"
        )
    
    with col2:
        scan_button = st.button("🚀 Start Screening", type="primary", use_container_width=True)
    
    # Advanced Options
    with st.expander("⚙️ Advanced Configuration"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            days_back = st.select_slider("Time Range", options=[7, 30, 60, 90, 180, 365], value=90)
        with col2:
            max_articles = st.select_slider("Max Articles", options=[10, 25, 50, 75, 100], value=50)
        with col3:
            model = st.selectbox("AI Model", ["gpt-3.5-turbo", "gpt-4o", "claude-3-haiku"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Examples
    st.markdown("### 💡 Quick Start Examples")
    cols = st.columns(5)
    examples = ["Tesla", "JP Morgan", "Wells Fargo", "Binance", "Walmart"]
    
    for col, example in zip(cols, examples):
        with col:
            if st.button(example, key=f"ex_{example}", use_container_width=True):
                entity_name = example
                scan_button = True
    
    # Processing
    if scan_button and entity_name:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### 🔄 Analyzing **{entity_name}**...")
        
        progress = st.progress(0)
        status = st.empty()
        
        steps = [
            ("📰 Fetching news articles", 25),
            ("🤖 AI risk analysis", 50),
            ("📊 Processing results", 75),
            ("✅ Generating report", 100)
        ]
        
        for step, pct in steps:
            status.info(step)
            time.sleep(1)
            progress.progress(pct)
        
        status.success("✅ Screening complete!")
        time.sleep(0.5)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Mock Results
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"## 📊 Results: **{entity_name}**")
        
        cols = st.columns(4)
        with cols[0]:
            st.metric("Severity", "65/100")
        with cols[1]:
            st.metric("Articles", "42")
        with cols[2]:
            st.metric("High-Risk", "7")
        with cols[3]:
            st.metric("Primary Risk", "Fraud")
        
        st.success("Full analysis complete. View detailed breakdown in History.")
        st.markdown('</div>', unsafe_allow_html=True)
