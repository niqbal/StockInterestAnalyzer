import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from financial_analyzer import FinancialAnalyzer
from cache_manager import CacheManager
from logger import logger

def main():
    st.title("Stock Interest Earnings Analyzer")

    # Initialize components
    cache_mgr = CacheManager()
    financial_analyzer = FinancialAnalyzer(cache_mgr)

    # Input section
    st.subheader("Enter Stock Symbols")
    stock_input = st.text_input(
        "Enter stock symbols (comma-separated)",
        placeholder="e.g., NVDA, TSLA, CRM"
    )

    # Date range selection
    st.subheader("Select Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=365)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )

    if st.button("Analyze Stocks"):
        if not stock_input:
            st.error("Please enter at least one stock symbol")
            return

        stocks = [s.strip() for s in stock_input.split(",")]
        logger.info(f"Analyzing stocks: {stocks}")

        with st.spinner("Analyzing stock data..."):
            try:
                results = financial_analyzer.analyze_stocks(
                    stocks,
                    start_date,
                    end_date
                )

                if results:
                    # Display results
                    st.subheader("Analysis Results")
                    for stock, data in results.items():
                        st.write(f"**{stock} Analysis**")

                        # Create DataFrame for display
                        df = pd.DataFrame(data)
                        st.dataframe(df)
                else:
                    st.warning("No data found for the selected stocks and date range")

            except Exception as e:
                logger.error(f"Error during analysis: {str(e)}")
                st.error(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()