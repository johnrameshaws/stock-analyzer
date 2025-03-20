import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

class TickerInfo:
    def __init__(self, ticker_symbol, purchased_date, quantity, avg_cost_basis, country):
        self.ticker = yf.Ticker(ticker_symbol)
        self.purchased_date = purchased_date
        self.quantity = quantity
        self.avg_cost_basis = avg_cost_basis
        self.country = country

    def get_full_info(self):
        info = {
            'company_info': self.ticker.info,
            'balance_sheet': self.ticker.balance_sheet,
            'cashflow': self.ticker.cashflow,
            'earnings': self.ticker.earnings,
            'sustainability': self.ticker.sustainability,
            'analyst_price_targets': self.ticker.analyst_price_targets,
            'recommendations': self.ticker.recommendations,
        }
        return info

    def get_recommendations_by_dictionary(self):
        recommendations = self.ticker.recommendations.iloc[0].to_dict()
        return recommendations

    def get_process_last_2years_performance(self):
        period_perf_df=pd.DataFrame(columns=['period', 'quantity', 'actual_price', 'actual_cost', 'date', 'close', 'current_cost'])
        start_date=self.purchased_date
        print(start_date)
        two_years_ago = datetime.now() - pd.DateOffset(years=2)
        if two_years_ago < start_date:
            start_date = two_years_ago

        data = self.ticker.history(start=start_date)
        """get min data"""
        row={
                'period': 'min',
                'quantity': self.quantity,
                'actual_price': self.avg_cost_basis,
                'actual_cost': self.quantity * self.avg_cost_basis,
                'date' : data['Close'].idxmin(),
                'close': data['Close'].min(),
                'current_cost': self.quantity * data['Close'].min(),
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        """get max data"""
        row={
                'period': 'max',
                'quantity': self.quantity,
                'actual_price': self.avg_cost_basis,
                'actual_cost': self.quantity * self.avg_cost_basis,
                'date' : data['Close'].idxmax(),
                'close': data['Close'].max(),
                'current_cost': self.quantity * data['Close'].max(),
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        """get current data"""
        row={
                'period': 'now',
                'quantity': self.quantity,
                'actual_price': self.avg_cost_basis,
                'actual_cost': self.quantity * self.avg_cost_basis,
                'date' : data.iloc[-1].name,
                'close': data['Close'].iloc[-1],
                'current_cost': self.quantity * data['Close'].iloc[-1],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        """get previous day data"""
        row={
                'period': 'previous day',
                'quantity': self.quantity,
                'actual_price': self.avg_cost_basis,
                'actual_cost': self.quantity * self.avg_cost_basis,
                'date' : data.iloc[-2].name,
                'close': data['Close'].iloc[-2],
                'current_cost': self.quantity * data['Close'].iloc[-2],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)


    def get_last_2years_performance(self, quantity, avg_cost_basis, purchased_date):
        period_perf_df=pd.DataFrame(columns=['period', 'quantity', 'actual_price', 'actual_cost', 'date', 'close', 'current_cost'])

        start_date=self.purchased_date        
        two_years_ago = datetime.now() - pd.DateOffset(years=2)
        if two_years_ago < start_date:
            start_date = two_years_ago

        self.data = self.ticker.history(start=start_date)
        #data = self.ticker.history(start=purchased_date)
        row={
                'period': 'min',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data['Close'].idxmin(),
                'close': self.data['Close'].min(),
                'current_cost': quantity * self.data['Close'].min(),
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        row={
                'period': 'max',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data['Close'].idxmax(),
                'close': self.data['Close'].max(),
                'current_cost': quantity * self.data['Close'].max(),
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        row={
                'period': 'now',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[-1].name,
                'close': self.data['Close'].iloc[-1],
                'current_cost': quantity * self.data['Close'].iloc[-1],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        row={
                'period': 'previous day',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[-2].name,
                'close': self.data['Close'].iloc[-2],
                'current_cost': quantity * self.data['Close'].iloc[-2],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        row={
                'period': '1wk before',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[-5].name,
                'close': self.data['Close'].iloc[-5],
                'current_cost': quantity * self.data['Close'].iloc[-5],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        #data = self.ticker.history(period='1mo', interval='1d')    
        row={
                'period': '1mo before',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[-20].name,
                'close': self.data['Close'].iloc[-20],
                'current_cost': quantity * self.data['Close'].iloc[-20],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        #data = self.ticker.history(period='6mo', interval='1d')    
        row={
                'period': '6mo before',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[-120].name,
                'close': self.data['Close'].iloc[-120],
                'current_cost': quantity * self.data['Close'].iloc[-120],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        #data = self.ticker.history(period='1y', interval='1d')    
        row={
                'period': '1yr before',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[-240].name,
                'close': self.data['Close'].iloc[-240],
                'current_cost': quantity * self.data['Close'].iloc[-240],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        #data = self.ticker.history(period='2y', interval='1d')    
        row={
                'period': '2yr before',
                'quantity': quantity,
                'actual_price': avg_cost_basis,
                'actual_cost': quantity * avg_cost_basis,
                'date' : self.data.iloc[0].name,
                'close': self.data['Close'].iloc[0],
                'current_cost': quantity * self.data['Close'].iloc[0],
            }
        period_perf_df=pd.concat([period_perf_df, pd.DataFrame([row])], ignore_index=True)

        yr1_df=self.data[self.data.index.year >= datetime.now().year - 1]
        self.yr1_min_price = yr1_df['Close'].min()
        self.yr1_max_price = yr1_df['Close'].max()

        return period_perf_df.sort_values(by='date')

    def get_current_price(self):
        current_price = self.ticker.info.get('currentPrice', 'N/A')
        if current_price == 'N/A':
            current_price = self.ticker.info.get('previousClose', 'N/A')
        return current_price
    
    def get_previous_close_price(self):
        previous_close_price = self.ticker.info.get('previousClose', 'N/A')
        return previous_close_price

    def get_1wk_before_price(self):
        data = self.ticker.history(period='1wk', interval='1d')
        close_price = data['Close'].iloc[0]
        return close_price

    def get_1mo_before_price(self):
        data = self.ticker.history(period='1mo', interval='1d')
        close_price = data['Close'].iloc[0]
        return close_price

    def get_6mo_before_price(self):
        data = self.ticker.history(period='6mo', interval='1d')
        close_price = data['Close'].iloc[0]
        return close_price

    def get_1y_before_price(self):
        data = self.ticker.history(period='1y', interval='1d')
        close_price = data['Close'].iloc[0]
        return close_price

    def get_2y_before_price(self):
        data = self.ticker.history(period='2y', interval='1d')
        close_price = data['Close'].iloc[0]
        return close_price

    def get_historical_data(self, period='1mo', interval='1d'):
        historical_data = self.ticker.history(period=period, interval=interval)
        return historical_data
    
    def get_historical_data_with_duration(self, period='1mo', interval='1d'):
        #df = self.ticker.history(start=start_date, end=datetime.now())
        df = self.ticker.history(period=period, interval=interval)

        today1 = pd.to_datetime(datetime.now())
        df_x=df[['Close']]
        df_x=df_x.reset_index()
        df_x['Date']=df_x['Date'].dt.date 
        df_x['duration']=(today1 - pd.to_datetime(df_x['Date'])).dt.days
        df_x['duration']=np.where(df_x['duration'] <= 7, '1wk',
                                np.where(df_x['duration'] <= 31, '1mo',
                                np.where(df_x['duration'] <= 120, '3mos',
                                np.where(df_x['duration'] <= 180, '6mos',
                                np.where(df_x['duration'] <= 365, '1yr','2yrs')))))                                
        return df_x

    def get_dividends(self):
        dividends = self.ticker.dividends
        return dividends

    def get_stock_splits(self):
        stock_splits = self.ticker.splits
        return stock_splits

    def get_recent_news(self):
        news = self.ticker.news
        return news

    def get_major_holders(self):
        major_holders = self.ticker.major_holders
        return major_holders

    def get_institutional_holders(self):
        institutional_holders = self.ticker.institutional_holders
        return institutional_holders

    def get_recommendations_summary(self):
        recommendations_summary = self.ticker.recommendations_summary
        return recommendations_summary

    def get_earnings_calendar(self):
        earnings_calendar = self.ticker.earnings_dates
        return earnings_calendar

    def get_financials(self):
        financials = self.ticker.financials
        return financials

