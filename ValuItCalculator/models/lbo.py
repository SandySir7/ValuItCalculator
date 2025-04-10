import numpy as np
import pandas as pd
from datetime import datetime

class LBOModel:
    """
    Leveraged Buyout (LBO) valuation model
    
    This model estimates the potential equity value and returns for a leveraged buyout
    transaction based on purchase price, exit value, and debt structure.
    """
    
    def __init__(self, financial_data, exit_year, exit_multiple, target_irr):
        """
        Initialize the LBO model with required parameters
        
        Args:
            financial_data (dict): Financial data for the subject company
            exit_year (int): Year of LBO exit
            exit_multiple (float): EV/EBITDA multiple at exit
            target_irr (float): Target Internal Rate of Return
        """
        self.financial_data = financial_data
        self.exit_year = exit_year
        self.exit_multiple = exit_multiple
        self.target_irr = target_irr
    
    def run_valuation(self):
        """
        Run the LBO valuation
        
        Returns:
            dict: Valuation results
        """
        # Get the base financial metrics
        base_ebitda = self._get_base_ebitda()
        base_revenue = self._get_base_revenue()
        current_debt = self._get_debt()
        current_cash = self._get_cash()
        
        # Use default value if EBITDA not available
        if base_ebitda is None:
            if base_revenue is not None:
                # Estimate EBITDA from revenue (assuming 20% EBITDA margin)
                base_ebitda = base_revenue * 0.2
            else:
                # Default value if no data available
                base_ebitda = 100000000  # $100M EBITDA
        
        # Calculate entry multiple based on target IRR
        entry_multiple = self._calculate_entry_multiple(base_ebitda)
        
        # Calculate purchase price
        purchase_price = entry_multiple * base_ebitda
        
        # Assume standard LBO capital structure (70% debt, 30% equity)
        debt_percent = 0.7
        equity_percent = 0.3
        
        # Calculate debt and equity components
        new_debt = purchase_price * debt_percent
        new_equity = purchase_price * equity_percent
        
        # Project EBITDA growth
        ebitda_projection = self._project_ebitda(base_ebitda)
        
        # Calculate exit value
        exit_ebitda = ebitda_projection[-1]
        exit_value = exit_ebitda * self.exit_multiple
        
        # Assume debt is paid down linearly
        annual_debt_payment = new_debt / self.exit_year
        exit_debt = new_debt - (annual_debt_payment * self.exit_year)
        
        # Exit equity value
        exit_equity = exit_value - exit_debt
        
        # Calculate returns
        equity_multiple = exit_equity / new_equity
        # Actual IRR calculation would be more complex in a real model
        irr = (equity_multiple ** (1 / self.exit_year)) - 1
        
        # Calculate maximum supportable debt
        max_debt = self._calculate_max_debt(base_ebitda)
        
        # IRR sensitivity to entry multiple
        irr_sensitivity = self._calculate_irr_sensitivity(base_ebitda)
        
        # Return valuation results
        return {
            'enterprise_value': purchase_price,
            'equity_value': new_equity,
            'method': 'LBO',
            'lbo_details': {
                'base_ebitda': base_ebitda,
                'entry_multiple': entry_multiple,
                'purchase_price': purchase_price,
                'new_debt': new_debt,
                'new_equity': new_equity,
                'ebitda_projection': ebitda_projection,
                'exit_ebitda': exit_ebitda,
                'exit_value': exit_value,
                'exit_debt': exit_debt,
                'exit_equity': exit_equity,
                'equity_multiple': equity_multiple,
                'irr': irr,
                'max_debt': max_debt,
                'irr_sensitivity': irr_sensitivity
            }
        }
    
    def _get_base_ebitda(self):
        """
        Get the base year EBITDA
        
        Returns:
            float: Base year EBITDA or None if not available
        """
        if 'ebitda' in self.financial_data and self.financial_data['ebitda']:
            # Get the most recent EBITDA value
            return list(self.financial_data['ebitda'].values())[0]
        return None
    
    def _get_base_revenue(self):
        """
        Get the base year revenue
        
        Returns:
            float: Base year revenue or None if not available
        """
        if 'revenue' in self.financial_data and self.financial_data['revenue']:
            # Get the most recent revenue value
            return list(self.financial_data['revenue'].values())[0]
        return None
    
    def _get_debt(self):
        """
        Get the current debt
        
        Returns:
            float: Current debt or 0 if not available
        """
        if 'total_debt' in self.financial_data and self.financial_data['total_debt']:
            # Get the most recent debt value
            return list(self.financial_data['total_debt'].values())[0]
        return 0
    
    def _get_cash(self):
        """
        Get the current cash
        
        Returns:
            float: Current cash or 0 if not available
        """
        if 'cash' in self.financial_data and self.financial_data['cash']:
            # Get the most recent cash value
            return list(self.financial_data['cash'].values())[0]
        return 0
    
    def _calculate_entry_multiple(self, base_ebitda):
        """
        Calculate entry multiple based on target IRR
        
        Args:
            base_ebitda (float): Base year EBITDA
            
        Returns:
            float: Entry multiple
        """
        # Start with typical LBO multiple range of 6-8x
        # Adjust based on target IRR (higher IRR -> lower entry multiple)
        if self.target_irr > 0.25:
            return 6.0
        elif self.target_irr > 0.20:
            return 7.0
        elif self.target_irr > 0.15:
            return 8.0
        else:
            return 9.0
    
    def _project_ebitda(self, base_ebitda):
        """
        Project EBITDA growth for the holding period
        
        Args:
            base_ebitda (float): Base year EBITDA
            
        Returns:
            list: Projected EBITDA values
        """
        ebitda_projection = []
        current_ebitda = base_ebitda
        
        # Assume standard growth rates for LBO:
        # - Years 1-2: Higher growth from operational improvements (10%)
        # - Years 3+: Moderate growth (5%)
        for year in range(1, self.exit_year + 1):
            if year <= 2:
                growth_rate = 0.10
            else:
                growth_rate = 0.05
            
            current_ebitda = current_ebitda * (1 + growth_rate)
            ebitda_projection.append(current_ebitda)
        
        return ebitda_projection
    
    def _calculate_max_debt(self, base_ebitda):
        """
        Calculate maximum supportable debt
        
        Args:
            base_ebitda (float): Base year EBITDA
            
        Returns:
            float: Maximum supportable debt
        """
        # Typical debt multiples for LBOs range from 4-6x EBITDA
        # Use 5x as a standard multiple
        debt_multiple = 5.0
        
        return base_ebitda * debt_multiple
    
    def _calculate_irr_sensitivity(self, base_ebitda):
        """
        Calculate IRR sensitivity to entry multiples
        
        Args:
            base_ebitda (float): Base year EBITDA
            
        Returns:
            dict: IRR sensitivity analysis
        """
        # Create a range of entry multiples to test
        entry_multiples = [5.0, 6.0, 7.0, 8.0, 9.0]
        
        # Calculate IRR for each entry multiple
        irr_values = []
        
        for multiple in entry_multiples:
            # Calculate purchase price
            purchase_price = multiple * base_ebitda
            
            # Assume standard LBO capital structure (70% debt, 30% equity)
            new_equity = purchase_price * 0.3
            
            # Project EBITDA growth
            ebitda_projection = self._project_ebitda(base_ebitda)
            
            # Calculate exit value
            exit_ebitda = ebitda_projection[-1]
            exit_value = exit_ebitda * self.exit_multiple
            
            # Assume debt is paid down linearly
            new_debt = purchase_price * 0.7
            annual_debt_payment = new_debt / self.exit_year
            exit_debt = new_debt - (annual_debt_payment * self.exit_year)
            
            # Exit equity value
            exit_equity = exit_value - exit_debt
            
            # Calculate equity multiple and IRR
            equity_multiple = exit_equity / new_equity
            irr = (equity_multiple ** (1 / self.exit_year)) - 1
            
            irr_values.append(irr)
        
        return {
            'entry_multiples': entry_multiples,
            'irr_values': irr_values
        }
