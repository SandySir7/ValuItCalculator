import numpy as np
import pandas as pd
from datetime import datetime

class DCFModel:
    """
    Discounted Cash Flow (DCF) valuation model
    
    This model values a company by projecting future free cash flows and
    discounting them back to present value using WACC.
    """
    
    def __init__(self, financial_data, growth_rate, wacc, terminal_growth_rate, forecast_years):
        """
        Initialize the DCF model with required parameters
        
        Args:
            financial_data (dict): Historical financial data
            growth_rate (float): Annual growth rate for projections
            wacc (float): Weighted Average Cost of Capital (discount rate)
            terminal_growth_rate (float): Long-term growth rate for terminal value
            forecast_years (int): Number of years to forecast
        """
        self.financial_data = financial_data
        self.growth_rate = growth_rate
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        self.forecast_years = forecast_years
    
    def run_valuation(self):
        """
        Run the DCF valuation
        
        Returns:
            dict: Valuation results
        """
        # Get the base year financial metrics
        base_fcf = self._get_base_fcf()
        
        # When no FCF data is available, estimate from EBITDA
        if base_fcf is None:
            base_ebitda = self._get_base_ebitda()
            # If EBITDA is available, estimate FCF as 60% of EBITDA (simplified assumption)
            if base_ebitda is not None:
                base_fcf = base_ebitda * 0.6
            else:
                # If no EBITDA, try to estimate from revenue
                base_revenue = self._get_base_revenue()
                if base_revenue is not None:
                    # Estimate EBITDA margin based on industry or default to 20%
                    ebitda_margin = 0.20  # Default EBITDA margin
                    base_ebitda = base_revenue * ebitda_margin
                    base_fcf = base_ebitda * 0.6
                else:
                    # If no data available, use a default value
                    base_fcf = 1000000  # Default $1M FCF
        
        # Project free cash flows
        fcf_forecast = self._project_fcf(base_fcf)
        
        # Calculate present values
        present_values = self._calculate_present_values(fcf_forecast)
        
        # Calculate terminal value
        terminal_value = self._calculate_terminal_value(fcf_forecast[-1])
        
        # Discount terminal value to present
        pv_terminal_value = terminal_value / ((1 + self.wacc) ** self.forecast_years)
        
        # Calculate enterprise value
        enterprise_value = sum(present_values) + pv_terminal_value
        
        # Get debt and cash from financial data
        debt = self._get_total_debt()
        cash = self._get_cash()
        
        # Calculate equity value
        equity_value = enterprise_value - debt + cash
        
        # Create sensitivity analysis
        sensitivity_analysis = self._create_sensitivity_analysis(base_fcf)
        
        # Return valuation results
        return {
            'enterprise_value': enterprise_value,
            'equity_value': equity_value,
            'method': 'DCF',
            'dcf_details': {
                'base_fcf': base_fcf,
                'fcf_forecast': fcf_forecast,
                'present_values': present_values,
                'terminal_value': terminal_value,
                'pv_terminal_value': pv_terminal_value,
                'debt': debt,
                'cash': cash,
                'sensitivity_analysis': sensitivity_analysis
            }
        }
    
    def _get_base_fcf(self):
        """
        Get the base year free cash flow
        
        Returns:
            float: Base year FCF or None if not available
        """
        if 'fcf' in self.financial_data and self.financial_data['fcf']:
            # Get the most recent FCF value
            return list(self.financial_data['fcf'].values())[0]
        return None
    
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
    
    def _get_total_debt(self):
        """
        Get the total debt
        
        Returns:
            float: Total debt or 0 if not available
        """
        if 'total_debt' in self.financial_data and self.financial_data['total_debt']:
            # Get the most recent debt value
            return list(self.financial_data['total_debt'].values())[0]
        return 0
    
    def _get_cash(self):
        """
        Get the cash and equivalents
        
        Returns:
            float: Cash or 0 if not available
        """
        if 'cash' in self.financial_data and self.financial_data['cash']:
            # Get the most recent cash value
            return list(self.financial_data['cash'].values())[0]
        return 0
    
    def _project_fcf(self, base_fcf):
        """
        Project future free cash flows
        
        Args:
            base_fcf (float): Base year free cash flow
            
        Returns:
            list: Projected free cash flows
        """
        fcf_forecast = []
        current_fcf = base_fcf
        
        for _ in range(self.forecast_years):
            # Grow FCF by the growth rate
            current_fcf = current_fcf * (1 + self.growth_rate)
            fcf_forecast.append(current_fcf)
        
        return fcf_forecast
    
    def _calculate_present_values(self, fcf_forecast):
        """
        Calculate present values of projected free cash flows
        
        Args:
            fcf_forecast (list): Projected free cash flows
            
        Returns:
            list: Present values of projected free cash flows
        """
        present_values = []
        
        for i, fcf in enumerate(fcf_forecast):
            # Discount FCF to present value
            present_value = fcf / ((1 + self.wacc) ** (i + 1))
            present_values.append(present_value)
        
        return present_values
    
    def _calculate_terminal_value(self, final_fcf):
        """
        Calculate terminal value using perpetuity growth model
        
        Args:
            final_fcf (float): Final year projected free cash flow
            
        Returns:
            float: Terminal value
        """
        # Gordon Growth Model
        return final_fcf * (1 + self.terminal_growth_rate) / (self.wacc - self.terminal_growth_rate)
    
    def _create_sensitivity_analysis(self, base_fcf):
        """
        Create sensitivity analysis for different WACC and terminal growth rates
        
        Args:
            base_fcf (float): Base year free cash flow
            
        Returns:
            dict: Sensitivity analysis results
        """
        # Create ranges for WACC and terminal growth rate
        wacc_values = [self.wacc - 0.02, self.wacc - 0.01, self.wacc, self.wacc + 0.01, self.wacc + 0.02]
        growth_values = [self.terminal_growth_rate - 0.01, self.terminal_growth_rate - 0.005, 
                         self.terminal_growth_rate, self.terminal_growth_rate + 0.005, self.terminal_growth_rate + 0.01]
        
        # Create enterprise value matrix
        ev_matrix = []
        
        for w in wacc_values:
            ev_row = []
            
            for g in growth_values:
                # Recalculate with different WACC and growth rates
                fcf_forecast = self._project_fcf(base_fcf)
                present_values = []
                
                for i, fcf in enumerate(fcf_forecast):
                    present_value = fcf / ((1 + w) ** (i + 1))
                    present_values.append(present_value)
                
                terminal_value = fcf_forecast[-1] * (1 + g) / (w - g)
                pv_terminal_value = terminal_value / ((1 + w) ** self.forecast_years)
                
                enterprise_value = sum(present_values) + pv_terminal_value
                ev_row.append(enterprise_value)
            
            ev_matrix.append(ev_row)
        
        return {
            'wacc_values': wacc_values,
            'growth_values': growth_values,
            'ev_matrix': ev_matrix
        }

