import streamlit as st

def show():
    """Display the About page"""
    
    st.title("About ValuIt")
    
    st.write("""
    ValuIt was created to democratize company valuation, making robust financial 
    analysis accessible to everyone - from finance students to professional investors.
    """)
    
    # Company mission
    st.header("Our Mission")
    
    st.write("""
    Our mission is to empower individuals and organizations to make informed financial 
    decisions through accessible, transparent, and professional-grade valuation tools.
    
    We believe that:
    
    - Financial analysis should be accessible to everyone, not just financial professionals
    - Understanding a company's true value is key to making smart investment decisions
    - Complex financial concepts can be explained in clear, understandable terms
    - Technology can streamline and enhance the valuation process
    """)
    
    # Team information
    st.header("Our Team")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Alex Chen")
        st.write("Founder & CEO")
        st.write("""
        Former investment banker with 15 years of experience in M&A and corporate valuation. 
        MBA from Wharton Business School with a focus in Finance.
        """)
    
    with col2:
        st.subheader("Maya Rodriguez")
        st.write("Chief Technology Officer")
        st.write("""
        Computer science PhD with expertise in financial modeling algorithms and data 
        visualization. Previously led fintech engineering teams at major tech companies.
        """)
    
    with col3:
        st.subheader("Darius Johnson")
        st.write("Head of Finance & Education")
        st.write("""
        Former finance professor and CFA with extensive experience in equity research. 
        Author of three books on financial analysis and corporate valuation.
        """)
    
    # Company history
    st.header("Our Story")
    
    st.write("""
    ValuIt began in 2020 when our founder, Alex Chen, was teaching a finance course at 
    a local university. He noticed that students struggled with valuation concepts not 
    because they were incapable, but because the tools and resources were needlessly 
    complex and expensive.
    
    After a particularly frustrating session trying to explain DCF models using 
    traditional spreadsheets, Alex decided there had to be a better way. He teamed up 
    with Maya and Darius to create a platform that would combine financial rigor with 
    intuitive design.
    
    In our first year, we focused on helping finance students master valuation concepts. 
    Soon, startup founders and small business investors discovered our platform and 
    began using it for their own needs. Today, ValuIt serves thousands of users, from 
    students to professional analysts, all with the same mission: to make valuation 
    accessible to everyone.
    """)
    
    # Company values
    st.header("Our Values")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Accessibility")
        st.write("""
        We design our platform to be usable by people of all financial backgrounds, 
        from beginners to experts. Complex concepts are explained in clear language, 
        and our intuitive interface guides users through the valuation process.
        """)
        
        st.subheader("Transparency")
        st.write("""
        We believe in showing our work. All calculations, assumptions, and methodologies 
        are clearly explained, allowing users to understand not just the "what" but 
        the "why" behind their valuations.
        """)
    
    with col2:
        st.subheader("Accuracy")
        st.write("""
        While simplifying valuation, we never compromise on accuracy. Our models are built 
        on established financial principles and are regularly reviewed by finance experts 
        to ensure reliability.
        """)
        
        st.subheader("Education")
        st.write("""
        We're committed to helping our users learn. Our platform is designed not just as a 
        tool but as a learning experience, with embedded resources that explain concepts 
        as users apply them.
        """)
    
    # Future roadmap
    st.header("Our Roadmap")
    
    st.write("""
    ValuIt is continuously evolving. Here's what we're working on for the future:
    """)
    
    roadmap_items = [
        {
            "quarter": "Q3 2023",
            "features": [
                "Enhanced industry-specific valuation templates",
                "Integration with more financial data providers",
                "Expanded learning resources with video tutorials"
            ]
        },
        {
            "quarter": "Q4 2023",
            "features": [
                "Collaborative valuation workspaces for teams",
                "Advanced sensitivity analysis tools",
                "Mobile app for valuation on the go"
            ]
        },
        {
            "quarter": "Q1 2024",
            "features": [
                "AI-powered valuation suggestions",
                "Integration with major investment platforms",
                "Expanded professional certification program"
            ]
        },
        {
            "quarter": "Q2 2024",
            "features": [
                "Real-time collaboration features",
                "Industry benchmarking tools",
                "Expanded international market coverage"
            ]
        }
    ]
    
    for item in roadmap_items:
        st.subheader(item["quarter"])
        for feature in item["features"]:
            st.markdown(f"- {feature}")
    
    # Contact information
    st.header("Contact Us")
    
    st.write("""
    We'd love to hear from you! Whether you have questions, feedback, or partnership 
    inquiries, feel free to reach out.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("General Inquiries")
        st.write("info@valuit.com")
    
    with col2:
        st.subheader("Support")
        st.write("support@valuit.com")
    
    with col3:
        st.subheader("Partnerships")
        st.write("partners@valuit.com")
    
    # Social media links
    st.write("---")
    st.write("Follow us on social media:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("[LinkedIn](#)")
    
    with col2:
        st.write("[Twitter](#)")
    
    with col3:
        st.write("[Facebook](#)")
    
    with col4:
        st.write("[YouTube](#)")
    
    # Footer
    st.write("---")
    st.caption("© 2023 ValuIt - All Rights Reserved")

