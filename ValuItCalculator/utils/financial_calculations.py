import numpy as np
import pandas as pd

class FinancialCalculations:
    """
    Utility class for financial calculations used in valuation models
    """
    
    @staticmethod
    def calculate_wacc(risk_free_rate, market_risk_premium, beta, cost_of_debt, tax_rate, debt_weight, equity_weight):
        """
        Calculate Weighted Average Cost of Capital (WACC)
        
        Args:
            risk_free_rate (float): Risk-free rate (e.g., 10-year Treasury yield)
            market_risk_premium (float): Market risk premium
            beta (float): Company's beta (measure of volatility)
            cost_of_debt (float): Company's cost of debt
            tax_rate (float): Corporate tax rate
            debt_weight (float): Proportion of debt in capital structure
            equity_weight (float): Proportion of equity in capital structure
            
        Returns:
            float: WACC as a decimal
        """
        # Cost of equity using CAPM (Capital Asset Pricing Model)
        cost_of_equity = risk_free_rate + beta * market_risk_premium
        
        # WACC formula
        wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
        
        return wacc
    
    @staticmethod
    def calculate_terminal_value(final_fcf, growth_rate, discount_rate, method='perpetuity'):
        """
        Calculate terminal value
        
        Args:
            final_fcf (float): Final year free cash flow
            growth_rate (float): Perpetual growth rate
            discount_rate (float): Discount rate (WACC)
            method (str): Method to use ('perpetuity' or 'exit_multiple')
            
        Returns:
            float: Terminal value
        """
        if method == 'perpetuity':
            # Gordon Growth Model
            terminal_value = final_fcf * (1 + growth_rate) / (discount_rate - growth_rate)
        elif method == 'exit_multiple':
            # Using a default multiple of 10x for final year FCF
            terminal_value = final_fcf * 10
        else:
            raise ValueError("Method must be 'perpetuity' or 'exit_multiple'")
        
        return terminal_value
    
    @staticmethod
    def discount_cash_flows(cash_flows, discount_rate, years=None):
        """
        Discount cash flows to present value
        
        Args:
            cash_flows (list): List of cash flows
            discount_rate (float): Discount rate (WACC)
            years (list, optional): List of years corresponding to cash flows
            
        Returns:
            list: Present values of cash flows
        """
        if years is None:
            years = list(range(1, len(cash_flows) + 1))
        
        present_values = []
        for cf, year in zip(cash_flows, years):
            pv = cf / ((1 + discount_rate) ** year)
            present_values.append(pv)
        
        return present_values
    
    @staticmethod
    def calculate_enterprise_value(pv_fcf, terminal_value, final_year=5):
        """
        Calculate enterprise value
        
        Args:
            pv_fcf (list): Present values of free cash flows
            terminal_value (float): Terminal value
            final_year (int): Final forecast year
            
        Returns:
            float: Enterprise value
        """
        # Discount terminal value to present
        discounted_terminal_value = terminal_value / ((1 + discount_rate) ** final_year)
        
        # Enterprise value is sum of PV of FCFs and discounted terminal value
        enterprise_value = sum(pv_fcf) + discounted_terminal_value
        
        return enterprise_value
    
    @staticmethod
    def calculate_equity_value(enterprise_value, debt, cash):
        """
        Calculate equity value
        
        Args:
            enterprise_value (float): Enterprise value
            debt (float): Total debt
            cash (float): Cash and cash equivalents
            
        Returns:
            float: Equity value
        """
        equity_value = enterprise_value - debt + cash
        return equity_value
    
    @staticmethod
    def calculate_share_price(equity_value, shares_outstanding):
        """
        Calculate share price
        
        Args:
            equity_value (float): Equity value
            shares_outstanding (float): Number of shares outstanding
            
        Returns:
            float: Share price
        """
        share_price = equity_value / shares_outstanding
        return share_price
    
    @staticmethod
    def calculate_growth_rates(values):
        """
        Calculate year-over-year growth rates
        
        Args:
            values (list): List of values
            
        Returns:
            list: Growth rates
        """
        growth_rates = []
        for i in range(1, len(values)):
            if values[i-1] != 0:
                growth_rate = (values[i] - values[i-1]) / values[i-1]
            else:
                growth_rate = 0
            growth_rates.append(growth_rate)
        
        return growth_rates
    
    @staticmethod
    def calculate_margins(numerator, denominator):
        """
        Calculate margins
        
        Args:
            numerator (list): Numerator values (e.g., EBITDA)
            denominator (list): Denominator values (e.g., Revenue)
            
        Returns:
            list: Margins
        """
        margins = []
        for n, d in zip(numerator, denominator):
            if d != 0:
                margin = n / d
            else:
                margin = 0
            margins.append(margin)
        
        return margins
    
    @staticmethod
    def calculate_enterprise_value_multiples(enterprise_value, metrics):
        """
        Calculate enterprise value multiples
        
        Args:
            enterprise_value (float): Enterprise value
            metrics (dict): Financial metrics (e.g., revenue, ebitda)
            
        Returns:
            dict: EV multiples
        """
        multiples = {}
        
        for key, value in metrics.items():
            if value and value != 0:
                multiples[f'ev_{key}'] = enterprise_value / value
            else:
                multiples[f'ev_{key}'] = 'N/A'
        
        return multiples
