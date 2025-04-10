import streamlit as st
import pandas as pd

def show():
    """Display the Learn page"""
    
    st.title("Learn")
    
    st.write("""
    Welcome to the ValuIt learning center! Here you can explore valuation methods, 
    understand key financial concepts, and learn how to apply them effectively in your valuations.
    """)
    
    # Learning sections
    tab1, tab2, tab3, tab4 = st.tabs(["Valuation Methods", "Financial Concepts", "Quizzes", "Courses"])
    
    with tab1:
        st.subheader("Valuation Methods Explained")
        
        method = st.selectbox(
            "Select a valuation method to learn about",
            ["Discounted Cash Flow (DCF)", "Comparable Company Analysis", 
             "Precedent Transactions", "Asset-Based Valuation", "LBO Analysis"]
        )
        
        if method == "Discounted Cash Flow (DCF)":
            st.write("### Discounted Cash Flow (DCF)")
            
            st.write("""
            The Discounted Cash Flow (DCF) method values a company based on its expected future cash flows, 
            adjusted for the time value of money. This approach is widely used for companies with 
            predictable cash flows and growth trajectories.
            """)
            
            st.write("#### Key Components")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1. Projected Free Cash Flows**")
                st.write("""
                - Forecast period: Typically 5-10 years
                - Based on revenue growth, margins, CapEx, etc.
                - Cash available after reinvestment needs
                """)
                
                st.write("**2. Terminal Value**")
                st.write("""
                - Represents value beyond forecast period
                - Usually calculated using perpetuity growth or exit multiple
                - Significant portion of total value
                """)
            
            with col2:
                st.write("**3. Discount Rate (WACC)**")
                st.write("""
                - Weighted Average Cost of Capital
                - Reflects the riskiness of cash flows
                - Accounts for both debt and equity financing
                """)
                
                st.write("**4. Present Value Calculation**")
                st.write("""
                - Discounts all future cash flows to present
                - Accounts for the time value of money
                - Sum of PVs equals the enterprise value
                """)
            
            st.write("#### DCF Formula")
            
            st.latex(r'''
            \text{Enterprise Value} = \sum_{t=1}^{n} \frac{FCF_t}{(1+WACC)^t} + \frac{TV}{(1+WACC)^n}
            ''')
            
            st.write("""
            Where:
            - FCF_t = Free Cash Flow in year t
            - WACC = Weighted Average Cost of Capital
            - TV = Terminal Value
            - n = Forecast period (years)
            """)
            
            st.write("#### Terminal Value Calculation Methods")
            
            st.write("**1. Perpetuity Growth Method**")
            st.latex(r'''
            TV = \frac{FCF_{n+1}}{WACC - g} = \frac{FCF_n \times (1+g)}{WACC - g}
            ''')
            
            st.write("""
            Where:
            - FCF_n = Free Cash Flow in the final forecast year
            - g = Perpetual growth rate
            """)
            
            st.write("**2. Exit Multiple Method**")
            st.latex(r'''
            TV = \text{EBITDA}_n \times \text{EV/EBITDA multiple}
            ''')
            
            st.write("#### When to Use DCF")
            
            st.write("""
            DCF is most appropriate for:
            - Companies with predictable cash flows
            - Growing companies that aren't yet profitable
            - Companies where future performance will differ from the past
            - Businesses with significant expected changes (restructuring, new products)
            """)
            
            st.write("#### Limitations of DCF")
            
            st.write("""
            - Highly sensitive to assumptions (growth rate, discount rate, margins)
            - Terminal value often represents majority of the valuation
            - Difficulty forecasting cash flows for cyclical or volatile businesses
            - Not ideal for companies without clear path to positive cash flow
            """)
        
        elif method == "Comparable Company Analysis":
            st.write("### Comparable Company Analysis")
            
            st.write("""
            Comparable Company Analysis (or "Trading Comps") values a company based on how similar 
            public companies are valued in the market. This market-based approach uses valuation 
            multiples to determine a company's value relative to its peers.
            """)
            
            st.write("#### Key Components")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1. Peer Group Selection**")
                st.write("""
                - Companies in the same industry
                - Similar business models and markets
                - Comparable size, growth, and risk profile
                - Usually 5-10 relevant companies
                """)
                
                st.write("**2. Valuation Multiples**")
                st.write("""
                - EV/EBITDA: Enterprise Value to EBITDA
                - P/E: Price to Earnings
                - EV/Revenue: Enterprise Value to Revenue
                - P/B: Price to Book Value
                """)
            
            with col2:
                st.write("**3. Financial Metrics**")
                st.write("""
                - Current or forward-looking metrics
                - Adjusted for one-time items
                - Often use LTM (Last Twelve Months) or NTM (Next Twelve Months)
                """)
                
                st.write("**4. Valuation Range**")
                st.write("""
                - Apply peer multiples to company metrics
                - Consider premium/discount factors
                - Develop a valuation range rather than point estimate
                """)
            
            st.write("#### Valuation Process")
            
            st.write("""
            1. Identify comparable companies (peers)
            2. Gather financial data and calculate multiples for peers
            3. Analyze and adjust for outliers
            4. Apply appropriate multiples to the subject company's metrics
            5. Calculate implied valuation range
            """)
            
            st.write("#### Common Multiples")
            
            multiples_df = pd.DataFrame({
                'Multiple': ['EV/EBITDA', 'P/E', 'EV/Revenue', 'EV/EBIT', 'P/B', 'Dividend Yield'],
                'Description': [
                    'Enterprise Value / Earnings Before Interest, Taxes, Depreciation & Amortization',
                    'Price / Earnings',
                    'Enterprise Value / Revenue',
                    'Enterprise Value / Earnings Before Interest & Taxes',
                    'Price / Book Value',
                    'Annual Dividends / Share Price'
                ],
                'Best For': [
                    'Capital-intensive businesses, different capital structures',
                    'Profitable companies, financial institutions',
                    'Early-stage or high-growth companies',
                    'Companies with different depreciation policies',
                    'Financial institutions, asset-heavy companies',
                    'Mature companies with consistent dividends'
                ]
            })
            
            st.dataframe(multiples_df, use_container_width=True)
            
            st.write("#### When to Use Comparable Company Analysis")
            
            st.write("""
            Trading Comps is most appropriate for:
            - Companies with established peer groups
            - Industries where valuations follow consistent patterns
            - When market perception is a critical valuation factor
            - Supplementing other valuation methods
            """)
            
            st.write("#### Limitations")
            
            st.write("""
            - Difficulty finding truly comparable companies
            - Market inefficiencies and sentiment affecting peer valuations
            - Different accounting practices across companies
            - Doesn't account for company-specific factors
            - Assumes the market is correctly valuing peers
            """)
            
        elif method == "Precedent Transactions":
            st.write("### Precedent Transactions Analysis")
            
            st.write("""
            Precedent Transactions Analysis values a company based on the prices paid in 
            recent acquisitions of similar companies. This method incorporates control premiums 
            and synergies that are reflected in actual transaction prices.
            """)
            
            st.write("#### Key Components")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1. Transaction Selection**")
                st.write("""
                - Recent M&A deals in the same industry
                - Similar transaction size and structure
                - Strategic vs. financial buyers
                - Typically last 3-5 years of transactions
                """)
                
                st.write("**2. Transaction Multiples**")
                st.write("""
                - EV/EBITDA: Most common transaction multiple
                - EV/Revenue: Used for early-stage companies
                - EV/EBIT or P/E: Less common but still used
                - Industry-specific multiples
                """)
            
            with col2:
                st.write("**3. Premium Analysis**")
                st.write("""
                - Control premium paid over market value
                - Strategic vs. financial buyer premiums
                - Synergy expectations built into price
                """)
                
                st.write("**4. Deal Circumstances**")
                st.write("""
                - Competitive bidding vs. negotiated deals
                - Distressed sales vs. growth opportunities
                - Market conditions at time of transaction
                - Regulatory or other special considerations
                """)
            
            st.write("#### Valuation Process")
            
            st.write("""
            1. Identify relevant precedent transactions
            2. Gather transaction details and calculate multiples
            3. Adjust for market conditions and deal specifics
            4. Apply appropriate multiples to the subject company
            5. Calculate implied valuation range
            """)
            
            st.write("#### Example Transaction Multiples")
            
            transactions_df = pd.DataFrame({
                'Transaction': ['Company A acquires Company B', 'Company C acquires Company D', 'Company E acquires Company F'],
                'Date': ['Jan 2023', 'Mar 2022', 'Nov 2021'],
                'Value ($M)': [500, 1200, 800],
                'EV/EBITDA': ['10.5x', '12.2x', '8.7x'],
                'EV/Revenue': ['3.2x', '4.5x', '2.8x'],
                'Premium': ['25%', '35%', '18%']
            })
            
            st.dataframe(transactions_df, use_container_width=True)
            
            st.write("#### When to Use Precedent Transactions")
            
            st.write("""
            Precedent Transactions Analysis is most appropriate for:
            - M&A scenarios and change-of-control valuations
            - Industries with frequent, documented transactions
            - When analyzing potential acquisition premiums
            - Companies considering strategic alternatives
            """)
            
            st.write("#### Limitations")
            
            st.write("""
            - Limited availability of transaction data
            - Unique synergies and circumstances for each deal
            - Changing market conditions between transactions
            - Difficulty adjusting for different transaction structures
            - Older transactions may have limited relevance
            """)
            
        elif method == "Asset-Based Valuation":
            st.write("### Asset-Based Valuation")
            
            st.write("""
            Asset-Based Valuation determines a company's value by assessing the fair market value 
            of its assets minus its liabilities. This approach focuses on the company's balance sheet 
            rather than its earnings or cash flow potential.
            """)
            
            st.write("#### Key Components")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1. Asset Valuation**")
                st.write("""
                - Current assets (cash, inventory, receivables)
                - Fixed assets (property, plant, equipment)
                - Intangible assets (IP, goodwill, brand value)
                - Off-balance sheet assets
                """)
                
                st.write("**2. Liability Assessment**")
                st.write("""
                - Current liabilities
                - Long-term debt
                - Contingent liabilities
                - Off-balance sheet obligations
                """)
            
            with col2:
                st.write("**3. Adjustments**")
                st.write("""
                - Market value vs. book value adjustments
                - Obsolescence or impairment
                - Undervalued assets (real estate, IP)
                - Hidden liabilities
                """)
                
                st.write("**4. Net Asset Value**")
                st.write("""
                - Adjusted assets minus adjusted liabilities
                - Book value vs. liquidation value
                - Going concern vs. liquidation scenarios
                """)
            
            st.write("#### Approaches to Asset-Based Valuation")
            
            st.write("**1. Book Value Method**")
            st.write("""
            Uses the book value of assets and liabilities as reported on the balance sheet. 
            Simple but often understates real economic value.
            
            Book Value = Total Assets - Total Liabilities
            """)
            
            st.write("**2. Adjusted Book Value Method**")
            st.write("""
            Adjusts the book value of assets and liabilities to reflect current market values.
            More accurate but requires detailed analysis.
            
            Adjusted Book Value = Adjusted Market Value of Assets - Adjusted Market Value of Liabilities
            """)
            
            st.write("**3. Liquidation Value Method**")
            st.write("""
            Estimates the net cash that would be realized if all assets were sold and liabilities settled.
            Usually represents the floor value of a business.
            
            Liquidation Value = Distressed Sale Value of Assets - Liabilities - Liquidation Costs
            """)
            
            st.write("**4. Replacement Value Method**")
            st.write("""
            Estimates the cost to recreate the company by purchasing or building all of its assets new.
            
            Replacement Value = Current Cost to Replace All Assets - Liabilities
            """)
            
            st.write("#### When to Use Asset-Based Valuation")
            
            st.write("""
            Asset-Based Valuation is most appropriate for:
            - Asset-intensive businesses (real estate, manufacturing)
            - Holding companies and investment firms
            - Companies with significant tangible assets
            - Distressed businesses or liquidation scenarios
            - Companies with minimal or negative earnings
            """)
            
            st.write("#### Limitations")
            
            st.write("""
            - Difficulty valuing intangible assets
            - May undervalue going-concern value
            - Ignores future earnings potential
            - Labor-intensive to properly adjust values
            - Not suitable for service businesses or asset-light companies
            """)
            
        elif method == "LBO Analysis":
            st.write("### Leveraged Buyout (LBO) Analysis")
            
            st.write("""
            Leveraged Buyout (LBO) Analysis models the acquisition of a company using a significant 
            amount of debt. This method focuses on the potential return to equity investors based on 
            financial engineering, operational improvements, and exit strategies.
            """)
            
            st.write("#### Key Components")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1. Capital Structure**")
                st.write("""
                - Purchase price allocation
                - Debt/equity ratio (typically 60-80% debt)
                - Types of debt (senior, subordinated, mezzanine)
                - Equity contribution
                """)
                
                st.write("**2. Operational Projections**")
                st.write("""
                - Revenue and EBITDA growth
                - Margin improvements
                - Working capital optimization
                - Capital expenditure requirements
                """)
            
            with col2:
                st.write("**3. Debt Service**")
                st.write("""
                - Interest payments
                - Principal amortization
                - Debt covenants and requirements
                - Refinancing options
                """)
                
                st.write("**4. Exit Strategy**")
                st.write("""
                - Holding period (typically 3-7 years)
                - Exit multiples
                - Exit methods (IPO, strategic sale, secondary LBO)
                - Returns calculation (IRR, MoM)
                """)
            
            st.write("#### LBO Process")
            
            st.write("""
            1. Identify a target company with stable cash flows and growth potential
            2. Determine maximum purchase price based on target returns
            3. Structure the financing (debt and equity components)
            4. Project financial performance over holding period
            5. Model debt repayment schedule
            6. Calculate exit value and investor returns
            """)
            
            st.write("#### Key Return Metrics")
            
            st.write("**Internal Rate of Return (IRR)**")
            st.latex(r'''
            \sum_{t=0}^{n} \frac{CF_t}{(1+IRR)^t} = 0
            ''')
            
            st.write("""
            Where:
            - CF_t = Cash flow at time t (negative for investments, positive for returns)
            - n = Holding period
            """)
            
            st.write("**Multiple of Money (MoM)**")
            st.latex(r'''
            MoM = \frac{\text{Exit Equity Value}}{\text{Initial Equity Investment}}
            ''')
            
            st.write("#### LBO Candidates")
            
            lbo_candidates_df = pd.DataFrame({
                'Characteristic': [
                    'Stable and predictable cash flows',
                    'Low existing debt levels',
                    'Strong market position',
                    'Asset base for collateral',
                    'Cost-cutting opportunities',
                    'Non-core divisions of larger companies',
                    'Low capital expenditure requirements',
                    'Strong management team'
                ],
                'Importance': [
                    'Critical for debt service',
                    'Provides room for new debt',
                    'Supports operational stability',
                    'Secures financing',
                    'Path to value creation',
                    'Often undervalued',
                    'Maximizes free cash flow',
                    'Essential for executing strategy'
                ]
            })
            
            st.dataframe(lbo_candidates_df, use_container_width=True)
            
            st.write("#### When to Use LBO Analysis")
            
            st.write("""
            LBO Analysis is most appropriate for:
            - Private equity valuations and acquisitions
            - Companies with strong, stable cash flows
            - Businesses with significant debt capacity
            - Companies with improvement opportunities
            - When assessing maximum affordable purchase price
            """)
            
            st.write("#### Limitations")
            
            st.write("""
            - Highly sensitive to exit multiple assumptions
            - Risk of overleveraging the business
            - Vulnerable to economic downturns
            - Limited applicability to high-growth or capital-intensive businesses
            - Relies heavily on debt availability and terms
            """)
    
    with tab2:
        st.subheader("Key Financial Concepts")
        
        concept = st.selectbox(
            "Select a concept to learn about",
            ["WACC (Weighted Average Cost of Capital)", "EBITDA", "Enterprise Value vs. Equity Value", 
             "Terminal Value", "Valuation Multiples", "Beta and Risk", "Perpetual Growth Rate"]
        )
        
        if concept == "WACC (Weighted Average Cost of Capital)":
            st.write("### WACC (Weighted Average Cost of Capital)")
            
            st.write("""
            The Weighted Average Cost of Capital (WACC) represents the average rate of return a company 
            must pay to its investors (both debt and equity) to finance its assets. It's used as the discount 
            rate in DCF valuations to reflect the riskiness of the company's cash flows.
            """)
            
            st.write("#### WACC Formula")
            
            st.latex(r'''
            WACC = \left(\frac{E}{V} \times R_e\right) + \left(\frac{D}{V} \times R_d \times (1-T_c)\right)
            ''')
            
            st.write("""
            Where:
            - E = Market value of equity
            - D = Market value of debt
            - V = Total market value (E + D)
            - Re = Cost of equity
            - Rd = Cost of debt
            - Tc = Corporate tax rate
            """)
            
            st.write("#### Components of WACC")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Cost of Equity (Re)**")
                st.write("""
                Typically calculated using the Capital Asset Pricing Model (CAPM):
                """)
                
                st.latex(r'''
                R_e = R_f + \beta \times (R_m - R_f)
                ''')
                
                st.write("""
                Where:
                - Rf = Risk-free rate (typically 10-year Treasury yield)
                - β = Beta (measure of stock volatility relative to the market)
                - Rm = Expected market return
                - (Rm - Rf) = Market risk premium
                """)
            
            with col2:
                st.write("**Cost of Debt (Rd)**")
                st.write("""
                The effective interest rate the company pays on its debt, adjusted for tax benefits since 
                interest is tax-deductible:
                """)
                
                st.latex(r'''
                R_d \times (1 - T_c)
                ''')
                
                st.write("""
                Where:
                - Rd = Pre-tax cost of debt (yield to maturity on long-term debt)
                - Tc = Corporate tax rate
                """)
            
            st.write("#### Typical WACC by Industry")
            
            wacc_df = pd.DataFrame({
                'Industry': ['Technology', 'Healthcare', 'Financial Services', 'Utilities', 'Consumer Goods', 'Energy'],
                'Typical WACC Range': ['8-12%', '7-10%', '8-11%', '4-8%', '7-9%', '9-13%'],
                'Key Factors': [
                    'Higher equity proportion, higher beta',
                    'Stable cash flows, moderate beta',
                    'Highly leveraged, regulated',
                    'Low risk, high debt, regulated',
                    'Stable demand, moderate beta',
                    'Commodity price exposure, high capex'
                ]
            })
            
            st.dataframe(wacc_df, use_container_width=True)
            
            st.write("#### WACC Considerations")
            
            st.write("""
            - **Company-Specific Factors**: Size, financial health, and growth stage affect WACC
            - **Capital Structure**: Changes in debt/equity ratio impact WACC
            - **Market Conditions**: Interest rates and market risk premiums fluctuate
            - **Geographic Factors**: Country risk premiums for international operations
            - **Industry Dynamics**: Competitive landscape and industry disruption
            """)
            
        elif concept == "EBITDA":
            st.write("### EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization)")
            
            st.write("""
            EBITDA is a measure of a company's operating performance that excludes financing decisions (interest), 
            tax environments (taxes), and non-cash expenses (depreciation and amortization). It's widely used in 
            valuations as a proxy for operating cash flow and for comparing companies with different capital structures.
            """)
            
            st.write("#### EBITDA Calculation")
            
            st.write("**Starting from Net Income:**")
            st.write("""
            EBITDA = Net Income + Interest + Taxes + Depreciation + Amortization
            """)
            
            st.write("**Starting from Operating Income (EBIT):**")
            st.write("""
            EBITDA = Operating Income (EBIT) + Depreciation + Amortization
            """)
            
            st.write("**Starting from Revenue:**")
            st.write("""
            EBITDA = Revenue - Operating Expenses (excluding D&A)
            """)
            
            st.write("#### Why EBITDA Matters in Valuation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Advantages of EBITDA**")
                st.write("""
                - Eliminates effects of financing and accounting decisions
                - Allows easier comparison between companies
                - Approximates operating cash flow
                - Used in many valuation multiples (EV/EBITDA)
                - Popular in M&A and private equity
                """)
            
            with col2:
                st.write("**Limitations of EBITDA**")
                st.write("""
                - Ignores capital expenditure requirements
                - Doesn't account for working capital needs
                - Not a GAAP metric
                - Can mask underlying profitability issues
                - May overstate true cash flow
                """)
            
            st.write("#### EBITDA Adjustments")
            
            st.write("""
            When using EBITDA for valuation, analysts often make adjustments to normalize for one-time 
            or non-recurring items:
            """)
            
            adjustments_df = pd.DataFrame({
                'Adjustment Type': [
                    'One-time expenses/income',
                    'Owner compensation',
                    'Rent adjustments',
                    'Litigation expenses',
                    'Restructuring costs',
                    'Non-recurring professional fees',
                    'Inventory write-downs',
                    'R&D expenses',
                    'Stock-based compensation'
                ],
                'Treatment': [
                    'Remove non-recurring items',
                    'Normalize to market rates',
                    'Adjust to market rates for owned property',
                    'Remove if non-recurring',
                    'Remove if one-time event',
                    'Remove transaction-related fees',
                    'Remove one-time write-downs',
                    'Consider capitalizing portion',
                    'Add back non-cash expense'
                ]
            })
            
            st.dataframe(adjustments_df, use_container_width=True)
            
            st.write("#### EBITDA Margins by Industry")
            
            margin_df = pd.DataFrame({
                'Industry': ['Technology (Software)', 'Healthcare', 'Retail', 'Manufacturing', 'Utilities', 'Telecom'],
                'Typical EBITDA Margin': ['20-30%', '15-25%', '5-10%', '10-20%', '30-40%', '35-45%'],
                'Notes': [
                    'High margins due to scalability',
                    'Varies by subsector (pharma higher)',
                    'Thin margins, high volume',
                    'Varies by product complexity',
                    'Steady regulated returns',
                    'High fixed costs, infrastructure'
                ]
            })
            
            st.dataframe(margin_df, use_container_width=True)
            
        elif concept == "Enterprise Value vs. Equity Value":
            st.write("### Enterprise Value vs. Equity Value")
            
            st.write("""
            Understanding the difference between Enterprise Value and Equity Value is crucial for proper 
            company valuation. These concepts represent different perspectives on a company's value and 
            are used in different contexts and valuation multiples.
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Enterprise Value (EV)")
                
                st.write("""
                Enterprise Value represents the total value of a company, including debt and equity capital. 
                It's essentially the theoretical takeover price if a company were to be acquired.
                """)
                
                st.write("**Formula:**")
                st.write("""
                Enterprise Value = Market Capitalization + Total Debt + Preferred Stock + Minority Interest - Cash and Equivalents
                """)
                
                st.write("**Key Points:**")
                st.write("""
                - Represents the value of the entire business
                - Independent of capital structure
                - Used with operating metrics (Revenue, EBITDA, EBIT)
                - Includes all investor claims on the business
                - Appropriate for comparing companies with different debt levels
                """)
            
            with col2:
                st.write("#### Equity Value")
                
                st.write("""
                Equity Value represents the value available to equity shareholders. It's the market value 
                of all outstanding shares of a company.
                """)
                
                st.write("**Formula:**")
                st.write("""
                Equity Value = Share Price × Number of Shares Outstanding
                """)
                
                st.write("**Alternative Calculation:**")
                st.write("""
                Equity Value = Enterprise Value - Total Debt - Preferred Stock - Minority Interest + Cash and Equivalents
                """)
                
                st.write("**Key Points:**")
                st.write("""
                - Represents value available to shareholders only
                - Depends on capital structure
                - Used with equity metrics (Net Income, EPS, Dividends)
                - Excludes debt and other non-equity claims
                - Directly affected by cash and debt levels
                """)
            
            st.write("#### Bridge Between EV and Equity Value")
            
            st.write("""
            The relationship between Enterprise Value and Equity Value can be visualized as a bridge:
            """)
            
            bridge_data = [
                {"Component": "Market Capitalization (Equity Value)", "Value": 1000},
                {"Component": "Plus: Total Debt", "Value": 500},
                {"Component": "Plus: Preferred Stock", "Value": 100},
                {"Component": "Plus: Minority Interest", "Value": 50},
                {"Component": "Minus: Cash and Equivalents", "Value": -200},
                {"Component": "Enterprise Value", "Value": 1450}
            ]
            
            bridge_df = pd.DataFrame(bridge_data)
            
            # Format values as millions
            bridge_df['Value'] = bridge_df['Value'].apply(lambda x: f"${x}M")
            
            st.dataframe(bridge_df, use_container_width=True)
            
            st.write("#### Appropriate Valuation Multiples")
            
            multiples_df = pd.DataFrame({
                'Enterprise Value Multiples': ['EV/Revenue', 'EV/EBITDA', 'EV/EBIT', 'EV/FCF'],
                'Equity Value Multiples': ['P/E', 'P/B', 'Dividend Yield', 'P/FCF to Equity']
            })
            
            st.dataframe(multiples_df, use_container_width=True)
            
            st.write("#### Common Mistakes to Avoid")
            
            st.write("""
            - Using EV multiples with equity metrics (e.g., EV/Net Income)
            - Using equity multiples with operating metrics (e.g., P/EBITDA)
            - Forgetting to subtract cash when converting from EV to equity value
            - Not adjusting for off-balance sheet items in EV calculation
            - Mismatching time periods between value and metrics
            """)
            
        elif concept == "Terminal Value":
            st.write("### Terminal Value")
            
            st.write("""
            Terminal Value represents the value of a business beyond the explicit forecast period in a 
            Discounted Cash Flow (DCF) model. It typically accounts for the majority of the total enterprise 
            value, often 60-80% or more, making it a critical component of the valuation.
            """)
            
            st.write("#### Why Terminal Value Matters")
            
            st.write("""
            Since businesses are assumed to operate indefinitely, but we can only reasonably forecast 
            cash flows for a limited period (typically 5-10 years), the terminal value captures all 
            value created after the forecast period. This makes it both:
            - Essential for realistic valuations
            - A potential source of significant valuation error if miscalculated
            """)
            
            st.write("#### Terminal Value Calculation Methods")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**1. Perpetuity Growth Method**")
                
                st.latex(r'''
                TV = \frac{FCF_{n+1}}{WACC - g} = \frac{FCF_n \times (1+g)}{WACC - g}
                ''')
                
                st.write("""
                Where:
                - FCF_n = Free Cash Flow in the final forecast year
                - g = Perpetual growth rate
                - WACC = Weighted Average Cost of Capital
                """)
                
                st.write("**Key Considerations:**")
                st.write("""
                - Perpetual growth rate should not exceed long-term GDP growth
                - Typical range: 1-3% for mature markets
                - Highly sensitive to small changes in growth rate
                - Based on Gordon Growth Model
                """)
            
            with col2:
                st.write("**2. Exit Multiple Method**")
                
                st.latex(r'''
                TV = \text{EBITDA}_n \times \text{EV/EBITDA multiple}
                ''')
                
                st.write("""
                Where:
                - EBITDA_n = EBITDA in the final forecast year
                - EV/EBITDA multiple = Appropriate industry multiple
                """)
                
                st.write("**Key Considerations:**")
                st.write("""
                - Multiple should reflect expected future industry conditions
                - Often based on current trading multiples of comparable companies
                - Can also use other multiples (EV/EBIT, EV/Revenue)
                - Market-based rather than theoretical
                """)
            
            st.write("#### Sensitivity of Terminal Value")
            
            st.write("""
            Small changes in terminal value assumptions can dramatically impact the overall valuation. Consider 
            this sensitivity table showing the impact of different growth rates and discount rates on terminal value:
            """)
            
            # Create example sensitivity table
            wacc_values = [0.08, 0.10, 0.12, 0.14]
            growth_values = [0.01, 0.02, 0.03, 0.04]
            
            sensitivity_data = []
            
            for wacc in wacc_values:
                row = []
                for g in growth_values:
                    # Terminal value multiple formula
                    tv_multiple = 1 / (wacc - g)
                    row.append(f"{tv_multiple:.1f}x")
                sensitivity_data.append(row)
            
            sensitivity_df = pd.DataFrame(
                sensitivity_data,
                columns=[f"g = {g*100:.0f}%" for g in growth_values],
                index=[f"WACC = {wacc*100:.0f}%" for wacc in wacc_values]
            )
            
            st.dataframe(sensitivity_df, use_container_width=True)
            
            st.write("#### Terminal Value Best Practices")
            
            st.write("""
            1. **Use Both Methods**: Calculate terminal value using both perpetuity growth and exit multiple methods as a cross-check
            
            2. **Realistic Assumptions**: Ensure terminal growth rate is sustainable (usually below 3%)
            
            3. **Consistency Check**: Terminal value should imply reasonable multiples compared to industry norms
            
            4. **Scenario Analysis**: Test different terminal value assumptions
            
            5. **Terminal Year Normalization**: Ensure the final projection year represents "normalized" operations
            
            6. **Fade Period**: Consider a fade period to transition from high growth to terminal growth
            
            7. **Long-Term Margins**: Ensure terminal year margins are sustainable long-term
            """)
            
        elif concept == "Valuation Multiples":
            st.write("### Valuation Multiples")
            
            st.write("""
            Valuation multiples are ratios that relate a company's value or share price to a key metric 
            like earnings, sales, or book value. They provide a standardized way to compare different 
            companies and are widely used in relative valuation methods.
            """)
            
            st.write("#### Types of Valuation Multiples")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Enterprise Value Multiples**")
                st.write("""
                Relate the total value of the business (debt + equity - cash) to operating metrics:
                
                - EV/EBITDA
                - EV/EBIT
                - EV/Revenue
                - EV/Installed Capacity
                - EV/Subscribers
                """)
                
                st.write("**Key Advantage:**")
                st.write("Capital structure-neutral - allows comparison of companies with different debt levels")
            
            with col2:
                st.write("**Equity Multiples**")
                st.write("""
                Relate the market capitalization to equity-focused metrics:
                
                - P/E (Price-to-Earnings)
                - P/B (Price-to-Book)
                - P/S (Price-to-Sales)
                - P/FCF (Price-to-Free Cash Flow)
                - Dividend Yield
                """)
                
                st.write("**Key Advantage:**")
                st.write("Directly relate to shareholder returns and often easier to calculate")
            
            st.write("#### Most Common Multiples by Industry")
            
            industry_multiples_df = pd.DataFrame({
                'Industry': ['Technology', 'Consumer Retail', 'Manufacturing', 'Financial Services', 'Healthcare', 'Utilities'],
                'Primary Multiples': ['EV/Revenue, P/E', 'EV/EBITDA, P/E', 'EV/EBITDA, P/E', 'P/B, P/E', 'EV/EBITDA, P/E', 'EV/EBITDA, Dividend Yield'],
                'Secondary Multiples': ['EV/User, EV/R&D', 'EV/Sales, P/S', 'EV/EBIT, P/FCF', 'P/TBV, ROE', 'EV/Revenue, P/E', 'EV/Customer, Reg. Asset Base']
            })
            
            st.dataframe(industry_multiples_df, use_container_width=True)
            
            st.write("#### Interpreting Multiples")
            
            st.write("""
            **Higher Multiples May Indicate:**
            - Higher expected growth
            - Lower risk
            - Stronger competitive position
            - Superior management
            - Industry expansion phase
            - More efficient operations
            
            **Lower Multiples May Indicate:**
            - Lower expected growth
            - Higher risk
            - Weaker competitive position
            - Industry contraction phase
            - Less efficient operations
            - Potential undervaluation
            """)
            
            st.write("#### Factors Affecting Multiples")
            
            factors_df = pd.DataFrame({
                'Factor': [
                    'Growth Rate',
                    'Profit Margins',
                    'Return on Invested Capital',
                    'Risk Profile',
                    'Capital Intensity',
                    'Tax Rate',
                    'Industry Life Cycle'
                ],
                'Impact on Multiples': [
                    'Higher growth typically justifies higher multiples',
                    'Higher margins generally lead to higher multiples',
                    'Higher ROIC typically commands premium multiples',
                    'Lower risk (beta) generally leads to higher multiples',
                    'Lower capital needs often yield higher multiples',
                    'Lower effective tax rates can support higher multiples',
                    'Growth industries typically have higher multiples'
                ]
            })
            
            st.dataframe(factors_df, use_container_width=True)
            
            st.write("#### Advanced Multiple Concepts")
            
            st.write("**Forward vs. Trailing Multiples**")
            st.write("""
            - **Trailing Multiples**: Based on historical performance (last 12 months)
            - **Forward Multiples**: Based on projected future performance (next 12 months)
            - Forward multiples are generally considered more relevant but less reliable
            """)
            
            st.write("**Adjusted Multiples**")
            st.write("""
            - EV/EBITDA-CapEx: Accounts for capital intensity
            - PEG Ratio (P/E to Growth): Adjusts P/E for growth rate
            - EV/EBITDA adjusted for R&D: Treats R&D as capex rather than expense
            """)
            
            st.write("**Cyclical Adjustments**")
            st.write("""
            - Normalized earnings over business cycle
            - Mid-cycle multiples
            - Through-the-cycle average EBITDA
            """)
            
        elif concept == "Beta and Risk":
            st.write("### Beta and Risk")
            
            st.write("""
            Beta is a measure of a stock's volatility in relation to the overall market. It plays a critical role 
            in the Capital Asset Pricing Model (CAPM) and the calculation of cost of equity, which directly 
            impacts company valuations through the discount rate used.
            """)
            
            st.write("#### Understanding Beta")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Beta Interpretation:**")
                st.write("""
                - β = 1.0: Stock moves with the market
                - β > 1.0: Stock is more volatile than the market
                - β < 1.0: Stock is less volatile than the market
                - β = 0: Stock moves independently of the market
                - β < 0: Stock moves opposite to the market (rare)
                """)
                
                st.write("**Typical Beta Values by Sector:**")
                beta_df = pd.DataFrame({
                    'Sector': ['Utilities', 'Consumer Staples', 'Healthcare', 'Financial Services', 'Technology', 'Energy'],
                    'Typical Beta Range': ['0.3-0.7', '0.5-0.8', '0.7-1.0', '1.0-1.5', '1.2-1.8', '1.3-1.7']
                })
                
                st.dataframe(beta_df, use_container_width=True)
            
            with col2:
                st.write("**Calculating Beta:**")
                st.latex(r'''
                \beta = \frac{Cov(r_i, r_m)}{Var(r_m)}
                ''')
                
                st.write("""
                Where:
                - r_i = Return of the security
                - r_m = Return of the market
                - Cov = Covariance
                - Var = Variance
                """)
                
                st.write("**Beta in the CAPM Formula:**")
                st.latex(r'''
                r_i = r_f + \beta_i (r_m - r_f)
                ''')
                
                st.write("""
                Where:
                - r_i = Expected return on the security
                - r_f = Risk-free rate
                - r_m = Expected market return
                - (r_m - r_f) = Market risk premium
                """)
            
            st.write("#### Types of Beta")
            
            st.write("**1. Historical Beta**")
            st.write("""
            Calculated from historical price movements, typically over a 2-5 year period with 
            weekly or monthly observations.
            
            **Limitations:**
            - May not reflect current company structure or strategy
            - Subject to market anomalies during the measurement period
            - Backward-looking rather than forward-looking
            """)
            
            st.write("**2. Adjusted Beta**")
            st.write("""
            Assumes beta tends to move toward the market average (1.0) over time:
            
            Adjusted Beta = (2/3 × Historical Beta) + (1/3 × 1.0)
            
            **Benefits:**
            - Accounts for mean reversion tendencies
            - Used by services like Bloomberg and Merrill Lynch
            """)
            
            st.write("**3. Fundamental Beta**")
            st.write("""
            Derived from company fundamentals rather than stock price movements:
            - Operating leverage (fixed vs. variable costs)
            - Financial leverage (debt vs. equity)
            - Cyclicality of revenues
            - Size and diversification
            
            **Benefits:**
            - Can be applied to private companies
            - Forward-looking rather than historical
            """)
            
            st.write("#### Adjusting Beta for Valuation")
            
            st.write("**For Unlevered (Asset) Beta:**")
            st.latex(r'''
            \beta_{unlevered} = \frac{\beta_{levered}}{1 + (1 - t) \times \frac{D}{E}}
            ''')
            
            st.write("""
            Where:
            - t = Tax rate
            - D/E = Debt-to-Equity ratio
            """)
            
            st.write("**For Relevered Beta:**")
            st.latex(r'''
            \beta_{relevered} = \beta_{unlevered} \times [1 + (1 - t) \times \frac{D_{target}}{E_{target}}]
            ''')
            
            st.write("#### Beta in Private Company Valuation")
            
            st.write("""
            For private companies without observable betas:
            
            1. **Pure-play Method**: Use beta from comparable public companies
            2. **Industry Average**: Use average beta from the industry
            3. **Bottom-up Beta**: Build beta from fundamental risk factors
            4. **Accounting Beta**: Correlate accounting returns with market returns
            """)
            
            st.write("#### Risk Considerations Beyond Beta")
            
            st.write("""
            Beta only captures systematic (market) risk. Other risk factors to consider:
            
            - **Size Premium**: Smaller companies typically have higher required returns
            - **Company-Specific Risk**: Unsystematic risks unique to the company
            - **Country Risk Premium**: Added premium for emerging or unstable markets
            - **Illiquidity Discount**: Premium for lack of marketability
            - **Control Premium/Discount**: Adjustments for controlling or minority stakes
            """)
            
        elif concept == "Perpetual Growth Rate":
            st.write("### Perpetual Growth Rate")
            
            st.write("""
            The perpetual growth rate is a critical assumption in DCF valuation models that represents 
            the expected growth rate of a company's cash flows in perpetuity after the explicit forecast 
            period. This rate is used in calculating the terminal value, which often accounts for the 
            majority of a company's overall valuation.
            """)
            
            st.write("#### Importance in Valuation")
            
            st.write("""
            The perpetual growth rate is one of the most sensitive assumptions in a DCF model:
            - Small changes can have significant impacts on valuation
            - Generally represents the company's sustainable long-term growth
            - Must be lower than the discount rate to avoid infinite value
            - Should be consistent with long-term macroeconomic expectations
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Theoretical Limits")
                
                st.write("""
                A company cannot grow faster than the economy indefinitely:
                
                - **Maximum Limit**: Long-term GDP growth + inflation
                - **Typical Range**: 1% to 3% in developed economies
                - **Zero or Negative Growth**: Possible for declining industries
                - **Minimum Practical Limit**: Usually not below -1% or -2%
                """)
                
                st.write("**Impact on Terminal Value:**")
                
                st.latex(r'''
                TV = \frac{FCF_n \times (1+g)}{WACC - g}
                ''')
                
                st.write("As g approaches WACC, terminal value approaches infinity")
            
            with col2:
                st.write("#### Factors Affecting Perpetual Growth Rate")
                
                st.write("""
                **Macroeconomic Factors:**
                - Long-term GDP growth expectations
                - Industry growth prospects
                - Inflation expectations
                - Population growth
                
                **Company-Specific Factors:**
                - Competitive advantages and their sustainability
                - Market share trends
                - Product life cycle positioning
                - Industry maturity
                - Regulatory environment
                """)
            
            st.write("#### Growth Rate Benchmarks")
            
            growth_df = pd.DataFrame({
                'Benchmark': [
                    'US Long-term GDP Growth',
                    'Developed Markets GDP Growth',
                    'Emerging Markets GDP Growth',
                    'Global Inflation Rate',
                    'Mature Industries',
                    'Growth Industries',
                    'Declining Industries'
                ],
                'Typical Rate': [
                    '2.0-2.5%',
                    '1.5-2.5%',
                    '3.0-5.0%',
                    '2.0-3.0%',
                    '0-2%',
                    '2-4%',
                    '-2-0%'
                ],
                'Notes': [
                    'Real growth + inflation',
                    'Lower than historical averages',
                    'Higher growth but higher risk',
                    'Central bank targets typically ~2%',
                    'Consumer staples, utilities, basic materials',
                    'Technology, healthcare, renewable energy',
                    'Traditional retail, print media, coal'
                ]
            })
            
            st.dataframe(growth_df, use_container_width=True)
            
            st.write("#### Common Mistakes with Perpetual Growth Rates")
            
            st.write("""
            1. **Using Unrealistic Growth Rates**: Growth rates exceeding long-term economic growth
            
            2. **Inconsistency with Terminal Year**: Terminal year should represent a normalized state
            
            3. **Ignoring Reinvestment Requirements**: Higher growth requires higher reinvestment
            
            4. **Not Adjusting for Industry Life Cycle**: Mature or declining industries should have lower growth
            
            5. **Mismatching Currency/Inflation**: Nominal growth rate should include inflation
            
            6. **Forgetting Competitive Forces**: Perfect competition erodes excess returns over time
            """)
            
            st.write("#### Best Practices")
            
            st.write("""
            - **Multiple Scenarios**: Use several perpetual growth assumptions
            - **Sensitivity Analysis**: Test how value changes with different growth rates
            - **Cross-Check**: Implied terminal multiples should be reasonable
            - **Fade Period**: Consider a transition period to sustainable growth
            - **Segmentation**: Different growth rates for different business segments
            - **Consistency**: Ensure consistency with capital investment assumptions
            """)
    
    with tab3:
        st.subheader("Valuation Quizzes")
        
        quiz_type = st.selectbox(
            "Select a quiz to take",
            ["DCF Fundamentals", "Valuation Multiples", "Financial Statement Analysis", "Advanced Valuation Concepts"]
        )
        
        if quiz_type == "DCF Fundamentals":
            st.write("### DCF Fundamentals Quiz")
            
            with st.form("dcf_quiz"):
                st.write("Test your knowledge of Discounted Cash Flow valuation.")
                
                q1 = st.radio(
                    "1. What does DCF stand for?",
                    ["Direct Cash Flow", "Discounted Cash Flow", "Declining Cash Flow", "Dividend Cash Flow"]
                )
                
                q2 = st.radio(
                    "2. In a DCF model, what does the discount rate represent?",
                    ["The growth rate of the company", 
                     "The weighted average cost of capital (WACC)", 
                     "The inflation rate", 
                     "The tax rate"]
                )
                
                q3 = st.radio(
                    "3. What percentage of a typical DCF valuation comes from the terminal value?",
                    ["10-20%", "30-40%", "50-60%", "60-80%"]
                )
                
                q4 = st.radio(
                    "4. What happens to the valuation if the perpetual growth rate increases?",
                    ["Valuation decreases", 
                     "Valuation increases", 
                     "Valuation stays the same", 
                     "Effect depends on the industry"]
                )
                
                q5 = st.radio(
                    "5. Which of the following is NOT typically included in a DCF model?",
                    ["Free cash flow projections", 
                     "Terminal value calculation", 
                     "Stock price history", 
                     "Discount rate (WACC)"]
                )
                
                submitted = st.form_submit_button("Submit Answers")
                
                if submitted:
                    score = 0
                    if q1 == "Discounted Cash Flow":
                        score += 1
                    if q2 == "The weighted average cost of capital (WACC)":
                        score += 1
                    if q3 == "60-80%":
                        score += 1
                    if q4 == "Valuation increases":
                        score += 1
                    if q5 == "Stock price history":
                        score += 1
                    
                    st.success(f"You scored {score}/5!")
                    
                    if score == 5:
                        st.balloons()
                        st.write("Perfect score! You're a DCF expert!")
                    elif score >= 3:
                        st.write("Good job! You have a solid understanding of DCF fundamentals.")
                    else:
                        st.write("Keep learning! Check out our DCF lesson for more information.")
        
        elif quiz_type == "Valuation Multiples":
            st.write("### Valuation Multiples Quiz")
            
            with st.form("multiples_quiz"):
                st.write("Test your knowledge of valuation multiples.")
                
                q1 = st.radio(
                    "1. Which of the following is an enterprise value multiple?",
                    ["P/E", "EV/EBITDA", "P/B", "Dividend Yield"]
                )
                
                q2 = st.radio(
                    "2. If a company has a P/E ratio of 20, what does this mean?",
                    ["The company is worth 20 times its book value", 
                     "Investors are paying $20 for every $1 of earnings", 
                     "The company has a 20% profit margin", 
                     "The company will return your investment in 20 years"]
                )
                
                q3 = st.radio(
                    "3. Which industry typically has the highest EV/EBITDA multiples?",
                    ["Utilities", "Technology", "Banking", "Basic Materials"]
                )
                
                q4 = st.radio(
                    "4. What does a low EV/EBITDA multiple potentially indicate?",
                    ["High growth expectations", 
                     "Potential undervaluation or business challenges", 
                     "High dividend yield", 
                     "Strong competitive position"]
                )
                
                q5 = st.radio(
                    "5. Which multiple would be most appropriate for valuing a pre-profit tech company?",
                    ["P/E", "EV/EBITDA", "EV/Revenue", "P/B"]
                )
                
                submitted = st.form_submit_button("Submit Answers")
                
                if submitted:
                    score = 0
                    if q1 == "EV/EBITDA":
                        score += 1
                    if q2 == "Investors are paying $20 for every $1 of earnings":
                        score += 1
                    if q3 == "Technology":
                        score += 1
                    if q4 == "Potential undervaluation or business challenges":
                        score += 1
                    if q5 == "EV/Revenue":
                        score += 1
                    
                    st.success(f"You scored {score}/5!")
                    
                    if score == 5:
                        st.balloons()
                        st.write("Perfect score! You're a valuation multiples expert!")
                    elif score >= 3:
                        st.write("Good job! You have a solid understanding of valuation multiples.")
                    else:
                        st.write("Keep learning! Check out our Valuation Multiples lesson for more information.")
        
        elif quiz_type == "Financial Statement Analysis":
            st.write("### Financial Statement Analysis Quiz")
            
            with st.form("financial_quiz"):
                st.write("Test your knowledge of financial statement analysis for valuation.")
                
                q1 = st.radio(
                    "1. Which financial statement is most useful for calculating free cash flow?",
                    ["Income Statement", "Balance Sheet", "Cash Flow Statement", "Statement of Shareholders' Equity"]
                )
                
                q2 = st.radio(
                    "2. EBITDA stands for:",
                    ["Earnings Before Interest, Tax, Depreciation, and Amortization", 
                     "Earnings Before Income Tax, Dividends, and Adjustments", 
                     "Effective Business Income Tax and Depreciation Allowance", 
                     "Equity-Based Income, Tax, Dividends, and Assets"]
                )
                
                q3 = st.radio(
                    "3. Which of the following is NOT a component of working capital?",
                    ["Accounts Receivable", "Inventory", "Long-term Debt", "Accounts Payable"]
                )
                
                q4 = st.radio(
                    "4. What is the formula for calculating Free Cash Flow?",
                    ["Net Income + Depreciation - Changes in Working Capital - CapEx", 
                     "EBITDA - Taxes", 
                     "Operating Cash Flow - CapEx", 
                     "Revenue - Operating Expenses"]
                )
                
                q5 = st.radio(
                    "5. Which financial metric is most important when using the EV/EBITDA multiple?",
                    ["Net Income", "EBITDA", "Revenue", "Book Value"]
                )
                
                submitted = st.form_submit_button("Submit Answers")
                
                if submitted:
                    score = 0
                    if q1 == "Cash Flow Statement":
                        score += 1
                    if q2 == "Earnings Before Interest, Tax, Depreciation, and Amortization":
                        score += 1
                    if q3 == "Long-term Debt":
                        score += 1
                    if q4 == "Operating Cash Flow - CapEx":
                        score += 1
                    if q5 == "EBITDA":
                        score += 1
                    
                    st.success(f"You scored {score}/5!")
                    
                    if score == 5:
                        st.balloons()
                        st.write("Perfect score! You're a financial statement analysis expert!")
                    elif score >= 3:
                        st.write("Good job! You have a solid understanding of financial statement analysis.")
                    else:
                        st.write("Keep learning! Check out our Financial Statement Analysis lesson for more information.")
        
        elif quiz_type == "Advanced Valuation Concepts":
            st.write("### Advanced Valuation Concepts Quiz")
            
            with st.form("advanced_quiz"):
                st.write("Test your knowledge of advanced valuation concepts.")
                
                q1 = st.radio(
                    "1. In an LBO model, what is IRR?",
                    ["Interest Rate of Return", 
                     "Internal Rate of Return", 
                     "Investment Return Ratio", 
                     "Incremental Revenue Rate"]
                )
                
                q2 = st.radio(
                    "2. What is a 'football field' chart in valuation?",
                    ["A chart showing industry performance", 
                     "A chart showing valuation ranges from different methods", 
                     "A chart tracking stock price movement", 
                     "A chart showing market share"]
                )
                
                q3 = st.radio(
                    "3. Which factor would NOT typically be included in a WACC calculation?",
                    ["Cost of Equity", "Cost of Debt", "Tax Rate", "Depreciation Rate"]
                )
                
                q4 = st.radio(
                    "4. In a sum-of-the-parts valuation, what is being valued?",
                    ["Each product line separately", 
                     "Each business segment or division separately", 
                     "Assets and liabilities separately", 
                     "Each year's cash flow separately"]
                )
                
                q5 = st.radio(
                    "5. What does a negative enterprise value suggest?",
                    ["The company has negative earnings", 
                     "The company's cash exceeds its market cap and debt", 
                     "The company has negative book value", 
                     "The company is in bankruptcy"]
                )
                
                submitted = st.form_submit_button("Submit Answers")
                
                if submitted:
                    score = 0
                    if q1 == "Internal Rate of Return":
                        score += 1
                    if q2 == "A chart showing valuation ranges from different methods":
                        score += 1
                    if q3 == "Depreciation Rate":
                        score += 1
                    if q4 == "Each business segment or division separately":
                        score += 1
                    if q5 == "The company's cash exceeds its market cap and debt":
                        score += 1
                    
                    st.success(f"You scored {score}/5!")
                    
                    if score == 5:
                        st.balloons()
                        st.write("Perfect score! You're an advanced valuation concepts expert!")
                    elif score >= 3:
                        st.write("Good job! You have a solid understanding of advanced valuation concepts.")
                    else:
                        st.write("Keep learning! Check out our Advanced Valuation Concepts lesson for more information.")
    
    with tab4:
        st.subheader("Valuation Courses")
        
        st.write("""
        Enhance your valuation skills with our structured courses. Each course includes 
        video lessons, practical examples, and a certificate upon completion.
        """)
        
        courses = [
            {
                "title": "Fundamentals of Company Valuation",
                "description": "Learn the basics of company valuation including key methods and financial concepts.",
                "modules": ["Introduction to Valuation", "Understanding Financial Statements", "DCF Basics", "Multiples-Based Valuation", "Final Project"],
                "duration": "5 hours",
                "level": "Beginner"
            },
            {
                "title": "Advanced DCF Modeling",
                "description": "Master the art of building complex DCF models with multiple scenarios and detailed projections.",
                "modules": ["Advanced Forecasting Techniques", "Complex Capital Structures", "Multi-Stage DCF Models", "Sensitivity Analysis", "Case Studies"],
                "duration": "8 hours",
                "level": "Intermediate"
            },
            {
                "title": "Private Company Valuation",
                "description": "Specialized techniques for valuing private companies with limited financial information.",
                "modules": ["Private vs. Public Valuation", "Adjusting Financial Statements", "Discount Rates for Private Companies", "Liquidity Discounts", "Case Studies"],
                "duration": "6 hours",
                "level": "Intermediate"
            },
            {
                "title": "M&A Valuation and Deal Structuring",
                "description": "Learn how to value acquisition targets and structure deals for maximum value creation.",
                "modules": ["Synergy Valuation", "Deal Structuring", "LBO Analysis", "Post-Merger Integration", "Case Studies"],
                "duration": "10 hours",
                "level": "Advanced"
            }
        ]
        
        for i, course in enumerate(courses):
            with st.expander(f"{course['title']} ({course['level']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{course['description']}**")
                    
                    st.write("**Modules:**")
                    for j, module in enumerate(course['modules']):
                        st.write(f"{j+1}. {module}")
                    
                    st.write(f"**Duration:** {course['duration']}")
                    
                with col2:
                    st.write("**Course Features:**")
                    st.write("✅ Video Lessons")
                    st.write("✅ Practical Examples")
                    st.write("✅ Excel Templates")
                    st.write("✅ Final Assessment")
                    st.write("✅ Completion Certificate")
                    
                    st.button(f"Enroll in Course", key=f"enroll_{i}")
        
        st.write("### ValuIt Certificate Program")
        
        st.write("""
        Complete all four courses to earn the ValuIt Professional Valuation Analyst certificate. 
        This credential demonstrates your expertise in company valuation across multiple methods 
        and scenarios.
        
        **Program Benefits:**
        - Comprehensive valuation knowledge
        - Practical skills applicable to real-world scenarios
        - Recognized credential for your resume
        - Access to advanced features on the ValuIt platform
        - Networking opportunities with other valuation professionals
        """)
        
        if st.button("Learn More About Certification"):
            st.info("""
            The ValuIt Professional Valuation Analyst certification program requires:
            1. Completion of all four core courses
            2. Passing score on the comprehensive final assessment
            3. Submission of a capstone valuation project
            
            For more information, please contact certification@valuit.com
            """)

