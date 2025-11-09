"""
Settings Page
Sentinel AI
"""
import streamlit as st
from components.auth import AuthManager

def show():
    auth = AuthManager()
    user = auth.get_current_user()
    
    st.markdown("""
    <div class="page-header">
        <h1>⚙️ Settings</h1>
        <p>Manage your account and preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔔 Notifications", "🔐 Security"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 👤 Profile Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", value=user['name'])
            st.text_input("Username", value=user['username'], disabled=True)
        with col2:
            st.text_input("Email", value=user['email'])
            st.text_input("Role", value=user['role'].title(), disabled=True)
        
        if st.button("💾 Save Changes", type="primary"):
            st.success("✅ Profile updated successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔔 Notification Preferences")
        
        st.checkbox("Email notifications for high-risk alerts", value=True)
        st.checkbox("Weekly summary reports", value=True)
        st.checkbox("System updates and announcements", value=False)
        
        if st.button("💾 Save Preferences", type="primary"):
            st.success("✅ Preferences saved!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Change Password")
        
        current_pw = st.text_input("Current Password", type="password")
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm New Password", type="password")
        
        if st.button("🔒 Update Password", type="primary"):
            if new_pw == confirm_pw and len(new_pw) >= 6:
                st.success("✅ Password updated successfully!")
            else:
                st.error("❌ Passwords don't match or too short")
        
        st.markdown('</div>', unsafe_allow_html=True)
