import numpy as np
import pandas as pd
from datetime import datetime

class AssetBasedModel:
    """
    Asset-Based valuation model
    
    This model values a company based on the value of its assets minus liabilities,
    with optional adjustments to asset values.
    """
    
    def __init__(self, financial_data, asset_discount=0.0):
        """
        Initialize the Asset-Based model with required parameters
        
        Args:
            financial_data (dict): Financial data for the subject company
            asset_discount (float): Discount to apply to asset values (0-1)
        """
        self.financial_data = financial_data
        self.asset_discount = asset_discount
    
    def run_valuation(self):
        """
        Run the asset-based valuation
        
        Returns:
            dict: Valuation results
        """
        # Get total assets and liabilities
        total_assets = self._get_total_assets()
        total_liabilities = self._get_total_liabilities()
        
        if total_assets is None:
            # If no asset data, use equity and liabilities to back-calculate
            equity = self._get_equity()
            if equity is not None and total_liabilities is not None:
                total_assets = equity + total_liabilities
        
        if total_liabilities is None:
            # If no liability data, use assets and equity to back-calculate
            equity = self._get_equity()
            if equity is not None and total_assets is not None:
                total_liabilities = total_assets - equity
        
        # If still missing data, use default values
        if total_assets is None:
            total_assets = 1000000  # Default $1M assets
        
        if total_liabilities is None:
            total_liabilities = total_assets * 0.6  # Default 60% liability-to-asset ratio
        
        # Calculate book value of equity
        book_equity = total_assets - total_liabilities
        
        # Apply asset discount if specified
        adjusted_assets = total_assets * (1 - self.asset_discount)
        
        # Calculate adjusted equity value
        adjusted_equity = adjusted_assets - total_liabilities
        
        # Return valuation results
        return {
            'enterprise_value': adjusted_assets,  # Enterprise value = adjusted assets
            'equity_value': adjusted_equity,      # Equity value = adjusted assets - liabilities
            'method': 'Asset-Based Valuation',
            'asset_details': {
                'total_assets': total_assets,
                'total_liabilities': total_liabilities,
                'book_equity': book_equity,
                'asset_discount': self.asset_discount,
                'adjusted_assets': adjusted_assets,
                'adjusted_equity': adjusted_equity
            }
        }
    
    def _get_total_assets(self):
        """
        Get the most recent total assets value
        
        Returns:
            float: Total assets or None if not available
        """
        if 'total_assets' in self.financial_data and self.financial_data['total_assets']:
            # Get the most recent total assets value
            return list(self.financial_data['total_assets'].values())[0]
        return None
    
    def _get_total_liabilities(self):
        """
        Get the most recent total liabilities value
        
        Returns:
            float: Total liabilities or None if not available
        """
        # If total liabilities is directly available
        if 'total_liabilities' in self.financial_data and self.financial_data['total_liabilities']:
            return list(self.financial_data['total_liabilities'].values())[0]
        
        # Otherwise, try to calculate from debt
        if 'total_debt' in self.financial_data and self.financial_data['total_debt']:
            debt = list(self.financial_data['total_debt'].values())[0]
            # Estimate total liabilities as 1.5x debt (including non-debt liabilities)
            return debt * 1.5
        
        return None
    
    def _get_equity(self):
        """
        Get the most recent equity value
        
        Returns:
            float: Equity or None if not available
        """
        if 'equity' in self.financial_data and self.financial_data['equity']:
            # Get the most recent equity value
            return list(self.financial_data['equity'].values())[0]
        return None

