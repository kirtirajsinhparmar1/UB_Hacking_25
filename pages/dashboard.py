"""
Dashboard Page
Sentinel AI
"""
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show():
    st.markdown("""
    <div class="page-header">
        <h1>📊 Dashboard</h1>
        <p>Real-time monitoring and analytics overview</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Total Screenings", "1,234", delta="↑ 12% vs last month")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("High-Risk Alerts", "47", delta="↓ 8% vs last month", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Avg Severity", "32/100", delta="↓ 5 points")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Articles Analyzed", "61,543", delta="↑ 23%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Screening Trend (Last 30 Days)")
        
        # Generate sample data
        days = [(datetime.now() - timedelta(days=x)).strftime("%b %d") for x in range(30, 0, -1)]
        screenings = [random.randint(30, 60) for _ in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days,
            y=screenings,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Risk Category Distribution")
        
        fig = go.Figure(data=[go.Pie(
            labels=['Fraud', 'Sanctions', 'AML', 'Bribery', 'Cyber', 'Insolvency', 'ESG'],
            values=[25, 18, 22, 12, 8, 10, 5],
            hole=0.5,
            marker=dict(colors=['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#17a2b8', '#6610f2', '#6c757d'])
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🕐 Recent Screenings")
    
    recent_data = {
        "Entity": ["Tesla Inc", "JP Morgan Chase", "Wells Fargo", "Bank of America", "Binance"],
        "Severity": [78, 45, 62, 38, 85],
        "Primary Risk": ["ESG Violation", "Fraud", "AML", "Compliance", "Sanctions"],
        "Date": ["2 hours ago", "5 hours ago", "1 day ago", "1 day ago", "2 days ago"]
    }
    
    import pandas as pd
    df = pd.DataFrame(recent_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
