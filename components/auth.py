"""
Enterprise Authentication System
Sentinel AI - Buffalo Hackathon 2025
"""
import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import secrets

class AuthManager:
    def __init__(self, users_file='config/users.json'):
        self.users_file = users_file
        self.session_duration = 24  # hours
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create default users file if it doesn't exist"""
        if not os.path.exists(self.users_file):
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            default_users = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "role": "admin",
                    "name": "System Administrator",
                    "email": "admin@sentinel.ai",
                    "created": datetime.now().isoformat()
                },
                "demo": {
                    "password": self._hash_password("demo123"),
                    "role": "analyst",
                    "name": "Demo User",
                    "email": "demo@sentinel.ai",
                    "created": datetime.now().isoformat()
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=2)
    
    def _hash_password(self, password):
        """Hash password with SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        """Load users from JSON file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def authenticate(self, username, password):
        """Authenticate user credentials"""
        users = self._load_users()
        
        if username in users:
            if users[username]['password'] == self._hash_password(password):
                return {
                    'username': username,
                    'role': users[username]['role'],
                    'name': users[username]['name'],
                    'email': users[username]['email']
                }
        return None
    
    def register_user(self, username, password, name, email, role='analyst'):
        """Register new user"""
        users = self._load_users()
        
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            'password': self._hash_password(password),
            'role': role,
            'name': name,
            'email': email,
            'created': datetime.now().isoformat()
        }
        
        self._save_users(users)
        return True, "User registered successfully"
    
    def login(self, username, password):
        """Login and create session"""
        user = self.authenticate(username, password)
        
        if user:
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.session_token = secrets.token_hex(16)
            st.session_state.login_time = datetime.now()
            return True
        return False
    
    def logout(self):
        """Logout and clear session"""
        for key in ['authenticated', 'user', 'session_token', 'login_time']:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        if not st.session_state.get('authenticated', False):
            return False
        
        # Check session expiration
        login_time = st.session_state.get('login_time')
        if login_time:
            if datetime.now() - login_time > timedelta(hours=self.session_duration):
                self.logout()
                return False
        
        return True
    
    def get_current_user(self):
        """Get current logged-in user"""
        return st.session_state.get('user', None)
    
    def require_auth(self):
        """Decorator to require authentication"""
        if not self.is_authenticated():
            st.warning("🔒 Please login to access this page")
            st.stop()
