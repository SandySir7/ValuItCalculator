import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import base64

class PDFGenerator:
    """
    Utility class for generating PDF reports for valuations
    """
    
    @staticmethod
    def generate_valuation_report(valuation_data, company_info, filename="valuation_report.pdf"):
        """
        Generate a PDF report for a valuation
        
        Args:
            valuation_data (dict): Valuation data including results
            company_info (dict): Company information
            filename (str): Output filename
            
        Returns:
            bytes: PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        styles = getSampleStyleSheet()
        style_heading1 = styles['Heading1']
        style_heading2 = styles['Heading2']
        style_normal = styles['Normal']
        
        # Create custom styles
        style_title = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=18,
            alignment=1,  # Center alignment
        )
        
        style_subtitle = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.darkblue,
        )
        
        style_table_header = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.white,
            alignment=1,  # Center alignment
        )
        
        # Build document content
        content = []
        
        # Title
        content.append(Paragraph("ValuIt - Company Valuation Report", style_title))
        content.append(Spacer(1, 0.25*inch))
        
        # Company information
        content.append(Paragraph(f"Company: {company_info.get('name', 'N/A')} ({valuation_data.get('ticker', 'N/A')})", style_heading1))
        content.append(Paragraph(f"Industry: {company_info.get('industry', 'N/A')}", style_normal))
        content.append(Paragraph(f"Sector: {company_info.get('sector', 'N/A')}", style_normal))
        content.append(Spacer(1, 0.25*inch))
        
        # Valuation Summary
        content.append(Paragraph("Valuation Summary", style_heading2))
        
        # Create summary table
        valuation_method = valuation_data.get('method', 'N/A')
        enterprise_value = valuation_data.get('enterprise_value', 'N/A')
        equity_value = valuation_data.get('equity_value', 'N/A')
        
        if isinstance(enterprise_value, (int, float)):
            enterprise_value_str = f"${enterprise_value/1e9:.2f} billion"
        else:
            enterprise_value_str = enterprise_value
            
        if isinstance(equity_value, (int, float)):
            equity_value_str = f"${equity_value/1e9:.2f} billion"
        else:
            equity_value_str = equity_value
        
        summary_data = [
            ["Valuation Method", "Enterprise Value", "Equity Value"],
            [valuation_method, enterprise_value_str, equity_value_str]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        content.append(summary_table)
        content.append(Spacer(1, 0.25*inch))
        
        # Valuation Inputs
        content.append(Paragraph("Valuation Inputs", style_heading2))
        
        inputs = valuation_data.get('inputs', {})
        if valuation_method == "DCF":
            input_data = [
                ["Parameter", "Value"],
                ["WACC", f"{inputs.get('wacc', 'N/A')*100:.2f}%" if isinstance(inputs.get('wacc'), (int, float)) else inputs.get('wacc', 'N/A')],
                ["Terminal Growth Rate", f"{inputs.get('terminal_growth_rate', 'N/A')*100:.2f}%" if isinstance(inputs.get('terminal_growth_rate'), (int, float)) else inputs.get('terminal_growth_rate', 'N/A')],
                ["Forecast Period", f"{inputs.get('forecast_years', 'N/A')} years"],
            ]
        elif valuation_method == "Comparable Company Analysis":
            input_data = [
                ["Parameter", "Value"],
                ["EV/EBITDA Multiple", f"{inputs.get('ev_ebitda_multiple', 'N/A'):.2f}x" if isinstance(inputs.get('ev_ebitda_multiple'), (int, float)) else inputs.get('ev_ebitda_multiple', 'N/A')],
                ["P/E Multiple", f"{inputs.get('pe_multiple', 'N/A'):.2f}x" if isinstance(inputs.get('pe_multiple'), (int, float)) else inputs.get('pe_multiple', 'N/A')],
                ["EV/Revenue Multiple", f"{inputs.get('ev_revenue_multiple', 'N/A'):.2f}x" if isinstance(inputs.get('ev_revenue_multiple'), (int, float)) else inputs.get('ev_revenue_multiple', 'N/A')],
            ]
        else:
            input_data = [["Parameter", "Value"]]
            for key, value in inputs.items():
                if isinstance(value, (int, float)):
                    if 'rate' in key or 'growth' in key:
                        formatted_value = f"{value*100:.2f}%"
                    else:
                        formatted_value = f"{value:.2f}"
                else:
                    formatted_value = str(value)
                input_data.append([key.replace('_', ' ').title(), formatted_value])
        
        input_table = Table(input_data, colWidths=[3*inch, 3*inch])
        input_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        content.append(input_table)
        content.append(Spacer(1, 0.25*inch))
        
        # Generate and add charts if available
        if 'charts' in valuation_data:
            try:
                # For each chart in the valuation data, convert to an image and add to the PDF
                for chart_title, chart_data in valuation_data['charts'].items():
                    content.append(Paragraph(chart_title, style_subtitle))
                    
                    # Create figure using matplotlib
                    fig, ax = plt.figure(figsize=(6, 4), dpi=100)
                    
                    # Logic to create appropriate chart based on chart_data
                    # This is simplified - in a real app you'd have more specific chart creation
                    
                    # Save figure to bytes
                    img_data = io.BytesIO()
                    plt.savefig(img_data, format='png')
                    img_data.seek(0)
                    
                    # Add image to PDF
                    img = Image(img_data, width=6*inch, height=4*inch)
                    content.append(img)
                    content.append(Spacer(1, 0.25*inch))
                    
                    # Close the plot to free memory
                    plt.close()
            except Exception as e:
                content.append(Paragraph(f"Error generating charts: {str(e)}", style_normal))
        
        # Disclaimer
        content.append(Spacer(1, 0.5*inch))
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
        )
        disclaimer_text = """
        Disclaimer: This valuation report is generated for informational purposes only. 
        The valuation presented is based on the inputs provided and publicly available information. 
        It should not be considered as financial advice or a recommendation to buy or sell securities. 
        Always consult with a qualified financial advisor before making investment decisions.
        """
        content.append(Paragraph(disclaimer_text, disclaimer_style))
        
        # Build the PDF
        doc.build(content)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
