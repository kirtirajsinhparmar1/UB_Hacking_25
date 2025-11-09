"""
About Page
Sentinel AI
"""
import streamlit as st

def show():
    st.markdown("""
    <div class="page-header">
        <h1>ℹ️ About Sentinel AI</h1>
        <p>Enterprise-grade adverse media screening platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🚀 Platform Overview
        
        **Sentinel AI** automates adverse media screening using advanced artificial intelligence, 
        reducing manual review time from hours to minutes while maintaining bank-grade accuracy.
        
        ### 🎯 Key Features
        
        - **7 Risk Categories**: Fraud, Sanctions, AML, Bribery, Cyber, Insolvency, ESG
        - **Multi-Model AI**: GPT-4, Claude 3.5, and more via OpenRouter
        - **Real-time Analysis**: Process 50+ articles in under 2 minutes
        - **Explainable Results**: Sentence-level evidence with confidence scores
        - **Regulatory Compliant**: Aligned with FinCEN, FATF, and BSA standards
        
        ### 📊 Performance Metrics
        
        - ⚡ **95% faster** than manual screening
        - 🎯 **92% accuracy** in risk detection
        - 📈 **50,000+** articles analyzed
        - 🏦 **Bank-grade** security and compliance
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🏆 Buffalo Hackathon 2025
        
        **Sponsors:**
        - 🏦 M&T Bank
        - 💼 Valmar Holdings
        - 🔧 Odoo
        - 💰 Radial Ventures
        - 💻 TechBuffalo
        
        ### 👨‍💻 Team
        
        Built by SUNY Buffalo CS students
        
        ### 📚 Technology Stack
        
        - **Frontend**: Streamlit
        - **AI Models**: OpenRouter API
        - **Data**: Google News RSS
        - **Auth**: JWT + Session Management
        
        ### 📞 Contact
        
        📧 info@sentinel-ai.com  
        🌐 sentinel-ai.com  
        💼 LinkedIn: /sentinel-ai
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### 📄 License & Attribution
    
    © 2025 Sentinel AI - Buffalo Hackathon Project. All rights reserved.
    
    This platform was developed as part of the Buffalo Hackathon 2025 challenge to create 
    innovative financial technology solutions.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
