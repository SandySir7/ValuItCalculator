import pandas as pd
import numpy as np
import requests
import yfinance as yf
import time

class DataFetcher:
    """Utility class to fetch financial data from various sources"""
    
    @staticmethod
    def get_company_info(ticker):
        """
        Fetch basic company information
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            dict: Company information
        """
        try:
            company = yf.Ticker(ticker)
            info = company.info
            
            # Basic company information
            company_info = {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'country': info.get('country', 'N/A'),
                'employees': info.get('fullTimeEmployees', 'N/A'),
                'marketCap': info.get('marketCap', 'N/A'),
                'currency': info.get('currency', 'USD'),
                'website': info.get('website', 'N/A'),
                'description': info.get('longBusinessSummary', 'N/A'),
            }
            
            return company_info
            
        except Exception as e:
            print(f"Error fetching company info: {e}")
            return {
                'name': ticker,
                'sector': 'N/A',
                'industry': 'N/A',
                'country': 'N/A',
                'employees': 'N/A',
                'marketCap': 'N/A',
                'currency': 'USD',
                'website': 'N/A',
                'description': 'Could not fetch company description.'
            }
    
    @staticmethod
    def get_financial_data(ticker):
        """
        Fetch financial data for a company
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            dict: Financial data
        """
        try:
            company = yf.Ticker(ticker)
            
            # Income statement
            income_stmt = company.income_stmt
            
            # Balance sheet
            balance_sheet = company.balance_sheet
            
            # Cash flow
            cash_flow = company.cashflow
            
            # Prepare financial metrics
            financial_data = {
                'revenue': income_stmt.loc['Total Revenue'].to_dict() if 'Total Revenue' in income_stmt.index else {},
                'ebitda': income_stmt.loc['EBITDA'].to_dict() if 'EBITDA' in income_stmt.index else {},
                'net_income': income_stmt.loc['Net Income'].to_dict() if 'Net Income' in income_stmt.index else {},
                'total_assets': balance_sheet.loc['Total Assets'].to_dict() if 'Total Assets' in balance_sheet.index else {},
                'total_debt': balance_sheet.loc['Total Debt'].to_dict() if 'Total Debt' in balance_sheet.index else {},
                'cash': balance_sheet.loc['Cash'].to_dict() if 'Cash' in balance_sheet.index else {},
                'equity': balance_sheet.loc['Total Stockholder Equity'].to_dict() if 'Total Stockholder Equity' in balance_sheet.index else {},
                'fcf': cash_flow.loc['Free Cash Flow'].to_dict() if 'Free Cash Flow' in cash_flow.index else {},
            }
            
            return financial_data
            
        except Exception as e:
            print(f"Error fetching financial data: {e}")
            # Return empty data structure
            return {
                'revenue': {},
                'ebitda': {},
                'net_income': {},
                'total_assets': {},
                'total_debt': {},
                'cash': {},
                'equity': {},
                'fcf': {},
            }
    
    @staticmethod
    def check_sp500_membership(ticker):
        """
        Check if a company is in the S&P 500 index
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            bool: True if in S&P 500, False otherwise
        """
        try:
            # Use a list of the largest constituents
            sp500_major_stocks = [
                'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'GOOG', 'META', 'BRK-B', 'LLY', 'AVGO',
                'TSLA', 'V', 'UNH', 'JPM', 'XOM', 'PG', 'MA', 'HD', 'COST', 'ORCL', 'MRK', 'ABBV',
                'ADBE', 'CSCO', 'ACN', 'AMD', 'MCD', 'CRM', 'NFLX', 'INTC', 'PEP', 'TMO', 'CMCSA',
                'IBM', 'QCOM', 'DIS', 'VZ', 'CAT', 'PFE', 'TXN', 'PM', 'MS', 'NEE', 'WMT', 'BAC',
                'CVX', 'DHR', 'LIN', 'ABT', 'COP', 'KO', 'WFC', 'TJX', 'MMM', 'AMGN', 'NKE', 'MDT',
                'RTX', 'BMY', 'UPS', 'PM', 'SCHW', 'HON', 'LOW', 'SPGI', 'GS', 'UNP', 'INTU', 'ELV'
            ]
            return ticker in sp500_major_stocks
        except Exception as e:
            print(f"Error checking S&P 500 membership: {e}")
            return False

    @staticmethod
    def get_industry_averages(ticker_or_industry):
        """
        Calculate industry average metrics based on the sector of a given ticker,
        or return defaults for a given industry name
        
        Args:
            ticker_or_industry (str): Ticker symbol or industry name
            
        Returns:
            dict: Industry average metrics and index membership info
        """
        # First check if this is a ticker or industry name
        is_ticker = len(ticker_or_industry) <= 5 and ticker_or_industry.isupper()
        
        if is_ticker:
            ticker = ticker_or_industry
            try:
                # Get company info to determine sector
                company = yf.Ticker(ticker)
                info = company.info
                sector = info.get('sector', None)
                
                # Check index membership
                is_sp500 = DataFetcher.check_sp500_membership(ticker)
                
                # If we have a valid sector, calculate averages from peers
                if sector:
                    # Get peers in the same sector
                    peers_data = DataFetcher.get_sector_peers_metrics(ticker, sector, is_sp500)
                    
                    # If we got valid peer data, return it
                    if peers_data and len(peers_data) > 0:
                        # Add index membership info
                        peers_data['index_membership'] = {
                            'sp500': is_sp500
                        }
                        return peers_data
            except Exception as e:
                print(f"Error calculating industry averages for {ticker}: {e}")
                # Fall back to defaults based on sector if we have it
                if 'sector' in locals() and sector:
                    return DataFetcher.get_industry_defaults(sector)
        else:
            # If it's not a ticker, treat it as an industry name
            industry = ticker_or_industry
            return DataFetcher.get_industry_defaults(industry)
            
        # Default case
        return DataFetcher.get_industry_defaults('Default')
        
    @staticmethod
    def get_sector_peers_metrics(ticker, sector, is_sp500=False):
        """
        Calculate average metrics for peers in the same sector
        
        Args:
            ticker (str): Company ticker symbol
            sector (str): Company sector
            is_sp500 (bool): Whether the company is in the S&P 500
            
        Returns:
            dict: Average metrics for peer companies
        """
        try:
            # Start with a basic list of peers by sector
            sector_peers = {
                'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'NVDA', 'ADBE', 'CRM', 'INTC', 'CSCO'],
                'Healthcare': ['JNJ', 'PFE', 'MRK', 'UNH', 'ABT', 'LLY', 'TMO', 'ABBV', 'BMY', 'AMGN'],
                'Financial Services': ['JPM', 'BAC', 'GS', 'MS', 'WFC', 'C', 'BLK', 'V', 'MA', 'AXP'],
                'Consumer Goods': ['PG', 'KO', 'PEP', 'WMT', 'COST', 'NKE', 'MCD', 'DIS', 'HD', 'TGT'],
                'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'OXY', 'BP', 'PSX', 'VLO', 'KMI'],
                'Industrials': ['GE', 'BA', 'HON', 'UPS', 'CAT', 'MMM', 'LMT', 'RTX', 'DE', 'GD'],
                'Communication Services': ['GOOGL', 'META', 'DIS', 'CMCSA', 'NFLX', 'VZ', 'T', 'TMUS', 'EA', 'ATVI'],
                'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'ED', 'PCG', 'XEL'],
                'Real Estate': ['AMT', 'CBRE', 'SPG', 'PLD', 'CCI', 'WELL', 'EQIX', 'PSA', 'AVB', 'O'],
                'Basic Materials': ['LIN', 'SHW', 'APD', 'FCX', 'NUE', 'ECL', 'DD', 'NEM', 'DOW', 'IP'],
                'Default': ['SPY', 'QQQ', 'DIA', 'IWM', 'VTI']
            }
            
            # Get peers list for the sector
            peers = sector_peers.get(sector, sector_peers['Default'])
            
            # Remove the company itself from the list
            if ticker in peers:
                peers.remove(ticker)
            
            # Limit to reasonable number of peers
            peers = peers[:8]
            
            # Initialize metrics collection
            all_metrics = {
                'pe_ratios': [],
                'ev_ebitda_multiples': [],
                'ev_revenue_multiples': [],
                'revenue_growth_rates': [],
                'ebitda_margins': [],
                'wacc_estimates': []
            }
            
            # Default WACC by sector
            wacc_by_sector = {
                'Technology': 0.10,
                'Healthcare': 0.09,
                'Financial Services': 0.08,
                'Consumer Goods': 0.07,
                'Energy': 0.10,
                'Industrials': 0.09,
                'Communication Services': 0.08,
                'Utilities': 0.06,
                'Real Estate': 0.07,
                'Basic Materials': 0.09,
                'Default': 0.09
            }
            
            # Default terminal growth by sector
            terminal_growth_by_sector = {
                'Technology': 0.03,
                'Healthcare': 0.025,
                'Financial Services': 0.02,
                'Consumer Goods': 0.02,
                'Energy': 0.015,
                'Industrials': 0.02,
                'Communication Services': 0.025,
                'Utilities': 0.015,
                'Real Estate': 0.018,
                'Basic Materials': 0.017,
                'Default': 0.025
            }
            
            # Collect metrics for each peer
            for peer in peers:
                try:
                    p = yf.Ticker(peer)
                    info = p.info
                    
                    # Get PE ratio
                    pe_ratio = info.get('trailingPE')
                    if pe_ratio and pe_ratio > 0 and pe_ratio < 100:  # Filter unreasonable values
                        all_metrics['pe_ratios'].append(pe_ratio)
                    
                    # Get EV/EBITDA
                    ev_ebitda = info.get('enterpriseToEbitda')
                    if ev_ebitda and ev_ebitda > 0 and ev_ebitda < 50:  # Filter unreasonable values
                        all_metrics['ev_ebitda_multiples'].append(ev_ebitda)
                    
                    # Get EV/Revenue
                    ev_revenue = info.get('enterpriseToRevenue')
                    if ev_revenue and ev_revenue > 0 and ev_revenue < 20:  # Filter unreasonable values
                        all_metrics['ev_revenue_multiples'].append(ev_revenue)
                    
                    # Revenue growth (estimate from earnings growth as proxy)
                    earnings_growth = info.get('earningsGrowth')
                    if earnings_growth and abs(earnings_growth) < 1.0:  # Reasonable growth rate
                        all_metrics['revenue_growth_rates'].append(earnings_growth)
                    
                    # Add standard WACC for the sector
                    all_metrics['wacc_estimates'].append(wacc_by_sector.get(sector, wacc_by_sector['Default']))
                    
                    # Calculate EBITDA margin if we have the data
                    try:
                        income_stmt = p.income_stmt
                        if not income_stmt.empty:
                            if 'EBITDA' in income_stmt.index and 'Total Revenue' in income_stmt.index:
                                ebitda = income_stmt.loc['EBITDA'].iloc[0]
                                revenue = income_stmt.loc['Total Revenue'].iloc[0]
                                if ebitda and revenue and revenue > 0:
                                    margin = ebitda / revenue
                                    if 0 < margin < 1:  # Reasonable margin
                                        all_metrics['ebitda_margins'].append(margin)
                    except:
                        # Skip if we can't get income statement
                        pass
                    
                    # Add a small delay to avoid API rate limits
                    time.sleep(0.2)
                    
                except Exception as e:
                    print(f"Error processing peer {peer}: {e}")
                    continue
            
            # Calculate averages
            sector_averages = {
                'revenue_growth': np.mean(all_metrics['revenue_growth_rates']) if all_metrics['revenue_growth_rates'] else wacc_by_sector.get(sector, 0.07),
                'ebitda_margin': np.mean(all_metrics['ebitda_margins']) if all_metrics['ebitda_margins'] else 0.20,
                'wacc': np.mean(all_metrics['wacc_estimates']) if all_metrics['wacc_estimates'] else wacc_by_sector.get(sector, 0.09),
                'terminal_growth': terminal_growth_by_sector.get(sector, 0.025),
                'ev_ebitda': np.mean(all_metrics['ev_ebitda_multiples']) if all_metrics['ev_ebitda_multiples'] else 12,
                'pe_ratio': np.mean(all_metrics['pe_ratios']) if all_metrics['pe_ratios'] else 18,
                'ev_revenue': np.mean(all_metrics['ev_revenue_multiples']) if all_metrics['ev_revenue_multiples'] else 3,
                'sector': sector,
                'peer_count': len(peers),
                'metrics_source': 'calculated_from_peers'
            }
            
            return sector_averages
            
        except Exception as e:
            print(f"Error calculating sector peer metrics: {e}")
            # Fall back to defaults
            return DataFetcher.get_industry_defaults(sector)

    @staticmethod
    def get_industry_defaults(industry):
        """Get default industry metrics when calculation isn't possible"""
        # Provide some default values for common industries
        industry_defaults = {
            'Technology': {
                'revenue_growth': 0.15,
                'ebitda_margin': 0.25,
                'wacc': 0.10,
                'terminal_growth': 0.03,
                'ev_ebitda': 15,
                'pe_ratio': 25,
                'ev_revenue': 5,
                'sector': 'Technology',
                'metrics_source': 'industry_defaults'
            },
            'Healthcare': {
                'revenue_growth': 0.10,
                'ebitda_margin': 0.20,
                'wacc': 0.09,
                'terminal_growth': 0.025,
                'ev_ebitda': 12,
                'pe_ratio': 20,
                'ev_revenue': 3,
                'sector': 'Healthcare',
                'metrics_source': 'industry_defaults'
            },
            'Financial Services': {
                'revenue_growth': 0.07,
                'ebitda_margin': 0.40,
                'wacc': 0.08,
                'terminal_growth': 0.02,
                'ev_ebitda': 10,
                'pe_ratio': 15,
                'ev_revenue': 2,
                'sector': 'Financial Services',
                'metrics_source': 'industry_defaults'
            },
            'Consumer Goods': {
                'revenue_growth': 0.05,
                'ebitda_margin': 0.15,
                'wacc': 0.07,
                'terminal_growth': 0.02,
                'ev_ebitda': 10,
                'pe_ratio': 18,
                'ev_revenue': 1.5,
                'sector': 'Consumer Goods',
                'metrics_source': 'industry_defaults'
            },
            'Energy': {
                'revenue_growth': 0.03,
                'ebitda_margin': 0.30,
                'wacc': 0.10,
                'terminal_growth': 0.015,
                'ev_ebitda': 8,
                'pe_ratio': 12,
                'ev_revenue': 1.2,
                'sector': 'Energy',
                'metrics_source': 'industry_defaults'
            },
            'Industrials': {
                'revenue_growth': 0.06,
                'ebitda_margin': 0.18,
                'wacc': 0.09,
                'terminal_growth': 0.02,
                'ev_ebitda': 11,
                'pe_ratio': 17,
                'ev_revenue': 1.8,
                'sector': 'Industrials',
                'metrics_source': 'industry_defaults'
            },
            'Communication Services': {
                'revenue_growth': 0.08,
                'ebitda_margin': 0.22,
                'wacc': 0.08,
                'terminal_growth': 0.025,
                'ev_ebitda': 10,
                'pe_ratio': 18,
                'ev_revenue': 3.5,
                'sector': 'Communication Services',
                'metrics_source': 'industry_defaults'
            },
            'Utilities': {
                'revenue_growth': 0.03,
                'ebitda_margin': 0.35,
                'wacc': 0.06,
                'terminal_growth': 0.015,
                'ev_ebitda': 9,
                'pe_ratio': 16,
                'ev_revenue': 2.5,
                'sector': 'Utilities',
                'metrics_source': 'industry_defaults'
            },
            'Real Estate': {
                'revenue_growth': 0.04,
                'ebitda_margin': 0.55,
                'wacc': 0.07,
                'terminal_growth': 0.018,
                'ev_ebitda': 14,
                'pe_ratio': 20,
                'ev_revenue': 7,
                'sector': 'Real Estate',
                'metrics_source': 'industry_defaults'
            },
            'Basic Materials': {
                'revenue_growth': 0.05,
                'ebitda_margin': 0.20,
                'wacc': 0.09,
                'terminal_growth': 0.017,
                'ev_ebitda': 9,
                'pe_ratio': 14,
                'ev_revenue': 1.5,
                'sector': 'Basic Materials',
                'metrics_source': 'industry_defaults'
            },
            'Default': {
                'revenue_growth': 0.07,
                'ebitda_margin': 0.20,
                'wacc': 0.09,
                'terminal_growth': 0.025,
                'ev_ebitda': 10,
                'pe_ratio': 15,
                'ev_revenue': 2,
                'sector': 'General Market',
                'metrics_source': 'industry_defaults'
            }
        }
        
        # Add index membership as unknown
        result = industry_defaults.get(industry, industry_defaults['Default'])
        result['index_membership'] = {
            'sp500': False  # Default to false for industry-based lookups
        }
        
        return result
    
    @staticmethod
    def get_comparable_companies(ticker, industry):
        """
        Fetch list of comparable companies based on ticker and industry
        
        Args:
            ticker (str): Company ticker symbol
            industry (str): Industry name
            
        Returns:
            list: List of comparable companies with metrics
        """
        try:
            # In a real app, this would search for companies in the same industry
            # For this demo, we'll return a simplified list based on industry
            industry_peers = {
                'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN'],
                'Healthcare': ['JNJ', 'PFE', 'MRK', 'UNH', 'ABT'],
                'Financial Services': ['JPM', 'BAC', 'GS', 'MS', 'WFC'],
                'Consumer Goods': ['PG', 'KO', 'PEP', 'WMT', 'COST'],
                'Energy': ['XOM', 'CVX', 'BP', 'SHEL', 'COP'],
                'Default': ['SPY', 'QQQ', 'DIA', 'IWM', 'VTI'],
            }
            
            peers = industry_peers.get(industry, industry_peers['Default'])
            # Remove the ticker itself from peers if present
            if ticker in peers:
                peers.remove(ticker)
            
            peer_data = []
            for peer in peers[:3]:  # Limit to 3 peers for simplicity
                try:
                    company = yf.Ticker(peer)
                    info = company.info
                    
                    # Get key metrics
                    peer_info = {
                        'ticker': peer,
                        'name': info.get('longName', peer),
                        'marketCap': info.get('marketCap', 'N/A'),
                        'ev_ebitda': info.get('enterpriseToEbitda', 'N/A'),
                        'pe_ratio': info.get('trailingPE', 'N/A'),
                        'ev_revenue': info.get('enterpriseToRevenue', 'N/A'),
                    }
                    
                    peer_data.append(peer_info)
                    time.sleep(0.5)  # To avoid API rate limits
                    
                except Exception as e:
                    print(f"Error fetching peer {peer}: {e}")
                    continue
            
            return peer_data
            
        except Exception as e:
            print(f"Error fetching comparable companies: {e}")
            return []
    
    @staticmethod
    def get_precedent_transactions(industry):
        """
        Fetch recent M&A transactions in the industry
        
        Args:
            industry (str): Industry name
            
        Returns:
            list: List of precedent transactions
        """
        # In a real app, this would fetch from a database or API
        # Here we provide sample transactions for common industries
        sample_transactions = {
            'Technology': [
                {'target': 'Activision Blizzard', 'acquirer': 'Microsoft', 'date': '2022-01-18', 'value': 68.7, 'ev_ebitda': 28.0, 'ev_revenue': 7.5},
                {'target': 'VMware', 'acquirer': 'Broadcom', 'date': '2022-05-26', 'value': 61.0, 'ev_ebitda': 18.5, 'ev_revenue': 5.9},
                {'target': 'Twitter', 'acquirer': 'Elon Musk', 'date': '2022-10-27', 'value': 44.0, 'ev_ebitda': 42.0, 'ev_revenue': 8.2},
            ],
            'Healthcare': [
                {'target': 'Allergan', 'acquirer': 'AbbVie', 'date': '2020-05-08', 'value': 63.0, 'ev_ebitda': 15.8, 'ev_revenue': 6.5},
                {'target': 'Alexion', 'acquirer': 'AstraZeneca', 'date': '2021-07-21', 'value': 39.0, 'ev_ebitda': 16.2, 'ev_revenue': 7.1},
                {'target': 'Pfizer Consumer Health', 'acquirer': 'GSK', 'date': '2019-08-01', 'value': 12.7, 'ev_ebitda': 17.5, 'ev_revenue': 3.2},
            ],
            'Financial Services': [
                {'target': 'E*TRADE', 'acquirer': 'Morgan Stanley', 'date': '2020-10-02', 'value': 13.0, 'ev_ebitda': 11.0, 'ev_revenue': 3.8},
                {'target': 'TD Ameritrade', 'acquirer': 'Charles Schwab', 'date': '2020-10-06', 'value': 22.0, 'ev_ebitda': 10.5, 'ev_revenue': 4.1},
                {'target': 'Credit Karma', 'acquirer': 'Intuit', 'date': '2020-12-03', 'value': 7.1, 'ev_ebitda': 23.0, 'ev_revenue': 7.2},
            ],
            'Default': [
                {'target': 'Sample Target A', 'acquirer': 'Sample Acquirer X', 'date': '2022-01-01', 'value': 10.0, 'ev_ebitda': 12.0, 'ev_revenue': 3.0},
                {'target': 'Sample Target B', 'acquirer': 'Sample Acquirer Y', 'date': '2021-06-15', 'value': 5.0, 'ev_ebitda': 10.0, 'ev_revenue': 2.5},
                {'target': 'Sample Target C', 'acquirer': 'Sample Acquirer Z', 'date': '2020-11-30', 'value': 8.0, 'ev_ebitda': 11.0, 'ev_revenue': 2.8},
            ],
        }
        
        return sample_transactions.get(industry, sample_transactions['Default'])
    
    @staticmethod
    def get_esg_metrics(ticker):
        """
        Fetch ESG metrics for a company
        
        Args:
            ticker (str): Company ticker symbol
            
        Returns:
            dict: ESG metrics
        """
        try:
            company = yf.Ticker(ticker)
            info = company.info
            
            # Extract ESG data if available
            esg_data = {
                'esgScore': info.get('esgScore', 'N/A'),
                'environmentalScore': info.get('environmentalScore', 'N/A'),
                'socialScore': info.get('socialScore', 'N/A'),
                'governanceScore': info.get('governanceScore', 'N/A'),
            }
            
            return esg_data
            
        except Exception as e:
            print(f"Error fetching ESG metrics: {e}")
            return {
                'esgScore': 'N/A',
                'environmentalScore': 'N/A',
                'socialScore': 'N/A',
                'governanceScore': 'N/A',
            }
