import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_fetcher import DataFetcher

def show():
    """Display the Company Info page"""
    
    st.title("Company Information")
    
    st.write("""
    Get detailed information about public companies, including financial data, 
    ESG metrics, and recent news.
    """)
    
    # Company search section
    ticker = st.text_input("Enter Company Ticker Symbol", help="Enter the stock ticker symbol (e.g., AAPL for Apple)")
    
    if st.button("Get Company Info") or ticker:
        if ticker:
            with st.spinner("Fetching company information..."):
                try:
                    # Fetch company information
                    company_info = DataFetcher.get_company_info(ticker)
                    
                    if company_info.get('name', '') == 'N/A':
                        st.error(f"Could not find information for ticker: {ticker}")
                    else:
                        # Display company information
                        display_company_info(ticker, company_info)
                        
                except Exception as e:
                    st.error(f"Error fetching company information: {str(e)}")
        else:
            st.warning("Please enter a ticker symbol")
    else:
        # Display sample companies
        st.subheader("Popular Companies")
        
        sample_companies = [
            {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
            {"ticker": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
            {"ticker": "AMZN", "name": "Amazon.com, Inc.", "sector": "Consumer Cyclical"},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Communication Services"},
            {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare"},
            {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial Services"},
            {"ticker": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Defensive"},
            {"ticker": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy"},
            {"ticker": "TSLA", "name": "Tesla, Inc.", "sector": "Consumer Cyclical"},
            {"ticker": "V", "name": "Visa Inc.", "sector": "Financial Services"}
        ]
        
        # Create columns for companies
        cols = st.columns(5)
        
        for i, company in enumerate(sample_companies):
            col_index = i % 5
            with cols[col_index]:
                if st.button(f"{company['ticker']}", key=f"sample_{company['ticker']}"):
                    # Set the ticker value
                    ticker = company['ticker']
                    st.rerun()
        
        # Display tickers by sector
        sectors = list(set([company['sector'] for company in sample_companies]))
        sectors.sort()
        
        selected_sector = st.selectbox("Browse by Sector", ["All"] + sectors)
        
        if selected_sector != "All":
            sector_companies = [company for company in sample_companies if company['sector'] == selected_sector]
        else:
            sector_companies = sample_companies
        
        # Display companies in a table
        sector_df = pd.DataFrame(sector_companies)
        st.dataframe(sector_df, use_container_width=True)

def display_company_info(ticker, company_info):
    """
    Display detailed company information
    
    Args:
        ticker (str): Company ticker symbol
        company_info (dict): Company information
    """
    # Main company header
    st.header(company_info.get('name', ticker))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("Company Overview")
        st.write(f"**Sector:** {company_info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {company_info.get('industry', 'N/A')}")
        st.write(f"**Country:** {company_info.get('country', 'N/A')}")
        st.write(f"**Employees:** {company_info.get('employees', 'N/A')}")
        if company_info.get('website', 'N/A') != 'N/A':
            st.write(f"**Website:** [{company_info.get('website')}]({company_info.get('website')})")
    
    with col2:
        st.subheader("Market Data")
        
        # Format market cap to billions/millions
        market_cap = company_info.get('marketCap', 'N/A')
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1e9:
                market_cap_str = f"${market_cap/1e9:.2f}B"
            elif market_cap >= 1e6:
                market_cap_str = f"${market_cap/1e6:.2f}M"
            else:
                market_cap_str = f"${market_cap:.2f}"
        else:
            market_cap_str = market_cap
        
        st.write(f"**Market Cap:** {market_cap_str}")
        st.write(f"**Currency:** {company_info.get('currency', 'USD')}")
        
        # Fetch financial data
        try:
            financial_data = DataFetcher.get_financial_data(ticker)
            
            # Get most recent revenue and EBITDA
            if financial_data.get('revenue', {}):
                recent_revenue = list(financial_data.get('revenue', {}).values())[0]
                if isinstance(recent_revenue, (int, float)):
                    if recent_revenue >= 1e9:
                        revenue_str = f"${recent_revenue/1e9:.2f}B"
                    elif recent_revenue >= 1e6:
                        revenue_str = f"${recent_revenue/1e6:.2f}M"
                    else:
                        revenue_str = f"${recent_revenue:.2f}"
                else:
                    revenue_str = "N/A"
                st.write(f"**Revenue (LTM):** {revenue_str}")
            
            if financial_data.get('ebitda', {}):
                recent_ebitda = list(financial_data.get('ebitda', {}).values())[0]
                if isinstance(recent_ebitda, (int, float)):
                    if recent_ebitda >= 1e9:
                        ebitda_str = f"${recent_ebitda/1e9:.2f}B"
                    elif recent_ebitda >= 1e6:
                        ebitda_str = f"${recent_ebitda/1e6:.2f}M"
                    else:
                        ebitda_str = f"${recent_ebitda:.2f}"
                else:
                    ebitda_str = "N/A"
                st.write(f"**EBITDA (LTM):** {ebitda_str}")
        except Exception as e:
            st.write("**Financial Data:** Could not fetch")
    
    with col3:
        # Fetch ESG data
        try:
            esg_data = DataFetcher.get_esg_metrics(ticker)
            
            st.subheader("ESG Profile")
            
            esg_score = esg_data.get('esgScore', 'N/A')
            if esg_score != 'N/A':
                # Create a gauge chart for the ESG score
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = esg_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "ESG Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#0066cc"},
                        'steps' : [
                            {'range': [0, 33], 'color': "#ffcccc"},
                            {'range': [33, 66], 'color': "#ffffcc"},
                            {'range': [66, 100], 'color': "#ccffcc"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': esg_score
                        }
                    }
                ))
                
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("**ESG Score:** N/A")
            
            environmental = esg_data.get('environmentalScore', 'N/A')
            social = esg_data.get('socialScore', 'N/A')
            governance = esg_data.get('governanceScore', 'N/A')
            
            if environmental != 'N/A' and social != 'N/A' and governance != 'N/A':
                # Create a radar chart for the ESG components
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=[environmental, social, governance],
                    theta=['Environmental', 'Social', 'Governance'],
                    fill='toself',
                    name=ticker
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=200
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write(f"**Environmental:** {environmental}")
                st.write(f"**Social:** {social}")
                st.write(f"**Governance:** {governance}")
                
        except Exception as e:
            st.write("**ESG Data:** Could not fetch")
    
    # Business description
    st.subheader("Business Description")
    st.write(company_info.get('description', 'No description available.'))
    
    # Financial data and charts
    st.subheader("Financial Performance")
    
    try:
        financial_data = DataFetcher.get_financial_data(ticker)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Revenue & Profitability", "Balance Sheet", "Cash Flow", "Ratios"])
        
        with tab1:
            # Revenue and EBITDA chart
            if financial_data.get('revenue', {}) and financial_data.get('ebitda', {}):
                revenue_data = financial_data.get('revenue', {})
                ebitda_data = financial_data.get('ebitda', {})
                
                # Convert to DataFrame
                dates = sorted(list(set(list(revenue_data.keys()) + list(ebitda_data.keys()))))
                fin_df = pd.DataFrame(index=dates)
                
                fin_df['Revenue'] = [revenue_data.get(date, None) for date in dates]
                fin_df['EBITDA'] = [ebitda_data.get(date, None) for date in dates]
                
                # Create a bar chart with Plotly
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=fin_df.index,
                    y=fin_df['Revenue'],
                    name='Revenue',
                    marker_color='#0066cc'
                ))
                
                fig.add_trace(go.Bar(
                    x=fin_df.index,
                    y=fin_df['EBITDA'],
                    name='EBITDA',
                    marker_color='#00cc66'
                ))
                
                fig.update_layout(
                    title='Revenue and EBITDA',
                    xaxis_title='Year',
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
                
                # Calculate and display EBITDA margin
                fin_df['EBITDA Margin'] = fin_df['EBITDA'] / fin_df['Revenue']
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=fin_df.index,
                    y=fin_df['EBITDA Margin'],
                    mode='lines+markers',
                    name='EBITDA Margin',
                    line=dict(color='#cc6600', width=3)
                ))
                
                fig.update_layout(
                    title='EBITDA Margin',
                    xaxis_title='Year',
                    yaxis_title='Margin',
                    yaxis_tickformat='.0%'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No revenue and EBITDA data available.")
            
            # Net income chart
            if financial_data.get('net_income', {}):
                net_income_data = financial_data.get('net_income', {})
                
                # Convert to DataFrame
                dates = sorted(list(net_income_data.keys()))
                ni_df = pd.DataFrame(index=dates)
                
                ni_df['Net Income'] = [net_income_data.get(date, None) for date in dates]
                
                # Create a bar chart with Plotly
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=ni_df.index,
                    y=ni_df['Net Income'],
                    name='Net Income',
                    marker_color='#0066cc'
                ))
                
                fig.update_layout(
                    title='Net Income',
                    xaxis_title='Year',
                    yaxis_title='Value'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No net income data available.")
        
        with tab2:
            # Balance sheet items
            if financial_data.get('total_assets', {}) and financial_data.get('equity', {}):
                assets_data = financial_data.get('total_assets', {})
                equity_data = financial_data.get('equity', {})
                debt_data = financial_data.get('total_debt', {})
                
                # Convert to DataFrame
                dates = sorted(list(set(list(assets_data.keys()) + list(equity_data.keys()) + list(debt_data.keys()))))
                bs_df = pd.DataFrame(index=dates)
                
                bs_df['Total Assets'] = [assets_data.get(date, None) for date in dates]
                bs_df['Equity'] = [equity_data.get(date, None) for date in dates]
                bs_df['Debt'] = [debt_data.get(date, None) for date in dates]
                
                # Create a bar chart with Plotly
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=bs_df.index,
                    y=bs_df['Total Assets'],
                    name='Total Assets',
                    marker_color='#0066cc'
                ))
                
                fig.add_trace(go.Bar(
                    x=bs_df.index,
                    y=bs_df['Equity'],
                    name='Equity',
                    marker_color='#00cc66'
                ))
                
                fig.add_trace(go.Bar(
                    x=bs_df.index,
                    y=bs_df['Debt'],
                    name='Debt',
                    marker_color='#cc6600'
                ))
                
                fig.update_layout(
                    title='Balance Sheet Items',
                    xaxis_title='Year',
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
                
                # Calculate and display Debt-to-Equity ratio
                bs_df['Debt-to-Equity'] = bs_df['Debt'] / bs_df['Equity']
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=bs_df.index,
                    y=bs_df['Debt-to-Equity'],
                    mode='lines+markers',
                    name='Debt-to-Equity',
                    line=dict(color='#cc6600', width=3)
                ))
                
                fig.update_layout(
                    title='Debt-to-Equity Ratio',
                    xaxis_title='Year',
                    yaxis_title='Ratio'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No balance sheet data available.")
        
        with tab3:
            # Cash flow items
            if financial_data.get('fcf', {}):
                fcf_data = financial_data.get('fcf', {})
                
                # Convert to DataFrame
                dates = sorted(list(fcf_data.keys()))
                cf_df = pd.DataFrame(index=dates)
                
                cf_df['Free Cash Flow'] = [fcf_data.get(date, None) for date in dates]
                
                # Create a bar chart with Plotly
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=cf_df.index,
                    y=cf_df['Free Cash Flow'],
                    name='Free Cash Flow',
                    marker_color='#0066cc'
                ))
                
                fig.update_layout(
                    title='Free Cash Flow',
                    xaxis_title='Year',
                    yaxis_title='Value'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate FCF growth rate
                cf_df['FCF Growth'] = cf_df['Free Cash Flow'].pct_change()
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=cf_df.index[1:],  # Skip first item as growth is N/A
                    y=cf_df['FCF Growth'][1:],
                    mode='lines+markers',
                    name='FCF Growth',
                    line=dict(color='#cc6600', width=3)
                ))
                
                fig.update_layout(
                    title='Free Cash Flow Growth',
                    xaxis_title='Year',
                    yaxis_title='Growth Rate',
                    yaxis_tickformat='.0%'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No cash flow data available.")
        
        with tab4:
            # Calculate financial ratios
            if (financial_data.get('revenue', {}) and financial_data.get('ebitda', {}) and 
                financial_data.get('net_income', {}) and financial_data.get('total_assets', {})):
                
                # Get the most recent data
                recent_revenue = list(financial_data.get('revenue', {}).values())[0]
                recent_ebitda = list(financial_data.get('ebitda', {}).values())[0]
                recent_net_income = list(financial_data.get('net_income', {}).values())[0]
                recent_assets = list(financial_data.get('total_assets', {}).values())[0]
                recent_equity = list(financial_data.get('equity', {}).values())[0] if financial_data.get('equity', {}) else 0
                recent_debt = list(financial_data.get('total_debt', {}).values())[0] if financial_data.get('total_debt', {}) else 0
                recent_fcf = list(financial_data.get('fcf', {}).values())[0] if financial_data.get('fcf', {}) else 0
                
                # Calculate ratios
                ebitda_margin = recent_ebitda / recent_revenue if recent_revenue else 0
                net_margin = recent_net_income / recent_revenue if recent_revenue else 0
                roa = recent_net_income / recent_assets if recent_assets else 0
                roe = recent_net_income / recent_equity if recent_equity else 0
                debt_to_equity = recent_debt / recent_equity if recent_equity else 0
                fcf_to_revenue = recent_fcf / recent_revenue if recent_revenue else 0
                
                # Create a DataFrame
                ratios_df = pd.DataFrame({
                    'Ratio': [
                        'EBITDA Margin',
                        'Net Margin',
                        'Return on Assets',
                        'Return on Equity',
                        'Debt-to-Equity',
                        'FCF to Revenue'
                    ],
                    'Value': [
                        f"{ebitda_margin:.2%}",
                        f"{net_margin:.2%}",
                        f"{roa:.2%}",
                        f"{roe:.2%}",
                        f"{debt_to_equity:.2f}",
                        f"{fcf_to_revenue:.2%}"
                    ]
                })
                
                st.dataframe(ratios_df, use_container_width=True)
                
                # Create a radar chart for the ratios
                fig = go.Figure()
                
                # Normalize ratio values for radar chart
                ebitda_margin_norm = min(ebitda_margin * 100, 50) / 50  # Cap at 50%
                net_margin_norm = min(net_margin * 100, 30) / 30  # Cap at 30%
                roa_norm = min(roa * 100, 20) / 20  # Cap at 20%
                roe_norm = min(roe * 100, 30) / 30  # Cap at 30%
                debt_to_equity_norm = 1 - min(debt_to_equity, 2) / 2  # Cap at 2, invert so lower is better
                fcf_to_revenue_norm = min(fcf_to_revenue * 100, 20) / 20  # Cap at 20%
                
                fig.add_trace(go.Scatterpolar(
                    r=[ebitda_margin_norm, net_margin_norm, roa_norm, roe_norm, debt_to_equity_norm, fcf_to_revenue_norm],
                    theta=['EBITDA Margin', 'Net Margin', 'ROA', 'ROE', 'Debt-to-Equity', 'FCF to Revenue'],
                    fill='toself',
                    name=ticker
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )
                    ),
                    title="Financial Ratio Profile"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Insufficient data to calculate financial ratios.")
                
    except Exception as e:
        st.error(f"Error displaying financial data: {str(e)}")
    
    # Comparable companies
    st.subheader("Comparable Companies")
    
    try:
        comparable_companies = DataFetcher.get_comparable_companies(
            ticker,
            company_info.get('industry', '')
        )
        
        if comparable_companies:
            # Create a DataFrame
            comps_df = pd.DataFrame([
                {
                    'Company': comp.get('name', comp.get('ticker', 'Unknown')),
                    'Ticker': comp.get('ticker', 'N/A'),
                    'Market Cap': format_value(comp.get('marketCap', 'N/A')),
                    'EV/EBITDA': f"{comp.get('ev_ebitda', 'N/A')}x" if isinstance(comp.get('ev_ebitda'), (int, float)) else comp.get('ev_ebitda', 'N/A'),
                    'P/E': f"{comp.get('pe_ratio', 'N/A')}x" if isinstance(comp.get('pe_ratio'), (int, float)) else comp.get('pe_ratio', 'N/A'),
                    'EV/Revenue': f"{comp.get('ev_revenue', 'N/A')}x" if isinstance(comp.get('ev_revenue'), (int, float)) else comp.get('ev_revenue', 'N/A')
                } for comp in comparable_companies
            ])
            
            st.dataframe(comps_df, use_container_width=True)
            
            # Create a multiples comparison chart
            if comparable_companies:
                # Extract data for chart
                company_names = [comp.get('name', comp.get('ticker', 'Unknown')) for comp in comparable_companies]
                ev_ebitda_values = [comp.get('ev_ebitda', 0) for comp in comparable_companies]
                pe_values = [comp.get('pe_ratio', 0) for comp in comparable_companies]
                ev_revenue_values = [comp.get('ev_revenue', 0) for comp in comparable_companies]
                
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
                    title='Comparable Company Multiples',
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
        else:
            st.info("No comparable companies found.")
    except Exception as e:
        st.error(f"Error displaying comparable companies: {str(e)}")
    
    # Recent news placeholder
    st.subheader("Recent News")
    
    # Placeholder for actual news items
    news_items = [
        {
            'title': f"{company_info.get('name', ticker)} Reports Quarterly Earnings",
            'date': (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            'source': 'Financial Times',
            'summary': f"{company_info.get('name', ticker)} reported quarterly earnings that exceeded analyst expectations, driven by strong growth in its core business segments."
        },
        {
            'title': f"{company_info.get('name', ticker)} Announces New Product Line",
            'date': (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            'source': 'Wall Street Journal',
            'summary': f"{company_info.get('name', ticker)} announced the launch of a new product line that aims to expand its market presence in emerging markets."
        },
        {
            'title': f"Analyst Upgrades {company_info.get('name', ticker)} Stock",
            'date': (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
            'source': 'Bloomberg',
            'summary': f"Analysts at a major investment bank upgraded {company_info.get('name', ticker)} stock from 'hold' to 'buy', citing improved growth prospects and competitive positioning."
        }
    ]
    
    for news in news_items:
        with st.expander(f"{news['date']} - {news['title']}"):
            st.write(f"**Source:** {news['source']}")
            st.write(news['summary'])
            st.write("*This is a placeholder news item. In a real application, actual news would be displayed.*")

def format_value(value):
    """Format value to millions/billions with $ symbol"""
    if isinstance(value, (int, float)):
        if value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        else:
            return f"${value:.2f}"
    return value

