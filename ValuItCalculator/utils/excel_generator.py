import pandas as pd
import io

class ExcelGenerator:
    """
    Utility class for generating Excel reports for valuations
    """
    
    @staticmethod
    def generate_valuation_excel(valuation_data, company_info, filename="valuation_report.xlsx"):
        """
        Generate an Excel report for a valuation
        
        Args:
            valuation_data (dict): Valuation data including results
            company_info (dict): Company information
            filename (str): Output filename
            
        Returns:
            bytes: Excel file as bytes
        """
        buffer = io.BytesIO()
        
        # Create a Pandas Excel writer
        writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
        
        # Get the workbook and worksheet objects
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#0066CC',
            'font_color': 'white',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'border': 1
        })
        
        percent_format = workbook.add_format({
            'border': 1,
            'num_format': '0.00%'
        })
        
        currency_format = workbook.add_format({
            'border': 1,
            'num_format': '$#,##0.00'
        })
        
        currency_millions_format = workbook.add_format({
            'border': 1,
            'num_format': '$#,##0.00,,"M"'
        })
        
        # Create summary sheet
        summary_df = pd.DataFrame({
            'Parameter': ['Company', 'Ticker', 'Industry', 'Sector', 'Valuation Method', 
                         'Enterprise Value', 'Equity Value'],
            'Value': [
                company_info.get('name', 'N/A'),
                valuation_data.get('ticker', 'N/A'),
                company_info.get('industry', 'N/A'),
                company_info.get('sector', 'N/A'),
                valuation_data.get('method', 'N/A'),
                valuation_data.get('enterprise_value', 'N/A'),
                valuation_data.get('equity_value', 'N/A')
            ]
        })
        
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        summary_sheet = writer.sheets['Summary']
        summary_sheet.set_column('A:A', 20)
        summary_sheet.set_column('B:B', 30)
        
        # Format the summary table
        for i, col in enumerate(summary_df.columns):
            summary_sheet.write(0, i, col, header_format)
        
        for i in range(len(summary_df)):
            for j in range(len(summary_df.columns)):
                if j == 0:  # Parameter column
                    summary_sheet.write(i+1, j, summary_df.iloc[i, j], cell_format)
                else:  # Value column
                    value = summary_df.iloc[i, j]
                    
                    # Format based on parameter type
                    if i >= 5:  # Enterprise Value and Equity Value
                        if isinstance(value, (int, float)):
                            summary_sheet.write(i+1, j, value, currency_millions_format)
                        else:
                            summary_sheet.write(i+1, j, value, cell_format)
                    else:
                        summary_sheet.write(i+1, j, value, cell_format)
        
        # Create inputs sheet
        inputs = valuation_data.get('inputs', {})
        inputs_df = pd.DataFrame({
            'Parameter': list(inputs.keys()),
            'Value': list(inputs.values())
        })
        
        # Convert parameter names to readable format
        inputs_df['Parameter'] = inputs_df['Parameter'].apply(
            lambda x: ' '.join(word.capitalize() for word in str(x).split('_'))
        )
        
        inputs_df.to_excel(writer, sheet_name='Inputs', index=False)
        inputs_sheet = writer.sheets['Inputs']
        inputs_sheet.set_column('A:A', 25)
        inputs_sheet.set_column('B:B', 20)
        
        # Format the inputs table
        for i, col in enumerate(inputs_df.columns):
            inputs_sheet.write(0, i, col, header_format)
        
        for i in range(len(inputs_df)):
            param = inputs_df.iloc[i, 0]
            value = inputs_df.iloc[i, 1]
            
            inputs_sheet.write(i+1, 0, param, cell_format)
            
            # Format based on parameter type
            if 'rate' in param.lower() or 'growth' in param.lower() or 'margin' in param.lower():
                if isinstance(value, (int, float)):
                    inputs_sheet.write(i+1, 1, value, percent_format)
                else:
                    inputs_sheet.write(i+1, 1, value, cell_format)
            elif 'price' in param.lower() or 'value' in param.lower() or 'cost' in param.lower():
                if isinstance(value, (int, float)):
                    inputs_sheet.write(i+1, 1, value, currency_format)
                else:
                    inputs_sheet.write(i+1, 1, value, cell_format)
            else:
                inputs_sheet.write(i+1, 1, value, cell_format)
        
        # Create results sheet if detailed results available
        if 'detailed_results' in valuation_data:
            results = valuation_data.get('detailed_results', {})
            
            # Convert results to dataframes and write to excel
            for result_name, result_data in results.items():
                sheet_name = result_name.replace('_', ' ').title()
                if len(sheet_name) > 31:  # Excel sheet name length limit
                    sheet_name = sheet_name[:31]
                
                # Handle different data formats
                if isinstance(result_data, dict):
                    # Convert dict to dataframe
                    result_df = pd.DataFrame(result_data)
                elif isinstance(result_data, list):
                    # Convert list to dataframe
                    if all(isinstance(item, dict) for item in result_data):
                        result_df = pd.DataFrame(result_data)
                    else:
                        result_df = pd.DataFrame({'Value': result_data})
                else:
                    # Single value
                    result_df = pd.DataFrame({'Value': [result_data]})
                
                # Write to excel
                result_df.to_excel(writer, sheet_name=sheet_name, index=False)
                result_sheet = writer.sheets[sheet_name]
                
                # Format the table
                for i, col in enumerate(result_df.columns):
                    result_sheet.write(0, i, col, header_format)
                    result_sheet.set_column(i, i, 15)
                
                # Apply basic formatting to all cells
                for i in range(len(result_df)):
                    for j in range(len(result_df.columns)):
                        value = result_df.iloc[i, j]
                        # Apply appropriate format based on column and value type
                        result_sheet.write(i+1, j, value, cell_format)
        
        # Create method-specific sheet
        method = valuation_data.get('method', '')
        if method == 'DCF':
            # Create DCF detail sheet
            if 'dcf_details' in valuation_data:
                dcf_data = valuation_data['dcf_details']
                
                # Create forecast dataframe
                years = ['Year ' + str(i) for i in range(1, len(dcf_data.get('fcf_forecast', [])) + 1)]
                forecast_df = pd.DataFrame({
                    'Year': years,
                    'Free Cash Flow': dcf_data.get('fcf_forecast', []),
                    'Present Value': dcf_data.get('present_values', [])
                })
                
                forecast_df.to_excel(writer, sheet_name='DCF Details', index=False)
                dcf_sheet = writer.sheets['DCF Details']
                
                # Format the DCF details
                for i, col in enumerate(forecast_df.columns):
                    dcf_sheet.write(0, i, col, header_format)
                
                for i in range(len(forecast_df)):
                    dcf_sheet.write(i+1, 0, forecast_df.iloc[i, 0], cell_format)
                    
                    # Format FCF and PV as currency
                    for j in range(1, len(forecast_df.columns)):
                        value = forecast_df.iloc[i, j]
                        if isinstance(value, (int, float)):
                            dcf_sheet.write(i+1, j, value, currency_millions_format)
                        else:
                            dcf_sheet.write(i+1, j, value, cell_format)
                
                # Add terminal value and enterprise value
                terminal_value = dcf_data.get('terminal_value', 'N/A')
                pv_terminal_value = dcf_data.get('pv_terminal_value', 'N/A')
                enterprise_value = valuation_data.get('enterprise_value', 'N/A')
                
                row = len(forecast_df) + 2
                dcf_sheet.write(row, 0, 'Terminal Value', cell_format)
                if isinstance(terminal_value, (int, float)):
                    dcf_sheet.write(row, 1, terminal_value, currency_millions_format)
                else:
                    dcf_sheet.write(row, 1, terminal_value, cell_format)
                
                row += 1
                dcf_sheet.write(row, 0, 'PV of Terminal Value', cell_format)
                if isinstance(pv_terminal_value, (int, float)):
                    dcf_sheet.write(row, 1, pv_terminal_value, currency_millions_format)
                else:
                    dcf_sheet.write(row, 1, pv_terminal_value, cell_format)
                
                row += 1
                dcf_sheet.write(row, 0, 'Enterprise Value', cell_format)
                if isinstance(enterprise_value, (int, float)):
                    dcf_sheet.write(row, 1, enterprise_value, currency_millions_format)
                else:
                    dcf_sheet.write(row, 1, enterprise_value, cell_format)
                
                # Set column widths
                dcf_sheet.set_column('A:A', 15)
                dcf_sheet.set_column('B:C', 20)
        
        elif method == 'Comparable Company Analysis':
            # Create Comps detail sheet
            if 'comps_details' in valuation_data:
                comps_data = valuation_data['comps_details']
                
                # Create comps dataframe
                if 'comparable_companies' in comps_data:
                    comps = comps_data['comparable_companies']
                    
                    if isinstance(comps, list) and len(comps) > 0:
                        comps_df = pd.DataFrame(comps)
                        
                        comps_df.to_excel(writer, sheet_name='Comps Details', index=False)
                        comps_sheet = writer.sheets['Comps Details']
                        
                        # Format the comps details
                        for i, col in enumerate(comps_df.columns):
                            comps_sheet.write(0, i, col, header_format)
                            comps_sheet.set_column(i, i, 15)
                        
                        # Apply appropriate formatting to each cell
                        for i in range(len(comps_df)):
                            for j in range(len(comps_df.columns)):
                                value = comps_df.iloc[i, j]
                                col_name = comps_df.columns[j].lower()
                                
                                if 'multiple' in col_name or 'ratio' in col_name or 'ev_' in col_name or 'pe_' in col_name:
                                    if isinstance(value, (int, float)):
                                        comps_sheet.write(i+1, j, value, workbook.add_format({
                                            'border': 1,
                                            'num_format': '0.00x'
                                        }))
                                    else:
                                        comps_sheet.write(i+1, j, value, cell_format)
                                elif 'margin' in col_name or 'growth' in col_name or 'rate' in col_name:
                                    if isinstance(value, (int, float)):
                                        comps_sheet.write(i+1, j, value, percent_format)
                                    else:
                                        comps_sheet.write(i+1, j, value, cell_format)
                                elif 'marketcap' in col_name.replace(' ', '') or 'value' in col_name:
                                    if isinstance(value, (int, float)):
                                        comps_sheet.write(i+1, j, value, currency_millions_format)
                                    else:
                                        comps_sheet.write(i+1, j, value, cell_format)
                                else:
                                    comps_sheet.write(i+1, j, value, cell_format)
        
        # Save the workbook
        writer.close()
        
        # Get the Excel data
        excel_data = buffer.getvalue()
        buffer.close()
        
        return excel_data
