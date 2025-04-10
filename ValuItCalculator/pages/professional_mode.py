import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from utils.data_fetcher import DataFetcher
from utils.financial_calculations import FinancialCalculations

def show():
    """Display the Professional Mode page"""
    
    st.title("Professional Mode")
    
    # Check if user is logged in and pro mode is activated
    if not st.session_state.user:
        st.warning("Please login to access Professional Mode.")
        return
    
    if not st.session_state.pro_mode:
        st.warning("Please activate Professional Mode in the sidebar.")
        return
    
    st.write("""
    Welcome to Professional Mode! Here you can perform advanced valuation analyses 
    with custom parameters, detailed projections, and scenario analysis.
    """)
    
    # Advanced settings section
    st.subheader("Advanced Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Custom WACC", "Scenario Analysis", "Detailed Projections", "LBO Analysis"])
    
    with tab1:
        st.write("### WACC Calculator")
        st.write("Calculate the Weighted Average Cost of Capital (WACC) with detailed inputs.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            risk_free_rate = st.slider("Risk-Free Rate (%)", 
                                     min_value=0.0, max_value=10.0, 
                                     value=3.0, 
                                     step=0.1,
                                     help="Usually based on 10-year Treasury yield") / 100
            
            market_risk_premium = st.slider("Market Risk Premium (%)", 
                                          min_value=1.0, max_value=15.0, 
                                          value=6.0, 
                                          step=0.1,
                                          help="Expected market return minus risk-free rate") / 100
            
            beta = st.slider("Beta", 
                           min_value=0.1, max_value=3.0, 
                           value=1.0, 
                           step=0.05,
                           help="Measure of company's volatility compared to the market")
        
        with col2:
            cost_of_debt = st.slider("Cost of Debt (%)", 
                                   min_value=1.0, max_value=20.0, 
                                   value=5.0, 
                                   step=0.1,
                                   help="Interest rate the company pays on its debt") / 100
            
            tax_rate = st.slider("Corporate Tax Rate (%)", 
                               min_value=0.0, max_value=40.0, 
                               value=21.0, 
                               step=0.5,
                               help="Effective corporate tax rate") / 100
            
            debt_weight = st.slider("Debt Weight (%)", 
                                  min_value=0.0, max_value=100.0, 
                                  value=30.0, 
                                  step=1.0,
                                  help="Debt as a percentage of total capital") / 100
            
            equity_weight = 1 - debt_weight
            st.write(f"Equity Weight: {equity_weight * 100:.1f}%")
        
        if st.button("Calculate WACC"):
            try:
                wacc = FinancialCalculations.calculate_wacc(
                    risk_free_rate=risk_free_rate,
                    market_risk_premium=market_risk_premium,
                    beta=beta,
                    cost_of_debt=cost_of_debt,
                    tax_rate=tax_rate,
                    debt_weight=debt_weight,
                    equity_weight=equity_weight
                )
                
                st.success(f"Calculated WACC: {wacc * 100:.2f}%")
                
                # WACC components breakdown
                cost_of_equity = risk_free_rate + beta * market_risk_premium
                tax_adjusted_cost_of_debt = cost_of_debt * (1 - tax_rate)
                
                # Create a DataFrame for the components
                components_df = pd.DataFrame({
                    'Component': ['Cost of Equity', 'After-Tax Cost of Debt', 'WACC'],
                    'Value (%)': [cost_of_equity * 100, tax_adjusted_cost_of_debt * 100, wacc * 100],
                    'Weight (%)': [equity_weight * 100, debt_weight * 100, 100],
                    'Contribution (%)': [equity_weight * cost_of_equity * 100, 
                                        debt_weight * tax_adjusted_cost_of_debt * 100, 
                                        wacc * 100]
                })
                
                # Format to 2 decimal places
                components_df['Value (%)'] = components_df['Value (%)'].apply(lambda x: f"{x:.2f}%")
                components_df['Weight (%)'] = components_df['Weight (%)'].apply(lambda x: f"{x:.2f}%")
                components_df['Contribution (%)'] = components_df['Contribution (%)'].apply(lambda x: f"{x:.2f}%")
                
                st.dataframe(components_df, use_container_width=True)
                
                # Create a WACC waterfall chart
                fig = go.Figure(go.Waterfall(
                    name = "WACC Breakdown",
                    orientation = "v",
                    measure = ["relative", "relative", "total"],
                    x = ["Cost of Equity", "After-Tax Cost of Debt", "WACC"],
                    textposition = "outside",
                    text = [f"{equity_weight * cost_of_equity * 100:.2f}%", 
                            f"{debt_weight * tax_adjusted_cost_of_debt * 100:.2f}%", 
                            f"{wacc * 100:.2f}%"],
                    y = [equity_weight * cost_of_equity * 100, 
                         debt_weight * tax_adjusted_cost_of_debt * 100, 
                         0],
                    connector = {"line":{"color":"rgb(63, 63, 63)"}},
                ))
                
                fig.update_layout(
                    title = "WACC Breakdown",
                    showlegend = False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Update the session state with the calculated WACC
                st.session_state.valuation_inputs['wacc'] = wacc
                
            except Exception as e:
                st.error(f"Error calculating WACC: {str(e)}")
    
    with tab2:
        st.write("### Scenario Analysis")
        st.write("Analyze company valuation under different economic scenarios.")
        
        # Create different scenarios
        scenarios = ["Base Case", "Bull Case", "Bear Case"]
        selected_scenario = st.selectbox("Select Scenario", scenarios)
        
        # Set parameters based on selected scenario
        if selected_scenario == "Base Case":
            revenue_growth = 0.05
            ebitda_margin = 0.20
            wacc = 0.10
            terminal_growth = 0.02
        elif selected_scenario == "Bull Case":
            revenue_growth = 0.10
            ebitda_margin = 0.25
            wacc = 0.09
            terminal_growth = 0.03
        else:  # Bear Case
            revenue_growth = 0.02
            ebitda_margin = 0.15
            wacc = 0.11
            terminal_growth = 0.01
        
        col1, col2 = st.columns(2)
        
        with col1:
            revenue_growth = st.slider(f"Revenue Growth (%) - {selected_scenario}", 
                                     min_value=-10.0, max_value=50.0, 
                                     value=revenue_growth * 100, 
                                     step=0.5) / 100
            
            ebitda_margin = st.slider(f"EBITDA Margin (%) - {selected_scenario}", 
                                    min_value=0.0, max_value=60.0, 
                                    value=ebitda_margin * 100, 
                                    step=0.5) / 100
        
        with col2:
            wacc = st.slider(f"WACC (%) - {selected_scenario}", 
                           min_value=1.0, max_value=30.0, 
                           value=wacc * 100, 
                           step=0.1) / 100
            
            terminal_growth = st.slider(f"Terminal Growth (%) - {selected_scenario}", 
                                      min_value=-2.0, max_value=10.0, 
                                      value=terminal_growth * 100, 
                                      step=0.1) / 100
        
        # Option to compare all scenarios
        if st.checkbox("Compare All Scenarios"):
            # Create a DataFrame with all scenarios
            scenarios_df = pd.DataFrame({
                'Scenario': ["Base Case", "Bull Case", "Bear Case"],
                'Revenue Growth': [0.05, 0.10, 0.02],
                'EBITDA Margin': [0.20, 0.25, 0.15],
                'WACC': [0.10, 0.09, 0.11],
                'Terminal Growth': [0.02, 0.03, 0.01]
            })
            
            # Format percentages
            scenarios_df['Revenue Growth'] = scenarios_df['Revenue Growth'].apply(lambda x: f"{x*100:.1f}%")
            scenarios_df['EBITDA Margin'] = scenarios_df['EBITDA Margin'].apply(lambda x: f"{x*100:.1f}%")
            scenarios_df['WACC'] = scenarios_df['WACC'].apply(lambda x: f"{x*100:.1f}%")
            scenarios_df['Terminal Growth'] = scenarios_df['Terminal Growth'].apply(lambda x: f"{x*100:.1f}%")
            
            st.dataframe(scenarios_df, use_container_width=True)
            
            # Create a comparison chart for enterprise values
            enterprise_values = {
                'Base Case': 1000000000,  # $1B - these would be calculated in a real app
                'Bull Case': 1500000000,  # $1.5B
                'Bear Case': 700000000    # $0.7B
            }
            
            fig = px.bar(
                x=list(enterprise_values.keys()),
                y=list(enterprise_values.values()),
                title="Enterprise Value by Scenario",
                labels={'x': 'Scenario', 'y': 'Enterprise Value ($)'}
            )
            
            # Format y-axis to show billions
            fig.update_layout(
                yaxis=dict(
                    tickformat="$,.1f",
                    ticksuffix="B"
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.write("### Detailed Financial Projections")
        st.write("Create and analyze detailed financial projections for DCF analysis.")
        
        # Input for initial revenue and growth rates
        col1, col2 = st.columns(2)
        
        with col1:
            base_revenue = st.number_input("Base Year Revenue ($M)", 
                                         min_value=1.0, 
                                         value=100.0, 
                                         step=10.0,
                                         help="Revenue for the most recent fiscal year (in millions)")
            
            forecast_years = st.slider("Forecast Period (Years)", 
                                     min_value=1, max_value=10, 
                                     value=5, 
                                     step=1)
        
        with col2:
            growth_rates = []
            for i in range(forecast_years):
                growth_rate = st.slider(f"Year {i+1} Growth Rate (%)", 
                                      min_value=-20.0, max_value=50.0, 
                                      value=5.0, 
                                      step=0.5) / 100
                growth_rates.append(growth_rate)
        
        # Calculate revenue projections
        revenues = [base_revenue]
        for i in range(forecast_years):
            next_revenue = revenues[-1] * (1 + growth_rates[i])
            revenues.append(next_revenue)
        
        revenues = revenues[1:]  # Remove base year
        
        # Input for EBITDA margin
        ebitda_margins = []
        for i in range(forecast_years):
            ebitda_margin = st.slider(f"Year {i+1} EBITDA Margin (%)", 
                                    min_value=0.0, max_value=60.0, 
                                    value=20.0, 
                                    step=0.5) / 100
            ebitda_margins.append(ebitda_margin)
        
        # Calculate EBITDA projections
        ebitdas = [revenues[i] * ebitda_margins[i] for i in range(forecast_years)]
        
        # Input for capital expenditures as % of revenue
        capex_percent = st.slider("Capital Expenditures (% of Revenue)", 
                                min_value=0.0, max_value=30.0, 
                                value=5.0, 
                                step=0.5) / 100
        
        # Calculate capex projections
        capex = [revenues[i] * capex_percent for i in range(forecast_years)]
        
        # Input for depreciation as % of capex
        depreciation_percent = st.slider("Depreciation (% of CapEx)", 
                                       min_value=0.0, max_value=200.0, 
                                       value=80.0, 
                                       step=5.0) / 100
        
        # Calculate depreciation projections
        depreciation = [capex[i] * depreciation_percent for i in range(forecast_years)]
        
        # Input for working capital as % of revenue change
        wc_percent = st.slider("Working Capital (% of Revenue Change)", 
                             min_value=0.0, max_value=30.0, 
                             value=10.0, 
                             step=0.5) / 100
        
        # Calculate working capital projections
        wc_changes = []
        for i in range(forecast_years):
            if i == 0:
                revenue_change = revenues[i] - base_revenue
            else:
                revenue_change = revenues[i] - revenues[i-1]
            
            wc_change = revenue_change * wc_percent
            wc_changes.append(wc_change)
        
        # Calculate free cash flow projections
        fcf = []
        for i in range(forecast_years):
            tax_rate = 0.21  # Assuming 21% corporate tax rate
            nopat = ebitdas[i] - depreciation[i]
            nopat_after_tax = nopat * (1 - tax_rate)
            
            cash_flow = nopat_after_tax + depreciation[i] - capex[i] - wc_changes[i]
            fcf.append(cash_flow)
        
        # Create a DataFrame for the projections
        years = [f"Year {i+1}" for i in range(forecast_years)]
        projections_df = pd.DataFrame({
            'Year': years,
            'Revenue ($M)': [round(rev, 2) for rev in revenues],
            'EBITDA ($M)': [round(ebitda, 2) for ebitda in ebitdas],
            'CapEx ($M)': [round(cap, 2) for cap in capex],
            'Depreciation ($M)': [round(dep, 2) for dep in depreciation],
            'Working Capital Change ($M)': [round(wc, 2) for wc in wc_changes],
            'Free Cash Flow ($M)': [round(cf, 2) for cf in fcf]
        })
        
        st.write("#### Financial Projections")
        st.dataframe(projections_df, use_container_width=True)
        
        # Create a chart of the projections
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=years,
            y=revenues,
            name='Revenue',
            marker_color='#0066cc'
        ))
        
        fig.add_trace(go.Bar(
            x=years,
            y=ebitdas,
            name='EBITDA',
            marker_color='#00cc66'
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=fcf,
            name='Free Cash Flow',
            mode='lines+markers',
            line=dict(color='#cc6600', width=3)
        ))
        
        fig.update_layout(
            title='Financial Projections',
            xaxis_title='Forecast Period',
            yaxis_title='Value ($M)',
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate enterprise value using DCF
        if st.button("Calculate Enterprise Value using DCF"):
            wacc = st.session_state.valuation_inputs.get('wacc', 0.10)
            terminal_growth_rate = st.session_state.valuation_inputs.get('terminal_growth_rate', 0.02)
            
            # Discount FCF to present value
            present_values = FinancialCalculations.discount_cash_flows(fcf, wacc)
            
            # Calculate terminal value
            terminal_value = FinancialCalculations.calculate_terminal_value(
                final_fcf=fcf[-1],
                growth_rate=terminal_growth_rate,
                discount_rate=wacc
            )
            
            # Discount terminal value to present
            discounted_terminal_value = terminal_value / ((1 + wacc) ** forecast_years)
            
            # Calculate enterprise value
            enterprise_value = sum(present_values) + discounted_terminal_value
            
            # Format values to millions
            def format_millions(value):
                return f"${value:.2f}M"
            
            # Display results
            st.write("#### DCF Valuation Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"WACC: {wacc*100:.2f}%")
                st.write(f"Terminal Growth Rate: {terminal_growth_rate*100:.2f}%")
                st.write(f"Sum of PV of FCF: {format_millions(sum(present_values))}")
                
            with col2:
                st.write(f"Terminal Value: {format_millions(terminal_value)}")
                st.write(f"PV of Terminal Value: {format_millions(discounted_terminal_value)}")
                st.write(f"Enterprise Value: {format_millions(enterprise_value)}")
            
            # Create a waterfall chart to show the components of enterprise value
            fig = go.Figure(go.Waterfall(
                name = "Enterprise Value Breakdown",
                orientation = "v",
                measure = ["relative"] * len(present_values) + ["relative", "total"],
                x = [f"PV of FCF Year {i+1}" for i in range(len(present_values))] + ["PV of Terminal Value", "Enterprise Value"],
                textposition = "outside",
                text = [format_millions(pv) for pv in present_values] + [format_millions(discounted_terminal_value), format_millions(enterprise_value)],
                y = present_values + [discounted_terminal_value, 0],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            
            fig.update_layout(
                title = "DCF Valuation Breakdown",
                showlegend = False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.write("### LBO Analysis")
        st.write("Perform Leveraged Buyout (LBO) analysis with detailed inputs.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            enterprise_value = st.number_input("Enterprise Value ($M)", 
                                             min_value=10.0, 
                                             value=1000.0, 
                                             step=10.0,
                                             help="Total company value (debt + equity)")
            
            ebitda = st.number_input("EBITDA ($M)", 
                                   min_value=1.0, 
                                   value=100.0, 
                                   step=1.0,
                                   help="Annual EBITDA")
            
            existing_debt = st.number_input("Existing Debt ($M)", 
                                          min_value=0.0, 
                                          value=200.0, 
                                          step=10.0,
                                          help="Current outstanding debt")
            
            cash = st.number_input("Cash ($M)", 
                                 min_value=0.0, 
                                 value=50.0, 
                                 step=5.0,
                                 help="Current cash and cash equivalents")
        
        with col2:
            debt_percent = st.slider("Debt Percentage (%)", 
                                   min_value=0.0, max_value=100.0, 
                                   value=70.0, 
                                   step=1.0,
                                   help="Percentage of purchase price funded with debt") / 100
            
            interest_rate = st.slider("Interest Rate (%)", 
                                    min_value=1.0, max_value=20.0, 
                                    value=8.0, 
                                    step=0.1,
                                    help="Interest rate on new debt") / 100
            
            exit_multiple = st.slider("Exit EV/EBITDA Multiple", 
                                    min_value=1.0, max_value=20.0, 
                                    value=8.0, 
                                    step=0.1,
                                    help="Multiple at exit")
            
            exit_year = st.slider("Exit Year", 
                                min_value=3, max_value=10, 
                                value=5, 
                                step=1,
                                help="Year of exit")
            
            ebitda_growth = st.slider("Annual EBITDA Growth (%)", 
                                    min_value=-10.0, max_value=30.0, 
                                    value=5.0, 
                                    step=0.5,
                                    help="Annual EBITDA growth rate") / 100
        
        if st.button("Run LBO Analysis"):
            try:
                # Calculate equity value
                equity_value = enterprise_value - existing_debt + cash
                
                # Calculate purchase price
                purchase_price = enterprise_value
                
                # Calculate required debt and equity
                new_debt = purchase_price * debt_percent
                new_equity = purchase_price - new_debt
                
                # Calculate EBITDA projection
                ebitda_projection = []
                current_ebitda = ebitda
                
                for i in range(exit_year):
                    current_ebitda *= (1 + ebitda_growth)
                    ebitda_projection.append(current_ebitda)
                
                # Calculate exit value
                exit_ebitda = ebitda_projection[-1]
                exit_enterprise_value = exit_ebitda * exit_multiple
                
                # Assume debt is paid down linearly
                annual_debt_repayment = new_debt / exit_year
                remaining_debt = new_debt - (annual_debt_repayment * exit_year)
                
                # Calculate exit equity value
                exit_equity_value = exit_enterprise_value - remaining_debt
                
                # Calculate returns
                equity_multiple = exit_equity_value / new_equity
                irr = (equity_multiple ** (1 / exit_year)) - 1
                
                # Display results
                st.write("#### LBO Analysis Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Purchase Details**")
                    st.write(f"Enterprise Value: ${enterprise_value:.2f}M")
                    st.write(f"Equity Value: ${equity_value:.2f}M")
                    st.write(f"Purchase Price: ${purchase_price:.2f}M")
                    st.write(f"New Debt: ${new_debt:.2f}M")
                    st.write(f"New Equity: ${new_equity:.2f}M")
                
                with col2:
                    st.write("**Exit Details**")
                    st.write(f"Exit Year: {exit_year}")
                    st.write(f"Exit EBITDA: ${exit_ebitda:.2f}M")
                    st.write(f"Exit Multiple: {exit_multiple:.1f}x")
                    st.write(f"Exit Enterprise Value: ${exit_enterprise_value:.2f}M")
                    st.write(f"Remaining Debt: ${remaining_debt:.2f}M")
                    st.write(f"Exit Equity Value: ${exit_equity_value:.2f}M")
                
                st.write("**Returns**")
                st.write(f"Equity Multiple: {equity_multiple:.2f}x")
                st.write(f"IRR: {irr*100:.2f}%")
                
                # Create an IRR sensitivity table
                st.write("#### IRR Sensitivity Analysis")
                
                # Create a range of exit multiples and exit years
                exit_multiples = [exit_multiple - 2, exit_multiple - 1, exit_multiple, exit_multiple + 1, exit_multiple + 2]
                exit_years_range = [exit_year - 1, exit_year, exit_year + 1]
                
                # Calculate IRR for each combination
                irr_matrix = []
                
                for year in exit_years_range:
                    irr_row = []
                    
                    for multiple in exit_multiples:
                        # Calculate exit values for this scenario
                        scenario_exit_ebitda = ebitda * ((1 + ebitda_growth) ** year)
                        scenario_exit_ev = scenario_exit_ebitda * multiple
                        scenario_remaining_debt = new_debt - (annual_debt_repayment * year)
                        scenario_exit_equity = scenario_exit_ev - scenario_remaining_debt
                        
                        # Calculate returns
                        scenario_equity_multiple = scenario_exit_equity / new_equity
                        scenario_irr = (scenario_equity_multiple ** (1 / year)) - 1
                        
                        irr_row.append(scenario_irr * 100)  # Convert to percentage
                    
                    irr_matrix.append(irr_row)
                
                # Create a sensitivity table
                irr_df = pd.DataFrame(
                    irr_matrix,
                    columns=[f"{m:.1f}x" for m in exit_multiples],
                    index=[f"{y} years" for y in exit_years_range]
                )
                
                irr_df.index.name = "Exit Year"
                irr_df.columns.name = "Exit Multiple"
                
                # Format values
                irr_df = irr_df.applymap(lambda x: f"{x:.2f}%")
                
                st.dataframe(irr_df, use_container_width=True)
                
                # Create a waterfall chart to show the components of equity value
                fig = go.Figure(go.Waterfall(
                    name = "Equity Value Bridge",
                    orientation = "v",
                    measure = ["absolute", "relative", "relative", "relative", "total"],
                    x = ["Initial Equity", "EBITDA Growth", "Multiple Expansion", "Debt Paydown", "Exit Equity"],
                    textposition = "outside",
                    text = [f"${new_equity:.2f}M", 
                           f"${(exit_ebitda - ebitda) * exit_multiple:.2f}M", 
                           f"${exit_ebitda * (exit_multiple - (enterprise_value/ebitda)):.2f}M", 
                           f"${new_debt - remaining_debt:.2f}M", 
                           f"${exit_equity_value:.2f}M"],
                    y = [new_equity, 
                        (exit_ebitda - ebitda) * exit_multiple, 
                        exit_ebitda * (exit_multiple - (enterprise_value/ebitda)), 
                        new_debt - remaining_debt, 
                        0],  # The total will be calculated automatically
                    connector = {"line":{"color":"rgb(63, 63, 63)"}},
                ))
                
                fig.update_layout(
                    title = "Equity Value Bridge from Entry to Exit",
                    showlegend = False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in LBO analysis: {str(e)}")
                
    # Validation request section
    st.subheader("Professional Validation")
    
    st.write("""
    Request a review of your valuation by financial professionals. 
    Our experts will review your assumptions and provide feedback on your valuation.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        validation_name = st.text_input("Your Name")
        validation_email = st.text_input("Your Email")
        validation_company = st.text_input("Company Being Valued")
    
    with col2:
        validation_method = st.selectbox(
            "Valuation Method",
            ["DCF", "Comparable Company Analysis", "Precedent Transactions", "Asset-Based Valuation", "LBO"]
        )
        urgency = st.selectbox("Urgency", ["Standard (3-5 business days)", "Rush (1-2 business days)"])
        comments = st.text_area("Additional Comments or Questions")
    
    if st.button("Submit Validation Request"):
        if validation_name and validation_email and validation_company:
            st.success("""
            Your validation request has been submitted! 
            Our professional team will review your valuation and send feedback to your email.
            """)
            
            # In a real app, this would send the request to a backend system
            validation_request = {
                'name': validation_name,
                'email': validation_email,
                'company': validation_company,
                'method': validation_method,
                'urgency': urgency,
                'comments': comments,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'Pending'
            }
            
            # Store validation request in session state for demo purposes
            if 'validation_requests' not in st.session_state:
                st.session_state.validation_requests = []
            
            st.session_state.validation_requests.append(validation_request)
        else:
            st.error("Please fill in all required fields.")

