import numpy as np
import pandas as pd
from datetime import datetime

from utils.data_fetcher import DataFetcher

class PrecedentTransactionsModel:
    """
    Precedent Transactions valuation model
    
    This model values a company by applying multiples from comparable M&A transactions
    to the subject company's financial metrics.
    """
    
    def __init__(self, financial_data, industry, ev_ebitda_multiple, ev_revenue_multiple):
        """
        Initialize the Precedent Transactions model with required parameters
        
        Args:
            financial_data (dict): Financial data for the subject company
            industry (str): Industry of the subject company
            ev_ebitda_multiple (float): EV/EBITDA multiple to apply
            ev_revenue_multiple (float): EV/Revenue multiple to apply
        """
        self.financial_data = financial_data
        self.industry = industry
        self.ev_ebitda_multiple = ev_ebitda_multiple
        self.ev_revenue_multiple = ev_revenue_multiple
    
    def run_valuation(self):
        """
        Run the precedent transactions valuation
        
        Returns:
            dict: Valuation results
        """
        # Get the latest financial metrics
        ebitda = self._get_ebitda()
        revenue = self._get_revenue()
        debt = self._get_debt()
        cash = self._get_cash()
        
        # Calculate enterprise value using multiples
        ev_ebitda_valuation = ebitda * self.ev_ebitda_multiple if ebitda is not None else None
        ev_revenue_valuation = revenue * self.ev_revenue_multiple if revenue is not None else None
        
        # Calculate equity values
        eq_ebitda_valuation = ev_ebitda_valuation - debt + cash if ev_ebitda_valuation is not None else None
        eq_revenue_valuation = ev_revenue_valuation - debt + cash if ev_revenue_valuation is not None else None
        
        # Get precedent transactions
        transactions = self._get_precedent_transactions()
        
        # Determine the primary enterprise value (prioritize EV/EBITDA if available)
        if ev_ebitda_valuation is not None:
            primary_ev = ev_ebitda_valuation
            primary_equity = eq_ebitda_valuation
            primary_method = "EV/EBITDA"
        elif ev_revenue_valuation is not None:
            primary_ev = ev_revenue_valuation
            primary_equity = eq_revenue_valuation
            primary_method = "EV/Revenue"
        else:
            # If no metrics available, use default values
            primary_ev = 0
            primary_equity = 0
            primary_method = "N/A"
        
        # Return valuation results
        return {
            'enterprise_value': primary_ev,
            'equity_value': primary_equity,
            'method': 'Precedent Transactions',
            'primary_method': primary_method,
            'transactions_details': {
                'ebitda': ebitda,
                'revenue': revenue,
                'debt': debt,
                'cash': cash,
                'ev_ebitda_valuation': ev_ebitda_valuation,
                'ev_revenue_valuation': ev_revenue_valuation,
                'transactions': transactions
            }
        }
    
    def _get_ebitda(self):
        """
        Get the most recent EBITDA value
        
        Returns:
            float: EBITDA or None if not available
        """
        if 'ebitda' in self.financial_data and self.financial_data['ebitda']:
            # Get the most recent EBITDA value
            return list(self.financial_data['ebitda'].values())[0]
        return None
    
    def _get_revenue(self):
        """
        Get the most recent revenue value
        
        Returns:
            float: Revenue or None if not available
        """
        if 'revenue' in self.financial_data and self.financial_data['revenue']:
            # Get the most recent revenue value
            return list(self.financial_data['revenue'].values())[0]
        return None
    
    def _get_debt(self):
        """
        Get the most recent debt value
        
        Returns:
            float: Debt or 0 if not available
        """
        if 'total_debt' in self.financial_data and self.financial_data['total_debt']:
            # Get the most recent debt value
            return list(self.financial_data['total_debt'].values())[0]
        return 0
    
    def _get_cash(self):
        """
        Get the most recent cash value
        
        Returns:
            float: Cash or 0 if not available
        """
        if 'cash' in self.financial_data and self.financial_data['cash']:
            # Get the most recent cash value
            return list(self.financial_data['cash'].values())[0]
        return 0
    
    def _get_precedent_transactions(self):
        """
        Get precedent transactions data
        
        Returns:
            list: List of precedent transactions with key metrics
        """
        try:
            transactions = DataFetcher.get_precedent_transactions(self.industry)
            return transactions
        except Exception as e:
            print(f"Error fetching precedent transactions: {e}")
            return []

