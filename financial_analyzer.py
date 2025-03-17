import yfinance as yf
import pandas as pd
from datetime import datetime
from logger import logger

class FinancialAnalyzer:
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager

    def analyze_stocks(self, symbols, start_date, end_date):
        results = {}

        for symbol in symbols:
            try:
                logger.info(f"Analyzing stock: {symbol}")

                # Check cache first
                cached_data = self.cache_manager.get_cached_data(symbol, start_date, end_date)

                if cached_data:
                    results[symbol] = cached_data
                    continue

                # Fetch data if not in cache
                logger.info(f"Fetching data from Yahoo Finance for {symbol}")
                stock = yf.Ticker(symbol)
                quarterly_data = stock.quarterly_financials

                if quarterly_data.empty:
                    logger.warning(f"No data found for {symbol}")
                    continue

                # Filter by date range
                quarterly_data = quarterly_data.loc[:, (quarterly_data.columns >= pd.Timestamp(start_date)) & 
                                                    (quarterly_data.columns <= pd.Timestamp(end_date))]

                interest_data = []

                for quarter in quarterly_data.columns:
                    try:
                        interest_income = quarterly_data.loc['Interest Income', quarter] if 'Interest Income' in quarterly_data.index else 0
                        net_income = quarterly_data.loc['Net Income', quarter] if 'Net Income' in quarterly_data.index else 0
                        shares = stock.info.get('sharesOutstanding', 0)

                        quarter_data = {
                            'Quarter': quarter.strftime('%Y-Q%m'),
                            'Interest Income': interest_income,
                            'Net Income': net_income,
                            'Interest per Share': interest_income / shares if shares else 0,
                            'Interest/Net Income Ratio': (interest_income / net_income * 100) if net_income else 0
                        }

                        interest_data.append(quarter_data)
                        logger.info(f"Processed quarter {quarter.strftime('%Y-Q%m')} for {symbol}")
                    except Exception as e:
                        logger.error(f"Error processing quarter data for {symbol}: {str(e)}")
                        continue

                # Cache the results
                self.cache_manager.cache_data(symbol, start_date, end_date, interest_data)
                results[symbol] = interest_data

            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {str(e)}")
                raise Exception(f"Error analyzing {symbol}: {str(e)}")

        return results