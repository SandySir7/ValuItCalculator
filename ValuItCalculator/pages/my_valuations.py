import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

from utils.pdf_generator import PDFGenerator
from utils.excel_generator import ExcelGenerator

def show():
    """Display the My Valuations page"""
    
    st.title("My Valuations")
    
    # Check if user is logged in
    if not st.session_state.user:
        st.warning("Please login to view your saved valuations.")
        return
    
    # Initialize valuations list if not exists
    if 'valuations' not in st.session_state:
        st.session_state.valuations = []
    
    # Display saved valuations
    if not st.session_state.valuations:
        st.info("You haven't saved any valuations yet. Use the Valuation Tool to create and save valuations.")
    else:
        # Create a dataframe of saved valuations for display
        valuations_data = []
        for val in st.session_state.valuations:
            # Format values to millions or billions
            def format_value(value):
                if isinstance(value, (int, float)):
                    if abs(value) >= 1e9:
                        return f"${value/1e9:.2f}B"
                    elif abs(value) >= 1e6:
                        return f"${value/1e6:.2f}M"
                    else:
                        return f"${value:.2f}"
                return value
            
            enterprise_value = format_value(val.get('enterprise_value', 'N/A'))
            equity_value = format_value(val.get('equity_value', 'N/A'))
            
            valuations_data.append({
                'ID': val.get('id', ''),
                'Company': val.get('company', 'Unknown'),
                'Method': val.get('method', ''),
                'Enterprise Value': enterprise_value,
                'Equity Value': equity_value,
                'Date': val.get('timestamp', '')
            })
        
        # Display valuations in a table
        df = pd.DataFrame(valuations_data)
        st.dataframe(df, use_container_width=True)
        
        # Valuation details and actions
        st.subheader("Valuation Details")
        
        # Select a valuation to view
        valuation_ids = [val.get('id', '') for val in st.session_state.valuations]
        valuation_names = [f"{val.get('company', 'Unknown')} - {val.get('method', '')} ({val.get('timestamp', '')})" for val in st.session_state.valuations]
        
        selected_index = 0
        if 'current_valuation' in st.session_state and st.session_state.current_valuation:
            try:
                selected_index = valuation_ids.index(st.session_state.current_valuation.get('id', ''))
            except:
                selected_index = 0
        
        selected_valuation = st.selectbox(
            "Select a valuation to view",
            options=valuation_names,
            index=selected_index
        )
        
        # Get the selected valuation data
        selected_index = valuation_names.index(selected_valuation)
        selected_valuation_data = st.session_state.valuations[selected_index]
        
        # Store the current valuation for reference
        st.session_state.current_valuation = selected_valuation_data
        
        # Display valuation details
        with st.expander("Valuation Summary", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Company:** {selected_valuation_data.get('company', 'Unknown')}")
                st.write(f"**Method:** {selected_valuation_data.get('method', '')}")
                st.write(f"**Date:** {selected_valuation_data.get('timestamp', '')}")
            
            with col2:
                st.write(f"**Enterprise Value:** {format_value(selected_valuation_data.get('enterprise_value', 'N/A'))}")
                st.write(f"**Equity Value:** {format_value(selected_valuation_data.get('equity_value', 'N/A'))}")
            
            with col3:
                st.write("**Actions:**")
                
                # Download options
                if st.button("Download PDF"):
                    try:
                        valuation_data = selected_valuation_data.get('data', {})
                        
                        # Get company info from the valuation data
                        company_info = {
                            'name': valuation_data.get('company_name', '') or valuation_data.get('ticker', ''),
                            'industry': valuation_data.get('inputs', {}).get('industry', ''),
                            'sector': 'N/A'  # This might be stored elsewhere in a real app
                        }
                        
                        pdf_data = PDFGenerator.generate_valuation_report(
                            valuation_data=valuation_data,
                            company_info=company_info
                        )
                        
                        company_name = valuation_data.get('company_name', '') or valuation_data.get('ticker', 'company')
                        filename = f"{company_name.replace(' ', '_')}_{valuation_data.get('method', '').replace(' ', '_')}_valuation.pdf"
                        
                        st.download_button(
                            label="Download PDF",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
                
                if st.button("Download Excel"):
                    try:
                        valuation_data = selected_valuation_data.get('data', {})
                        
                        # Get company info from the valuation data
                        company_info = {
                            'name': valuation_data.get('company_name', '') or valuation_data.get('ticker', ''),
                            'industry': valuation_data.get('inputs', {}).get('industry', ''),
                            'sector': 'N/A'  # This might be stored elsewhere in a real app
                        }
                        
                        excel_data = ExcelGenerator.generate_valuation_excel(
                            valuation_data=valuation_data,
                            company_info=company_info
                        )
                        
                        company_name = valuation_data.get('company_name', '') or valuation_data.get('ticker', 'company')
                        filename = f"{company_name.replace(' ', '_')}_{valuation_data.get('method', '').replace(' ', '_')}_valuation.xlsx"
                        
                        st.download_button(
                            label="Download Excel",
                            data=excel_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except Exception as e:
                        st.error(f"Error generating Excel: {str(e)}")
        
        # If multiple valuations for the same company, show comparison
        if len(st.session_state.valuations) > 1:
            # Check if there are other valuations for the same company
            company = selected_valuation_data.get('company', '')
            same_company_valuations = [v for v in st.session_state.valuations if v.get('company', '') == company]
            
            if len(same_company_valuations) > 1:
                with st.expander("Valuation Comparison", expanded=True):
                    st.write(f"### Comparing Valuations for {company}")
                    
                    # Create comparison chart
                    comparison_data = []
                    for val in same_company_valuations:
                        enterprise_value = val.get('enterprise_value', 0)
                        equity_value = val.get('equity_value', 0)
                        timestamp = val.get('timestamp', '')
                        method = val.get('method', '')
                        
                        if isinstance(enterprise_value, (int, float)) and isinstance(equity_value, (int, float)):
                            comparison_data.append({
                                'Date': timestamp,
                                'Method': method,
                                'Value Type': 'Enterprise Value',
                                'Value': enterprise_value
                            })
                            comparison_data.append({
                                'Date': timestamp,
                                'Method': method,
                                'Value Type': 'Equity Value',
                                'Value': equity_value
                            })
                    
                    if comparison_data:
                        df = pd.DataFrame(comparison_data)
                        
                        # Create a grouped bar chart
                        fig = px.bar(
                            df,
                            x='Date',
                            y='Value',
                            color='Value Type',
                            barmode='group',
                            title=f'Valuation Comparison for {company}',
                            labels={'Value': 'Value ($)', 'Date': ''},
                            hover_data=['Method']
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
        
        # Delete valuation option
        if st.button("Delete Selected Valuation"):
            if st.session_state.valuations:
                # Remove the selected valuation
                st.session_state.valuations = [v for v in st.session_state.valuations if v.get('id', '') != selected_valuation_data.get('id', '')]
                
                # Reset current valuation if it was deleted
                if st.session_state.current_valuation and st.session_state.current_valuation.get('id', '') == selected_valuation_data.get('id', ''):
                    st.session_state.current_valuation = None
                
                st.success("Valuation deleted successfully!")
                st.rerun()
        
        # Export all valuations option
        if st.button("Export All Valuations as JSON"):
            try:
                # Convert valuations to JSON
                valuations_json = json.dumps(st.session_state.valuations, default=str)
                
                # Create download button
                st.download_button(
                    label="Download JSON",
                    data=valuations_json,
                    file_name=f"valuations_{st.session_state.user}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Error exporting valuations: {str(e)}")

