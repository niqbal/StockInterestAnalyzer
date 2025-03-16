import yfinance as yf
import pandas as pd
from datetime import datetime

class FinancialAnalyzer:
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager

    def analyze_stocks(self, symbols, start_date, end_date):
        results = {}
        
        for symbol in symbols:
            try:
                # Check cache first
                cached_data = self.cache_manager.get_cached_data(symbol, start_date, end_date)
                
                if cached_data:
                    results[symbol] = cached_data
                    continue

                # Fetch data if not in cache
                stock = yf.Ticker(symbol)
                quarterly_data = stock.quarterly_financials
                
                if quarterly_data.empty:
                    continue

                # Filter by date range
                quarterly_data = quarterly_data.loc[:, (quarterly_data.columns >= pd.Timestamp(start_date)) & 
                                                    (quarterly_data.columns <= pd.Timestamp(end_date))]

                interest_data = []
                
                for quarter in quarterly_data.columns:
                    # Get financial metrics
                    try:
                        interest_income = quarterly_data.loc['Interest Income', quarter] if 'Interest Income' in quarterly_data.index else 0
                        net_income = quarterly_data.loc['Net Income', quarter] if 'Net Income' in quarterly_data.index else 0
                        shares = stock.info.get('sharesOutstanding', 0)
                        
                        quarter_data = {
                            'Quarter': quarter.strftime('%Y-Q%q'),
                            'Interest Income': interest_income,
                            'Net Income': net_income,
                            'Interest per Share': interest_income / shares if shares else 0,
                            'Interest/Net Income Ratio': (interest_income / net_income * 100) if net_income else 0
                        }
                        
                        interest_data.append(quarter_data)
                    except Exception as e:
                        continue

                # Cache the results
                self.cache_manager.cache_data(symbol, start_date, end_date, interest_data)
                results[symbol] = interest_data

            except Exception as e:
                raise Exception(f"Error analyzing {symbol}: {str(e)}")

        return results
