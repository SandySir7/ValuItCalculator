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
    def get_industry_averages(industry):
        """
        Fetch industry average metrics
        
        Args:
            industry (str): Industry name
            
        Returns:
            dict: Industry average metrics
        """
        # In a real application, this would fetch from a database or API
        # Here we provide some default values for common industries
        industry_defaults = {
            'Technology': {
                'revenue_growth': 0.15,
                'ebitda_margin': 0.25,
                'wacc': 0.10,
                'terminal_growth': 0.03,
                'ev_ebitda': 15,
                'pe_ratio': 25,
                'ev_revenue': 5,
            },
            'Healthcare': {
                'revenue_growth': 0.10,
                'ebitda_margin': 0.20,
                'wacc': 0.09,
                'terminal_growth': 0.025,
                'ev_ebitda': 12,
                'pe_ratio': 20,
                'ev_revenue': 3,
            },
            'Financial Services': {
                'revenue_growth': 0.07,
                'ebitda_margin': 0.40,
                'wacc': 0.08,
                'terminal_growth': 0.02,
                'ev_ebitda': 10,
                'pe_ratio': 15,
                'ev_revenue': 2,
            },
            'Consumer Goods': {
                'revenue_growth': 0.05,
                'ebitda_margin': 0.15,
                'wacc': 0.07,
                'terminal_growth': 0.02,
                'ev_ebitda': 10,
                'pe_ratio': 18,
                'ev_revenue': 1.5,
            },
            'Energy': {
                'revenue_growth': 0.03,
                'ebitda_margin': 0.30,
                'wacc': 0.10,
                'terminal_growth': 0.015,
                'ev_ebitda': 8,
                'pe_ratio': 12,
                'ev_revenue': 1.2,
            },
            'Default': {
                'revenue_growth': 0.07,
                'ebitda_margin': 0.20,
                'wacc': 0.09,
                'terminal_growth': 0.025,
                'ev_ebitda': 10,
                'pe_ratio': 15,
                'ev_revenue': 2,
            }
        }
        
        # Return default if industry not found
        return industry_defaults.get(industry, industry_defaults['Default'])
    
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
