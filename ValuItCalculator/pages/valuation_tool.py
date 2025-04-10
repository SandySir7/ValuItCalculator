import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import io
from datetime import datetime

from utils.data_fetcher import DataFetcher
from utils.pdf_generator import PDFGenerator
from utils.excel_generator import ExcelGenerator
from models.dcf import DCFModel
from models.comparable_company import ComparableCompanyModel
from models.precedent_transactions import PrecedentTransactionsModel
from models.asset_based import AssetBasedModel
from models.lbo import LBOModel

def show(pro_mode=False):
    """
    Display the Valuation Tool page
    
    Args:
        pro_mode (bool): Whether professional mode is activated
    """
    st.title("Valuation Tool")
    
    # Create a dictionary to store valuation inputs
    if 'valuation_inputs' not in st.session_state:
        st.session_state.valuation_inputs = {
            'ticker': '',
            'company_name': '',
            'industry': '',
            'method': 'DCF',
            'growth_rate': 0.05,
            'wacc': 0.10,
            'terminal_growth_rate': 0.02,
            'forecast_years': 5,
            'ev_ebitda_multiple': 10.0,
            'pe_ratio': 15.0,
            'ev_revenue_multiple': 2.0,
            'asset_discount': 0.10,
            'lbo_exit_year': 5,
            'lbo_exit_multiple': 8.0,
            'target_irr': 0.20,
        }
    
    # Create a dictionary to store valuation results
    if 'valuation_results' not in st.session_state:
        st.session_state.valuation_results = None
    
    # Company information input section
    st.subheader("Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Company Ticker Symbol", 
                               value=st.session_state.valuation_inputs['ticker'],
                               help="Enter the stock ticker symbol (e.g., AAPL for Apple)")
        
        st.session_state.valuation_inputs['ticker'] = ticker
        
        if st.button("Fetch Company Data"):
            if ticker:
                with st.spinner("Fetching company data..."):
                    # Fetch company info
                    company_info = DataFetcher.get_company_info(ticker)
                    st.session_state.valuation_inputs['company_name'] = company_info.get('name', '')
                    st.session_state.valuation_inputs['industry'] = company_info.get('industry', '')
                    
                    # Store company info in session state for later use
                    st.session_state.company_info = company_info
                    
                    # Fetch financial data
                    financial_data = DataFetcher.get_financial_data(ticker)
                    st.session_state.financial_data = financial_data
                    
                    # Get industry averages
                    industry = company_info.get('industry', '')
                    industry_averages = DataFetcher.get_industry_averages(industry)
                    
                    # Update default inputs based on industry averages
                    st.session_state.valuation_inputs['growth_rate'] = industry_averages.get('revenue_growth', 0.05)
                    st.session_state.valuation_inputs['wacc'] = industry_averages.get('wacc', 0.10)
                    st.session_state.valuation_inputs['terminal_growth_rate'] = industry_averages.get('terminal_growth', 0.02)
                    st.session_state.valuation_inputs['ev_ebitda_multiple'] = industry_averages.get('ev_ebitda', 10.0)
                    st.session_state.valuation_inputs['pe_ratio'] = industry_averages.get('pe_ratio', 15.0)
                    st.session_state.valuation_inputs['ev_revenue_multiple'] = industry_averages.get('ev_revenue', 2.0)
                    
                    st.success(f"Data fetched successfully for {company_info.get('name', ticker)}")
                    st.rerun()
            else:
                st.error("Please enter a ticker symbol")
    
    with col2:
        company_name = st.text_input("Company Name", 
                                    value=st.session_state.valuation_inputs['company_name'],
                                    help="Enter the company name if ticker is not available")
        industry = st.text_input("Industry", 
                                value=st.session_state.valuation_inputs['industry'],
                                help="Enter the company's industry (e.g., Technology, Healthcare)")
        
        st.session_state.valuation_inputs['company_name'] = company_name
        st.session_state.valuation_inputs['industry'] = industry
    
    # Valuation method selection
    st.subheader("Valuation Method")
    
    valuation_methods = ["DCF", "Comparable Company Analysis", "Precedent Transactions", "Asset-Based Valuation"]
    if pro_mode:
        valuation_methods.append("LBO")
    
    method = st.selectbox("Select Valuation Method", 
                         valuation_methods,
                         index=valuation_methods.index(st.session_state.valuation_inputs['method']) if st.session_state.valuation_inputs['method'] in valuation_methods else 0,
                         help="Choose the valuation methodology you want to use")
    
    st.session_state.valuation_inputs['method'] = method
    
    # Display inputs based on selected valuation method
    st.subheader("Valuation Inputs")
    
    if method == "DCF":
        col1, col2 = st.columns(2)
        
        with col1:
            growth_rate = st.slider("Annual Growth Rate (%)", 
                                  min_value=-10.0, max_value=50.0, 
                                  value=float(st.session_state.valuation_inputs['growth_rate'] * 100),
                                  step=0.5,
                                  help="Projected annual growth rate for the forecast period") / 100
            
            wacc = st.slider("WACC - Discount Rate (%)", 
                           min_value=1.0, max_value=30.0, 
                           value=float(st.session_state.valuation_inputs['wacc'] * 100),
                           step=0.1,
                           help="Weighted Average Cost of Capital") / 100
            
            st.session_state.valuation_inputs['growth_rate'] = growth_rate
            st.session_state.valuation_inputs['wacc'] = wacc
        
        with col2:
            terminal_growth_rate = st.slider("Terminal Growth Rate (%)", 
                                           min_value=-2.0, max_value=10.0, 
                                           value=float(st.session_state.valuation_inputs['terminal_growth_rate'] * 100),
                                           step=0.1,
                                           help="Perpetual growth rate after the forecast period") / 100
            
            forecast_years = st.slider("Forecast Period (Years)", 
                                     min_value=1, max_value=10, 
                                     value=int(st.session_state.valuation_inputs['forecast_years']),
                                     step=1,
                                     help="Number of years to forecast future cash flows")
            
            st.session_state.valuation_inputs['terminal_growth_rate'] = terminal_growth_rate
            st.session_state.valuation_inputs['forecast_years'] = forecast_years
    
    elif method == "Comparable Company Analysis":
        col1, col2 = st.columns(2)
        
        with col1:
            ev_ebitda = st.slider("EV/EBITDA Multiple", 
                                min_value=1.0, max_value=50.0, 
                                value=float(st.session_state.valuation_inputs['ev_ebitda_multiple']),
                                step=0.5,
                                help="Enterprise Value to EBITDA multiple")
            
            pe_ratio = st.slider("P/E Ratio", 
                               min_value=1.0, max_value=100.0, 
                               value=float(st.session_state.valuation_inputs['pe_ratio']),
                               step=0.5,
                               help="Price to Earnings ratio")
            
            st.session_state.valuation_inputs['ev_ebitda_multiple'] = ev_ebitda
            st.session_state.valuation_inputs['pe_ratio'] = pe_ratio
        
        with col2:
            ev_revenue = st.slider("EV/Revenue Multiple", 
                                 min_value=0.1, max_value=20.0, 
                                 value=float(st.session_state.valuation_inputs['ev_revenue_multiple']),
                                 step=0.1,
                                 help="Enterprise Value to Revenue multiple")
            
            st.session_state.valuation_inputs['ev_revenue_multiple'] = ev_revenue
            
            # Option to view and select comparable companies
            if st.checkbox("Show Comparable Companies"):
                if st.session_state.valuation_inputs['ticker'] and st.session_state.valuation_inputs['industry']:
                    with st.spinner("Fetching comparable companies..."):
                        comparable_companies = DataFetcher.get_comparable_companies(
                            st.session_state.valuation_inputs['ticker'],
                            st.session_state.valuation_inputs['industry']
                        )
                        
                        if comparable_companies:
                            st.write("Comparable Companies:")
                            for company in comparable_companies:
                                st.write(f"- {company.get('name', company.get('ticker'))}: " +
                                        f"EV/EBITDA: {company.get('ev_ebitda', 'N/A')}, " +
                                        f"P/E: {company.get('pe_ratio', 'N/A')}, " +
                                        f"EV/Revenue: {company.get('ev_revenue', 'N/A')}")
                        else:
                            st.info("No comparable companies found.")
                else:
                    st.warning("Please enter ticker and industry to find comparable companies.")
    
    elif method == "Precedent Transactions":
        col1, col2 = st.columns(2)
        
        with col1:
            ev_ebitda = st.slider("EV/EBITDA Transaction Multiple", 
                                min_value=1.0, max_value=50.0, 
                                value=float(st.session_state.valuation_inputs['ev_ebitda_multiple']),
                                step=0.5,
                                help="Enterprise Value to EBITDA multiple from precedent transactions")
            
            st.session_state.valuation_inputs['ev_ebitda_multiple'] = ev_ebitda
        
        with col2:
            ev_revenue = st.slider("EV/Revenue Transaction Multiple", 
                                 min_value=0.1, max_value=20.0, 
                                 value=float(st.session_state.valuation_inputs['ev_revenue_multiple']),
                                 step=0.1,
                                 help="Enterprise Value to Revenue multiple from precedent transactions")
            
            st.session_state.valuation_inputs['ev_revenue_multiple'] = ev_revenue
            
            # Option to view precedent transactions
            if st.checkbox("Show Precedent Transactions"):
                if st.session_state.valuation_inputs['industry']:
                    with st.spinner("Fetching precedent transactions..."):
                        transactions = DataFetcher.get_precedent_transactions(
                            st.session_state.valuation_inputs['industry']
                        )
                        
                        if transactions:
                            st.write("Recent Transactions:")
                            for transaction in transactions:
                                st.write(f"- {transaction.get('target', 'Unknown')} acquired by " +
                                        f"{transaction.get('acquirer', 'Unknown')} ({transaction.get('date', 'N/A')}): " +
                                        f"Value: ${transaction.get('value', 'N/A')}B, " +
                                        f"EV/EBITDA: {transaction.get('ev_ebitda', 'N/A')}x, " +
                                        f"EV/Revenue: {transaction.get('ev_revenue', 'N/A')}x")
                        else:
                            st.info("No precedent transactions found.")
                else:
                    st.warning("Please enter industry to find precedent transactions.")
    
    elif method == "Asset-Based Valuation":
        asset_discount = st.slider("Asset Discount (%)", 
                                 min_value=0.0, max_value=50.0, 
                                 value=float(st.session_state.valuation_inputs['asset_discount'] * 100),
                                 step=1.0,
                                 help="Discount applied to book value of assets") / 100
        
        st.session_state.valuation_inputs['asset_discount'] = asset_discount
    
    elif method == "LBO" and pro_mode:
        col1, col2 = st.columns(2)
        
        with col1:
            exit_year = st.slider("Exit Year", 
                                min_value=3, max_value=10, 
                                value=int(st.session_state.valuation_inputs['lbo_exit_year']),
                                step=1,
                                help="Year of LBO exit")
            
            st.session_state.valuation_inputs['lbo_exit_year'] = exit_year
        
        with col2:
            exit_multiple = st.slider("Exit Multiple", 
                                    min_value=4.0, max_value=20.0, 
                                    value=float(st.session_state.valuation_inputs['lbo_exit_multiple']),
                                    step=0.5,
                                    help="EV/EBITDA multiple at exit")
            
            target_irr = st.slider("Target IRR (%)", 
                                 min_value=10.0, max_value=50.0, 
                                 value=float(st.session_state.valuation_inputs['target_irr'] * 100),
                                 step=1.0,
                                 help="Target Internal Rate of Return") / 100
            
            st.session_state.valuation_inputs['lbo_exit_multiple'] = exit_multiple
            st.session_state.valuation_inputs['target_irr'] = target_irr
    
    # Run Valuation button
    if st.button("Run Valuation"):
        if not (st.session_state.valuation_inputs['ticker'] or st.session_state.valuation_inputs['company_name']):
            st.error("Please enter a company ticker or name")
        else:
            with st.spinner("Running valuation..."):
                # Get company financial data if not already fetched
                if 'financial_data' not in st.session_state and st.session_state.valuation_inputs['ticker']:
                    try:
                        st.session_state.financial_data = DataFetcher.get_financial_data(st.session_state.valuation_inputs['ticker'])
                    except Exception as e:
                        st.error(f"Error fetching financial data: {str(e)}")
                        st.session_state.financial_data = {}
                
                # Get company info if not already fetched
                if 'company_info' not in st.session_state:
                    if st.session_state.valuation_inputs['ticker']:
                        try:
                            st.session_state.company_info = DataFetcher.get_company_info(st.session_state.valuation_inputs['ticker'])
                        except Exception as e:
                            st.error(f"Error fetching company info: {str(e)}")
                            st.session_state.company_info = {
                                'name': st.session_state.valuation_inputs['company_name'],
                                'industry': st.session_state.valuation_inputs['industry'],
                                'sector': 'N/A'
                            }
                    else:
                        st.session_state.company_info = {
                            'name': st.session_state.valuation_inputs['company_name'],
                            'industry': st.session_state.valuation_inputs['industry'],
                            'sector': 'N/A'
                        }
                
                # Run the appropriate valuation model
                try:
                    if method == "DCF":
                        model = DCFModel(
                            financial_data=st.session_state.financial_data if 'financial_data' in st.session_state else {},
                            growth_rate=st.session_state.valuation_inputs['growth_rate'],
                            wacc=st.session_state.valuation_inputs['wacc'],
                            terminal_growth_rate=st.session_state.valuation_inputs['terminal_growth_rate'],
                            forecast_years=st.session_state.valuation_inputs['forecast_years']
                        )
                        valuation_results = model.run_valuation()
                    
                    elif method == "Comparable Company Analysis":
                        model = ComparableCompanyModel(
                            financial_data=st.session_state.financial_data if 'financial_data' in st.session_state else {},
                            industry=st.session_state.valuation_inputs['industry'],
                            ticker=st.session_state.valuation_inputs['ticker'],
                            ev_ebitda_multiple=st.session_state.valuation_inputs['ev_ebitda_multiple'],
                            pe_ratio=st.session_state.valuation_inputs['pe_ratio'],
                            ev_revenue_multiple=st.session_state.valuation_inputs['ev_revenue_multiple']
                        )
                        valuation_results = model.run_valuation()
                    
                    elif method == "Precedent Transactions":
                        model = PrecedentTransactionsModel(
                            financial_data=st.session_state.financial_data if 'financial_data' in st.session_state else {},
                            industry=st.session_state.valuation_inputs['industry'],
                            ev_ebitda_multiple=st.session_state.valuation_inputs['ev_ebitda_multiple'],
                            ev_revenue_multiple=st.session_state.valuation_inputs['ev_revenue_multiple']
                        )
                        valuation_results = model.run_valuation()
                    
                    elif method == "Asset-Based Valuation":
                        model = AssetBasedModel(
                            financial_data=st.session_state.financial_data if 'financial_data' in st.session_state else {},
                            asset_discount=st.session_state.valuation_inputs['asset_discount']
                        )
                        valuation_results = model.run_valuation()
                    
                    elif method == "LBO" and pro_mode:
                        model = LBOModel(
                            financial_data=st.session_state.financial_data if 'financial_data' in st.session_state else {},
                            exit_year=st.session_state.valuation_inputs['lbo_exit_year'],
                            exit_multiple=st.session_state.valuation_inputs['lbo_exit_multiple'],
                            target_irr=st.session_state.valuation_inputs['target_irr']
                        )
                        valuation_results = model.run_valuation()
                    
                    # Add method and ticker to results
                    valuation_results['method'] = method
                    valuation_results['ticker'] = st.session_state.valuation_inputs['ticker']
                    valuation_results['company_name'] = st.session_state.valuation_inputs['company_name']
                    valuation_results['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Add inputs to results
                    valuation_results['inputs'] = st.session_state.valuation_inputs.copy()
                    
                    # Store results in session state
                    st.session_state.valuation_results = valuation_results
                    
                    # Create a new valuation in the user's history if logged in
                    if st.session_state.user and valuation_results:
                        new_valuation = {
                            'id': len(st.session_state.valuations) + 1,
                            'company': valuation_results['company_name'] if valuation_results['company_name'] else valuation_results['ticker'],
                            'method': valuation_results['method'],
                            'enterprise_value': valuation_results.get('enterprise_value', 'N/A'),
                            'equity_value': valuation_results.get('equity_value', 'N/A'),
                            'timestamp': valuation_results['timestamp'],
                            'data': valuation_results
                        }
                        
                        st.session_state.valuations.append(new_valuation)
                        st.session_state.current_valuation = new_valuation
                
                except Exception as e:
                    st.error(f"Error running valuation: {str(e)}")
    
    # Display valuation results if available
    if st.session_state.valuation_results:
        display_valuation_results(st.session_state.valuation_results, st.session_state.company_info if 'company_info' in st.session_state else {})

def display_valuation_results(results, company_info):
    """
    Display valuation results
    
    Args:
        results (dict): Valuation results
        company_info (dict): Company information
    """
    st.markdown("---")
    st.subheader("Valuation Results")
    
    # Company name and method
    company_name = results.get('company_name', '') or results.get('ticker', '')
    st.write(f"**Company:** {company_name}")
    st.write(f"**Valuation Method:** {results.get('method', '')}")
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    # Format values to millions or billions
    def format_value(value):
        if isinstance(value, (int, float)):
            if abs(value) >= 1e9:
                return f"${value/1e9:.2f} billion"
            elif abs(value) >= 1e6:
                return f"${value/1e6:.2f} million"
            else:
                return f"${value:.2f}"
        return value
    
    enterprise_value = results.get('enterprise_value', 'N/A')
    equity_value = results.get('equity_value', 'N/A')
    
    with col1:
        st.metric("Enterprise Value", format_value(enterprise_value))
    
    with col2:
        st.metric("Equity Value", format_value(equity_value))
    
    with col3:
        if results.get('method') == 'DCF':
            st.metric("Implied WACC", f"{results.get('inputs', {}).get('wacc', 0) * 100:.2f}%")
        elif results.get('method') in ['Comparable Company Analysis', 'Precedent Transactions']:
            st.metric("Implied EV/EBITDA", f"{results.get('inputs', {}).get('ev_ebitda_multiple', 0):.2f}x")
        elif results.get('method') == 'Asset-Based Valuation':
            st.metric("Asset Discount", f"{results.get('inputs', {}).get('asset_discount', 0) * 100:.2f}%")
        elif results.get('method') == 'LBO':
            st.metric("Target IRR", f"{results.get('inputs', {}).get('target_irr', 0) * 100:.2f}%")
    
    # Detailed results
    st.write("### Detailed Results")
    
    # Display results based on the valuation method
    if results.get('method') == 'DCF':
        # DCF Visualization
        if 'dcf_details' in results:
            dcf_details = results['dcf_details']
            
            # Cash flow chart
            years = [f"Year {i+1}" for i in range(len(dcf_details.get('fcf_forecast', [])))]
            fcf_forecast = dcf_details.get('fcf_forecast', [])
            present_values = dcf_details.get('present_values', [])
            
            # Create cash flow chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=years,
                y=fcf_forecast,
                name='Forecasted Cash Flow',
                marker_color='#0066cc'
            ))
            
            fig.add_trace(go.Bar(
                x=years,
                y=present_values,
                name='Present Value',
                marker_color='#00cc66'
            ))
            
            fig.update_layout(
                title='Forecasted Cash Flows vs. Present Values',
                xaxis_title='Forecast Period',
                yaxis_title='Value',
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
            
            # Display DCF summary
            st.write("#### DCF Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Forecasted Cash Flows**")
                for i, (year, fcf, pv) in enumerate(zip(years, fcf_forecast, present_values)):
                    st.write(f"{year}: {format_value(fcf)} (PV: {format_value(pv)})")
            
            with col2:
                st.write("**Valuation Components**")
                st.write(f"Sum of PV of FCF: {format_value(sum(present_values))}")
                st.write(f"Terminal Value: {format_value(dcf_details.get('terminal_value', 'N/A'))}")
                st.write(f"PV of Terminal Value: {format_value(dcf_details.get('pv_terminal_value', 'N/A'))}")
                st.write(f"Enterprise Value: {format_value(results.get('enterprise_value', 'N/A'))}")
                st.write(f"Total Debt: {format_value(dcf_details.get('debt', 'N/A'))}")
                st.write(f"Cash: {format_value(dcf_details.get('cash', 'N/A'))}")
                st.write(f"Equity Value: {format_value(results.get('equity_value', 'N/A'))}")
            
            # Sensitivity analysis
            st.write("#### Sensitivity Analysis")
            
            # Create WACC vs. Terminal Growth Rate sensitivity table
            if 'sensitivity_analysis' in dcf_details:
                sensitivity = dcf_details['sensitivity_analysis']
                
                # Convert sensitivity data to a DataFrame
                wacc_values = sensitivity.get('wacc_values', [])
                growth_values = sensitivity.get('growth_values', [])
                ev_matrix = sensitivity.get('ev_matrix', [])
                
                if wacc_values and growth_values and ev_matrix:
                    sensitivity_df = pd.DataFrame(ev_matrix, columns=[f"{g*100:.1f}%" for g in growth_values])
                    sensitivity_df.index = [f"{w*100:.1f}%" for w in wacc_values]
                    sensitivity_df.index.name = "WACC"
                    
                    # Format values in the DataFrame
                    for i in range(sensitivity_df.shape[0]):
                        for j in range(sensitivity_df.shape[1]):
                            sensitivity_df.iloc[i, j] = format_value(sensitivity_df.iloc[i, j])
                    
                    st.write("WACC vs. Terminal Growth Rate Sensitivity (Enterprise Value)")
                    st.dataframe(sensitivity_df, use_container_width=True)
    
    elif results.get('method') == 'Comparable Company Analysis':
        # Comparable Company Visualization
        if 'comps_details' in results:
            comps_details = results['comps_details']
            
            # Create multiples comparison chart
            if 'comparable_companies' in comps_details:
                companies = comps_details.get('comparable_companies', [])
                
                if companies:
                    # Extract data for chart
                    company_names = [comp.get('name', comp.get('ticker', 'Unknown')) for comp in companies]
                    ev_ebitda_values = [comp.get('ev_ebitda', 0) for comp in companies]
                    pe_values = [comp.get('pe_ratio', 0) for comp in companies]
                    ev_revenue_values = [comp.get('ev_revenue', 0) for comp in companies]
                    
                    # Add the subject company
                    company_names.append('Subject Company')
                    ev_ebitda_values.append(results.get('inputs', {}).get('ev_ebitda_multiple', 0))
                    pe_values.append(results.get('inputs', {}).get('pe_ratio', 0))
                    ev_revenue_values.append(results.get('inputs', {}).get('ev_revenue_multiple', 0))
                    
                    # Create DataFrame for plotting
                    df = pd.DataFrame({
                        'Company': company_names * 3,
                        'Multiple Type': ['EV/EBITDA'] * len(company_names) + ['P/E'] * len(company_names) + ['EV/Revenue'] * len(company_names),
                        'Value': ev_ebitda_values + pe_values + ev_revenue_values
                    })
                    
                    # Create the grouped bar chart
                    fig = px.bar(
                        df, 
                        x='Company', 
                        y='Value', 
                        color='Multiple Type',
                        barmode='group',
                        title='Comparable Company Multiples Comparison',
                        color_discrete_map={
                            'EV/EBITDA': '#0066cc',
                            'P/E': '#00cc66',
                            'EV/Revenue': '#cc6600'
                        }
                    )
                    
                    fig.update_layout(
                        xaxis_title='',
                        yaxis_title='Multiple Value',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display comparable companies table
                    st.write("#### Comparable Companies")
                    
                    # Create DataFrame for display
                    comp_df = pd.DataFrame([
                        {
                            'Company': comp.get('name', comp.get('ticker', 'Unknown')),
                            'Market Cap': format_value(comp.get('marketCap', 'N/A')),
                            'EV/EBITDA': f"{comp.get('ev_ebitda', 'N/A')}x" if isinstance(comp.get('ev_ebitda'), (int, float)) else comp.get('ev_ebitda', 'N/A'),
                            'P/E': f"{comp.get('pe_ratio', 'N/A')}x" if isinstance(comp.get('pe_ratio'), (int, float)) else comp.get('pe_ratio', 'N/A'),
                            'EV/Revenue': f"{comp.get('ev_revenue', 'N/A')}x" if isinstance(comp.get('ev_revenue'), (int, float)) else comp.get('ev_revenue', 'N/A')
                        } for comp in companies
                    ])
                    
                    st.dataframe(comp_df, use_container_width=True)
            
            # Display valuation summary
            st.write("#### Valuation Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Valuation by Multiple**")
                st.write(f"EV/EBITDA: {format_value(comps_details.get('ev_ebitda_valuation', 'N/A'))}")
                st.write(f"P/E: {format_value(comps_details.get('pe_valuation', 'N/A'))}")
                st.write(f"EV/Revenue: {format_value(comps_details.get('ev_revenue_valuation', 'N/A'))}")
            
            with col2:
                st.write("**Financial Metrics**")
                st.write(f"EBITDA: {format_value(comps_details.get('ebitda', 'N/A'))}")
                st.write(f"Net Income: {format_value(comps_details.get('net_income', 'N/A'))}")
                st.write(f"Revenue: {format_value(comps_details.get('revenue', 'N/A'))}")
                st.write(f"Debt: {format_value(comps_details.get('debt', 'N/A'))}")
                st.write(f"Cash: {format_value(comps_details.get('cash', 'N/A'))}")
    
    elif results.get('method') == 'Precedent Transactions':
        # Precedent Transactions Visualization
        if 'transactions_details' in results:
            transactions_details = results['transactions_details']
            
            # Create transaction multiples chart
            if 'transactions' in transactions_details:
                transactions = transactions_details.get('transactions', [])
                
                if transactions:
                    # Extract data for chart
                    transaction_names = [f"{t.get('target', 'Unknown')}/{t.get('acquirer', 'Unknown')}" for t in transactions]
                    ev_ebitda_values = [t.get('ev_ebitda', 0) for t in transactions]
                    ev_revenue_values = [t.get('ev_revenue', 0) for t in transactions]
                    
                    # Add the selected multiple
                    transaction_names.append('Selected Multiple')
                    ev_ebitda_values.append(results.get('inputs', {}).get('ev_ebitda_multiple', 0))
                    ev_revenue_values.append(results.get('inputs', {}).get('ev_revenue_multiple', 0))
                    
                    # Create DataFrame for plotting
                    df = pd.DataFrame({
                        'Transaction': transaction_names * 2,
                        'Multiple Type': ['EV/EBITDA'] * len(transaction_names) + ['EV/Revenue'] * len(transaction_names),
                        'Value': ev_ebitda_values + ev_revenue_values
                    })
                    
                    # Create the grouped bar chart
                    fig = px.bar(
                        df, 
                        x='Transaction', 
                        y='Value', 
                        color='Multiple Type',
                        barmode='group',
                        title='Precedent Transaction Multiples Comparison',
                        color_discrete_map={
                            'EV/EBITDA': '#0066cc',
                            'EV/Revenue': '#cc6600'
                        }
                    )
                    
                    fig.update_layout(
                        xaxis_title='',
                        yaxis_title='Multiple Value',
                        xaxis_tickangle=-45,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display transactions table
                    st.write("#### Precedent Transactions")
                    
                    # Create DataFrame for display
                    trans_df = pd.DataFrame([
                        {
                            'Target': t.get('target', 'Unknown'),
                            'Acquirer': t.get('acquirer', 'Unknown'),
                            'Date': t.get('date', 'N/A'),
                            'Value ($B)': t.get('value', 'N/A'),
                            'EV/EBITDA': f"{t.get('ev_ebitda', 'N/A')}x" if isinstance(t.get('ev_ebitda'), (int, float)) else t.get('ev_ebitda', 'N/A'),
                            'EV/Revenue': f"{t.get('ev_revenue', 'N/A')}x" if isinstance(t.get('ev_revenue'), (int, float)) else t.get('ev_revenue', 'N/A')
                        } for t in transactions
                    ])
                    
                    st.dataframe(trans_df, use_container_width=True)
            
            # Display valuation summary
            st.write("#### Valuation Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Valuation by Multiple**")
                st.write(f"EV/EBITDA: {format_value(transactions_details.get('ev_ebitda_valuation', 'N/A'))}")
                st.write(f"EV/Revenue: {format_value(transactions_details.get('ev_revenue_valuation', 'N/A'))}")
            
            with col2:
                st.write("**Financial Metrics**")
                st.write(f"EBITDA: {format_value(transactions_details.get('ebitda', 'N/A'))}")
                st.write(f"Revenue: {format_value(transactions_details.get('revenue', 'N/A'))}")
                st.write(f"Debt: {format_value(transactions_details.get('debt', 'N/A'))}")
                st.write(f"Cash: {format_value(transactions_details.get('cash', 'N/A'))}")
    
    elif results.get('method') == 'Asset-Based Valuation':
        # Asset-Based Visualization
        if 'asset_details' in results:
            asset_details = results['asset_details']
            
            # Create assets and liabilities chart
            assets = asset_details.get('total_assets', 0)
            liabilities = asset_details.get('total_liabilities', 0)
            equity = assets - liabilities
            
            # Create the bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['Assets', 'Liabilities', 'Equity'],
                y=[assets, liabilities, equity],
                marker_color=['#0066cc', '#cc6600', '#00cc66']
            ))
            
            fig.update_layout(
                title='Assets, Liabilities, and Equity',
                xaxis_title='',
                yaxis_title='Value'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display asset-based valuation summary
            st.write("#### Asset-Based Valuation Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Balance Sheet Items**")
                st.write(f"Total Assets: {format_value(asset_details.get('total_assets', 'N/A'))}")
                st.write(f"Total Liabilities: {format_value(asset_details.get('total_liabilities', 'N/A'))}")
                st.write(f"Book Value of Equity: {format_value(asset_details.get('book_equity', 'N/A'))}")
            
            with col2:
                st.write("**Valuation Details**")
                st.write(f"Asset Discount: {asset_details.get('asset_discount', 0) * 100:.2f}%")
                st.write(f"Adjusted Asset Value: {format_value(asset_details.get('adjusted_assets', 'N/A'))}")
                st.write(f"Equity Value: {format_value(results.get('equity_value', 'N/A'))}")
    
    elif results.get('method') == 'LBO':
        # LBO Visualization
        if 'lbo_details' in results:
            lbo_details = results['lbo_details']
            
            # Create IRR vs. Entry Multiple chart
            if 'irr_sensitivity' in lbo_details:
                irr_sensitivity = lbo_details['irr_sensitivity']
                
                # Extract data for chart
                entry_multiples = irr_sensitivity.get('entry_multiples', [])
                irr_values = irr_sensitivity.get('irr_values', [])
                
                if entry_multiples and irr_values:
                    # Create the line chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=entry_multiples,
                        y=[irr * 100 for irr in irr_values],
                        mode='lines+markers',
                        name='IRR',
                        line=dict(color='#0066cc', width=3)
                    ))
                    
                    # Add target IRR line
                    target_irr = results.get('inputs', {}).get('target_irr', 0) * 100
                    fig.add_trace(go.Scatter(
                        x=[min(entry_multiples), max(entry_multiples)],
                        y=[target_irr, target_irr],
                        mode='lines',
                        name=f'Target IRR ({target_irr:.1f}%)',
                        line=dict(color='#cc6600', width=2, dash='dash')
                    ))
                    
                    fig.update_layout(
                        title='IRR vs. Entry Multiple',
                        xaxis_title='Entry Multiple (EV/EBITDA)',
                        yaxis_title='IRR (%)',
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Display LBO summary
            st.write("#### LBO Valuation Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**LBO Assumptions**")
                st.write(f"Entry Multiple: {lbo_details.get('entry_multiple', 'N/A')}x")
                st.write(f"Exit Multiple: {results.get('inputs', {}).get('lbo_exit_multiple', 'N/A')}x")
                st.write(f"Exit Year: {results.get('inputs', {}).get('lbo_exit_year', 'N/A')}")
                st.write(f"Target IRR: {results.get('inputs', {}).get('target_irr', 0) * 100:.2f}%")
            
            with col2:
                st.write("**Valuation Details**")
                st.write(f"Purchase Price: {format_value(lbo_details.get('purchase_price', 'N/A'))}")
                st.write(f"Exit Value: {format_value(lbo_details.get('exit_value', 'N/A'))}")
                st.write(f"Implied Equity Value: {format_value(results.get('equity_value', 'N/A'))}")
                st.write(f"Maximum Debt: {format_value(lbo_details.get('max_debt', 'N/A'))}")
    
    # Download reports section
    st.markdown("---")
    st.subheader("Download Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Download PDF Report"):
            try:
                pdf_data = PDFGenerator.generate_valuation_report(
                    valuation_data=results,
                    company_info=company_info
                )
                
                company_name = results.get('company_name', '') or results.get('ticker', 'company')
                filename = f"{company_name.replace(' ', '_')}_{results.get('method', '').replace(' ', '_')}_valuation.pdf"
                
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    with col2:
        if st.button("Download Excel Report"):
            try:
                excel_data = ExcelGenerator.generate_valuation_excel(
                    valuation_data=results,
                    company_info=company_info
                )
                
                company_name = results.get('company_name', '') or results.get('ticker', 'company')
                filename = f"{company_name.replace(' ', '_')}_{results.get('method', '').replace(' ', '_')}_valuation.xlsx"
                
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error generating Excel: {str(e)}")
    
    # Save valuation option for logged in users
    if st.session_state.user:
        if st.button("Save Valuation"):
            if 'valuations' not in st.session_state:
                st.session_state.valuations = []
            
            # Create a new valuation entry
            new_valuation = {
                'id': len(st.session_state.valuations) + 1,
                'company': results.get('company_name', '') or results.get('ticker', 'Unknown'),
                'method': results.get('method', ''),
                'enterprise_value': results.get('enterprise_value', 'N/A'),
                'equity_value': results.get('equity_value', 'N/A'),
                'timestamp': results.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                'data': results
            }
            
            # Add to user's valuations
            st.session_state.valuations.append(new_valuation)
            st.session_state.current_valuation = new_valuation
            
            st.success("Valuation saved successfully!")
