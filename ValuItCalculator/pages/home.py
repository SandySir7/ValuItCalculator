import streamlit as st

def show():
    """Display the Home page"""
    
    # Hero section
    st.title("ValuIt: Company Valuation Made Simple")
    st.markdown("### Valuation, simplified.")
    
    st.write("""
    ValuIt is a user-friendly platform that makes company valuation accessible to everyone—
    from students to professionals. Using proven financial techniques, get accurate valuations 
    with just a few inputs.
    """)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; margin-bottom: 2rem;">
        <h3>Ready to value a company?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Now", use_container_width=True):
            st.session_state['nav_selection'] = "Valuation Tool"
            st.rerun()
    
    # Features overview
    st.markdown("## How It Works")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("### 1. Enter Company Details")
        st.markdown("""
        - Enter company name or ticker symbol
        - We'll auto-fill financial data when available
        - Adjust inputs or use smart defaults
        """)
        
        st.markdown("### 3. Visualize Results")
        st.markdown("""
        - Interactive charts and tables
        - Sensitivity analysis
        - Compare multiple valuation methods
        """)
    
    with features_col2:
        st.markdown("### 2. Choose Valuation Methods")
        st.markdown("""
        - Discounted Cash Flow (DCF)
        - Comparable Company Analysis
        - Precedent Transactions
        - Asset-Based Valuation
        - LBO (Pro mode)
        """)
        
        st.markdown("### 4. Save and Share")
        st.markdown("""
        - Export to PDF or Excel
        - Save valuations to your personal dashboard
        - Compare valuations over time
        """)
    
    # Testimonials
    st.markdown("## What Our Users Say")
    
    testimonials_col1, testimonials_col2, testimonials_col3 = st.columns(3)
    
    with testimonials_col1:
        st.markdown("""
        > "ValuIt helped me understand company valuation in a way my finance textbooks never could."
        
        **- Finance Student**
        """)
    
    with testimonials_col2:
        st.markdown("""
        > "I valued my startup before my pitch meeting and investors were impressed with the thoroughness."
        
        **- Startup Founder**
        """)
    
    with testimonials_col3:
        st.markdown("""
        > "The platform's simplicity doesn't compromise on the rigor of the valuation methods."
        
        **- Investment Analyst**
        """)
    
    # Learn more section
    st.markdown("## Learn More About Valuation")
    
    learn_col1, learn_col2 = st.columns(2)
    
    with learn_col1:
        st.markdown("### Valuation Methods Explained")
        st.markdown("""
        Visit our [Learn](#) section to discover the principles behind each valuation method:
        - How DCF models forecast future cash flows
        - When to use comparable company analysis
        - Understanding precedent transactions
        - Asset-based approaches for stable businesses
        """)
    
    with learn_col2:
        st.markdown("### ValuIt Pro Features")
        st.markdown("""
        Upgrade to Pro for advanced capabilities:
        - Custom WACC and terminal value assumptions
        - Scenario and sensitivity analysis
        - LBO modeling and analysis
        - Detailed projection tables
        - Save unlimited valuations
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p>© 2023 ValuIt | <a href="#about">About</a> | <a href="#faq">FAQ</a> | <a href="#terms">Terms</a> | <a href="#privacy">Privacy</a></p>
    </div>
    """, unsafe_allow_html=True)
