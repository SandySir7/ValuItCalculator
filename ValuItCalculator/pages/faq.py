import streamlit as st

def show():
    """Display the FAQ page"""
    
    st.title("Frequently Asked Questions")
    
    st.write("""
    Find answers to common questions about ValuIt and company valuation. If you don't see 
    your question answered here, please contact our support team at support@valuit.com.
    """)
    
    # General questions
    with st.expander("General Questions", expanded=True):
        with st.expander("What is ValuIt?"):
            st.write("""
            ValuIt is a web-based platform that provides accessible, professional-grade company 
            valuation tools. Our platform allows users to perform valuations using several 
            established methodologies including Discounted Cash Flow (DCF), Comparable Company 
            Analysis, Precedent Transactions, and Asset-Based Valuation.
            """)
        
        with st.expander("Who is ValuIt for?"):
            st.write("""
            ValuIt is designed for a wide range of users, including:
            
            - Finance students learning valuation principles
            - Startup founders valuing their businesses
            - Small business owners considering M&A opportunities
            - Investment professionals seeking efficient valuation tools
            - MBA students working on case studies or projects
            - Angel investors and venture capitalists
            - Financial analysts and consultants
            
            Our platform offers both basic and advanced features to accommodate users with different 
            levels of financial expertise.
            """)
        
        with st.expander("Is ValuIt free to use?"):
            st.write("""
            ValuIt operates on a freemium model:
            
            **Free Features:**
            - Basic company information lookup
            - Single valuation method (DCF)
            - Limited historical data access
            - Basic educational resources
            
            **Pro Features (Subscription):**
            - All valuation methods
            - Advanced inputs and scenarios
            - Save and compare multiple valuations
            - Export to PDF and Excel
            - Full access to learning resources
            - Professional validation option
            
            Visit our pricing page for current subscription rates and features.
            """)
        
        with st.expander("How accurate are ValuIt's valuations?"):
            st.write("""
            ValuIt provides valuations based on established financial methodologies used by 
            investment professionals. However, any valuation is only as good as its inputs and 
            assumptions. We provide:
            
            - Industry standard valuation models
            - Smart defaults based on industry benchmarks
            - Clear documentation of all assumptions
            - Sensitivity analysis tools
            
            Remember that valuation is both an art and a science, and different methodologies may 
            yield different results. We recommend using multiple methods and scenarios for a more 
            comprehensive analysis.
            """)
    
    # Account and data questions
    with st.expander("Account & Data Questions"):
        with st.expander("How do I create an account?"):
            st.write("""
            To create a ValuIt account:
            
            1. Click "Login" in the sidebar
            2. Select "Sign Up"
            3. Enter your email address and create a password
            4. Verify your email address by clicking the link sent to your inbox
            5. Complete your profile information
            
            Once your account is created, you can immediately begin using ValuIt's features.
            """)
        
        with st.expander("Where does ValuIt get its financial data?"):
            st.write("""
            ValuIt sources financial data from several reputable providers:
            
            - Company financial statements from SEC filings
            - Market data from major exchanges
            - Industry benchmarks from leading financial research firms
            - Economic indicators from government sources
            
            We combine these sources to provide comprehensive and reliable data for our valuation models.
            """)
        
        with st.expander("Is my data secure on ValuIt?"):
            st.write("""
            Yes, we take data security seriously:
            
            - All data is encrypted in transit and at rest
            - Your valuations and analyses are private by default
            - We do not sell user data to third parties
            - Our servers are hosted in secure, SOC 2 compliant facilities
            
            For more information, please review our Privacy Policy and Terms of Service.
            """)
        
        with st.expander("Can I export my valuations?"):
            st.write("""
            Yes, ValuIt allows you to export your valuations in several formats:
            
            - PDF reports with charts and analysis
            - Excel spreadsheets with detailed calculations
            - JSON data export for integration with other tools
            
            Export functionality is available to Pro users. Free users can view their valuations 
            online but have limited export capabilities.
            """)
    
    # Valuation questions
    with st.expander("Valuation Questions"):
        with st.expander("Which valuation method should I use?"):
            st.write("""
            The best valuation method depends on the company and your specific situation:
            
            **Discounted Cash Flow (DCF):**
            - Best for: Companies with predictable cash flows
            - Advantages: Forward-looking, captures growth
            - Challenges: Sensitive to assumptions, requires forecasting
            
            **Comparable Company Analysis:**
            - Best for: Companies in established industries with clear peers
            - Advantages: Market-based, relatively simple
            - Challenges: Requires truly comparable companies
            
            **Precedent Transactions:**
            - Best for: M&A scenarios, takeover valuation
            - Advantages: Includes control premiums, based on actual prices paid
            - Challenges: Transactions may not be recent or truly comparable
            
            **Asset-Based Valuation:**
            - Best for: Asset-heavy businesses, distressed companies
            - Advantages: Concrete, based on tangible assets
            - Challenges: May undervalue intangible assets and growth potential
            
            We recommend using multiple methods to establish a valuation range.
            """)
        
        with st.expander("What is WACC and how is it calculated?"):
            st.write("""
            WACC (Weighted Average Cost of Capital) represents the average rate a company is expected 
            to pay to finance its assets. It's a key input in DCF valuation as the discount rate.
            
            **WACC Formula:**
            
            WACC = (E/V × Re) + (D/V × Rd × (1-Tc))
            
            Where:
            - E = Market value of equity
            - D = Market value of debt
            - V = Total market value (E + D)
            - Re = Cost of equity
            - Rd = Cost of debt
            - Tc = Corporate tax rate
            
            The cost of equity (Re) is typically calculated using the Capital Asset Pricing Model (CAPM):
            
            Re = Rf + β × (Rm - Rf)
            
            Where:
            - Rf = Risk-free rate
            - β = Beta (volatility relative to the market)
            - Rm = Expected market return
            - (Rm - Rf) = Market risk premium
            
            In ValuIt, you can:
            - Use our default WACC based on industry averages
            - Provide your own WACC calculation
            - Use our WACC calculator in Professional Mode
            """)
        
        with st.expander("How do I interpret valuation results?"):
            st.write("""
            Interpreting valuation results requires considering several factors:
            
            **Enterprise Value vs. Equity Value:**
            - Enterprise Value: Total value of the business (debt + equity - cash)
            - Equity Value: Value available to shareholders
            
            **Valuation Ranges:**
            - Consider results as a range rather than a precise figure
            - Compare results from different methods
            - Use sensitivity analysis to understand key drivers
            
            **Relative Valuation:**
            - Compare multiples (EV/EBITDA, P/E) to industry benchmarks
            - Consider the company's growth, profitability, and risk profile
            
            **Context Matters:**
            - Stage of company (startup, growth, mature)
            - Industry trends and disruptions
            - Economic conditions
            - Control premiums for M&A scenarios
            
            Remember that valuation is a starting point for decision-making, not the final answer.
            """)
        
        with st.expander("What is terminal value and why is it important?"):
            st.write("""
            Terminal value represents the value of a business beyond the explicit forecast period in a 
            DCF model. It's critically important because it often represents 60-80% of the total valuation.
            
            **Calculation Methods:**
            
            1. **Perpetuity Growth Method:**
               Terminal Value = FCF_n × (1 + g) / (WACC - g)
               
               Where:
               - FCF_n = Free Cash Flow in final forecast year
               - g = Perpetual growth rate
               - WACC = Weighted Average Cost of Capital
            
            2. **Exit Multiple Method:**
               Terminal Value = EBITDA_n × EV/EBITDA multiple
               
               Where:
               - EBITDA_n = EBITDA in final forecast year
               - EV/EBITDA = Appropriate industry multiple
            
            **Key Considerations:**
            - Perpetual growth rate should not exceed long-term GDP growth (typically 2-3%)
            - Exit multiples should reflect expected future industry conditions
            - Terminal value is highly sensitive to small changes in assumptions
            
            ValuIt allows you to calculate terminal value using both methods and compare the results.
            """)
    
    # Technical questions
    with st.expander("Technical Questions"):
        with st.expander("Which browsers are supported?"):
            st.write("""
            ValuIt works best on modern browsers including:
            
            - Google Chrome (recommended)
            - Mozilla Firefox
            - Microsoft Edge
            - Safari
            
            For the best experience, we recommend using the latest version of any of these browsers.
            """)
        
        with st.expander("Can I use ValuIt on mobile devices?"):
            st.write("""
            Yes, ValuIt is designed to be responsive and works on mobile devices. However, due to the 
            complex nature of financial analysis, we recommend using a desktop or laptop for the best 
            experience, especially when working with detailed inputs or analyzing results.
            
            A dedicated mobile app is on our roadmap for future development.
            """)
        
        with st.expander("What if I encounter a technical issue?"):
            st.write("""
            If you experience technical issues:
            
            1. First, try refreshing your browser and clearing your cache
            2. Check our status page at status.valuit.com for any known issues
            3. Contact our support team at support@valuit.com with:
               - A description of the issue
               - Steps to reproduce the problem
               - Your browser and device information
               - Screenshots if possible
            
            Our support team typically responds within 24 hours on business days.
            """)
        
        with st.expander("Can I integrate ValuIt with other financial tools?"):
            st.write("""
            Currently, ValuIt offers:
            
            - Export functionality to PDF and Excel
            - JSON data export for custom integrations
            
            We're developing an API for more robust integrations, which will allow:
            - Integration with financial dashboards
            - Automated data flows from CRM and ERP systems
            - Custom reporting tools
            
            If you have specific integration needs, please contact us at partners@valuit.com.
            """)
    
    # Learning and support
    with st.expander("Learning & Support"):
        with st.expander("How can I learn more about valuation?"):
            st.write("""
            ValuIt offers several resources to help you learn about valuation:
            
            - **Learn Section:** Step-by-step guides explaining valuation methods
            - **Interactive Tutorials:** Built into the platform as you use it
            - **Valuation Quizzes:** Test your knowledge and understanding
            - **Certification Courses:** Structured learning paths (Pro feature)
            - **Tooltips and Explanations:** Throughout the platform
            
            We also recommend exploring the resources in our blog and knowledge base.
            """)
        
        with st.expander("Does ValuIt offer professional support?"):
            st.write("""
            Yes, we offer several levels of professional support:
            
            - **Standard Support:** Email support for all users
            - **Priority Support:** Faster response times for Pro subscribers
            - **Valuation Review:** Professional review of your valuation by our finance team (additional fee)
            - **Consulting Services:** One-on-one guidance for complex valuations (additional fee)
            
            To request professional support, contact support@valuit.com or use the "Get Expert Help" 
            button in the platform.
            """)
        
        with st.expander("Can I request new features?"):
            st.write("""
            We welcome feature requests from our users! To suggest a new feature:
            
            1. Email your idea to feedback@valuit.com
            2. Use the feedback form in the platform
            3. Vote on existing feature requests in our community portal
            
            We regularly review user suggestions and incorporate them into our development roadmap.
            """)
        
        with st.expander("Are there educational discounts available?"):
            st.write("""
            Yes, we offer educational discounts for:
            
            - Students (with valid .edu email)
            - Educational institutions
            - Professors using ValuIt in their courses
            
            We also offer special pricing for classroom use and academic research.
            
            To request an educational discount, contact education@valuit.com with proof of academic affiliation.
            """)
    
    # Contact section
    st.subheader("Still have questions?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        If you couldn't find the answer to your question, please contact our support team:
        
        **Email:** support@valuit.com  
        **Hours:** Monday-Friday, 9am-5pm EST
        """)
    
    with col2:
        st.write("""
        For feedback or feature requests:
        
        **Email:** feedback@valuit.com  
        **Community Forum:** [forum.valuit.com](#)
        """)

