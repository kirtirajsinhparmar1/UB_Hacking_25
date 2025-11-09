"""
Screening History Page
Sentinel AI
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def show():
    st.markdown("""
    <div class="page-header">
        <h1>📊 Screening History</h1>
        <p>View and analyze past screenings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_severity = st.selectbox("Filter by Severity", ["All", "High (60+)", "Medium (30-60)", "Low (<30)"])
    with col2:
        filter_risk = st.selectbox("Filter by Risk Type", ["All", "Fraud", "Sanctions", "AML", "Bribery", "Cyber", "ESG"])
    with col3:
        filter_date = st.selectbox("Date Range", ["Last 7 days", "Last 30 days", "Last 90 days", "All time"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate sample history
    entities = ["Tesla", "JP Morgan", "Wells Fargo", "Bank of America", "Binance", "Walmart", "Amazon", "Apple"]
    risks = ["Fraud", "Sanctions", "AML", "Bribery", "Cyber", "ESG", "Insolvency"]
    
    history_data = []
    for i in range(20):
        history_data.append({
            "Date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d %H:%M"),
            "Entity": random.choice(entities),
            "Severity": random.randint(15, 95),
            "Primary Risk": random.choice(risks),
            "Articles": random.randint(20, 80),
            "Status": "Complete"
        })
    
    df = pd.DataFrame(history_data).sort_values("Date", ascending=False)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 Screening Records")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Severity": st.column_config.ProgressColumn(
                "Severity",
                help="Risk severity score",
                min_value=0,
                max_value=100,
            ),
        }
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button("📥 Export CSV", df.to_csv(index=False), "screening_history.csv", "text/csv", use_container_width=True)
    with col2:
        st.download_button("📥 Export JSON", df.to_json(orient='records'), "screening_history.json", "application/json", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
