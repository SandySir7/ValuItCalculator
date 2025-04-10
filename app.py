import streamlit as st
import os
import pandas as pd
from datetime import datetime
from pages import home, valuation_tool, my_valuations, professional_mode, learn, company_info, about, faq

# Set page configuration
st.set_page_config(
    page_title="ValuIt | Company Valuation Made Simple",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'user' not in st.session_state:
    st.session_state.user = None
if 'valuations' not in st.session_state:
    st.session_state.valuations = []
if 'current_valuation' not in st.session_state:
    st.session_state.current_valuation = None
if 'pro_mode' not in st.session_state:
    st.session_state.pro_mode = False

# Simple authentication system
def authenticate():
    if st.session_state.user:
        return True
    
    auth_type = st.sidebar.radio("", ["Login", "Sign Up"])
    
    if auth_type == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            # In a real application, you would validate against a database
            # This is a simplified version for demonstration
            st.session_state.user = username
            st.sidebar.success(f"Welcome back, {username}!")
            st.rerun()
    else:
        username = st.sidebar.text_input("Choose Username")
        password = st.sidebar.text_input("Choose Password", type="password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")
        if st.sidebar.button("Sign Up"):
            if password == confirm_password:
                # In a real application, you would store in a database
                st.session_state.user = username
                st.sidebar.success(f"Account created! Welcome, {username}!")
                st.rerun()
            else:
                st.sidebar.error("Passwords do not match!")
    
    return False

# Sidebar navigation
def sidebar():
    st.sidebar.title("ValuIt")
    st.sidebar.caption("Company Valuation Made Simple")
    
    if st.session_state.user:
        st.sidebar.write(f"Logged in as: {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
            
        # Pro mode toggle for authenticated users
        st.session_state.pro_mode = st.sidebar.checkbox("Professional Mode", value=st.session_state.pro_mode)
        
        if st.session_state.pro_mode:
            st.sidebar.success("Professional Mode Activated!")
        
    else:
        authenticated = authenticate()
        if not authenticated:
            st.sidebar.warning("Some features require login.")
    
    # Navigation options
    nav_selection = st.sidebar.radio(
        "Navigation",
        ["Home", "Valuation Tool", "My Valuations", "Professional Mode", "Learn", "Company Info", "FAQ", "About"]
    )
    
    # Credit at the bottom of sidebar
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2023 ValuIt")
    
    return nav_selection

# Main application logic
def main():
    nav_selection = sidebar()
    
    # Route to the appropriate page based on navigation selection
    if nav_selection == "Home":
        home()
    elif nav_selection == "Valuation Tool":
        valuation_tool(pro_mode=st.session_state.pro_mode)
    elif nav_selection == "My Valuations":
        if st.session_state.user:
            my_valuations()
        else:
            st.warning("Please login to access your saved valuations.")
            home()
    elif nav_selection == "Professional Mode":
        if st.session_state.user and st.session_state.pro_mode:
            professional_mode()
        else:
            st.warning("Professional Mode requires login and activation.")
            home()
    elif nav_selection == "Learn":
        learn()
    elif nav_selection == "Company Info":
        company_info()
    elif nav_selection == "FAQ":
        faq()
    elif nav_selection == "About":
        about()

if __name__ == "__main__":
    main()
