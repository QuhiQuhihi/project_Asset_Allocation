import pandas as pd
import pandas_market_calendars as mcal
import yfinance as yf
import quandl
import numpy as np

import datetime as dt
from dateutil.relativedelta import relativedelta

import time, requests, json



def timeis(func):  
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
          
        print('[{}] is executed in {:.2f} seconds'.format(func.__name__, end-start))
        return result
    return wrap


class BacktestEngine():
    @timeis
    def __init__(self, API_key=None, fred_list=[], yfinance_list=[], market_fred_list=[]):
        
        if API_key is not None:
            self.API_key = API_key
        else:
            self.API_key = 'ad0b46ed99911d1f77534d035a2cdb72'
            
        self.cache = {}
        self.initialize(fred_list, yfinance_list, market_fred_list)
        
    def initialize(self, fred_list, yfinance_list, market_fred_list):
        def divide_by_ticker(df):
            return {ticker:df[df.ticker.values == ticker] 
                                for ticker in set(df.ticker)}

        try:
            market_df = self.update_market(market_fred_list)
            self.cache['market'] = divide_by_ticker(market_df)
        except:
            print("looks like market data generation has problem")
        
        try:
            macro_df = self.update_macro(fred_list)
            self.cache['macro'] = divide_by_ticker(macro_df)
        except:
            print("looks like macro data generation has problem")

        try:
            index_df = self.update_index(yfinance_list)
            self.cache['index'] = divide_by_ticker(index_df)
        except:
            print("looks like index data generation has problem")

        
    def update_market(self, market_fred_list):

        market_list = ['BAMLH0A0HYM2']
        market_list = set(market_list+market_fred_list)

        df = None
        for ticker in market_list:
            df_add = self._get_PIT_market_df(ticker)
            df_add['ticker'] = [ticker for _ in df_add.index]
            df = pd.concat([df, df_add],axis=0)

        df = df.sort_index()        
        return df


    def update_macro(self, fred_list):

        macro_list = ['CPIAUCSL']
        macro_list = set(macro_list+fred_list)
        
        df = None
        for ticker in macro_list:
            df_add = self._get_PIT_df(ticker)
            # df_add = self._get_PIT_df_rev(ticker)
            df_add['ticker'] = [ticker for _ in df_add.index]
            df = pd.concat([df, df_add],axis=0)

        df = df.sort_index()        
        return df


    def _get_PIT_df(self, ID):
        API_KEY = self.API_key
        REAL_TIME_START, REAL_TIME_END = '2000-01-01', '9999-12-31'
        
        url = 'https://api.stlouisfed.org/fred/series/observations?series_id={}'.format(ID)
        url += '&realtime_start={}&realtime_end={}&api_key={}&file_type=json'.format(
                                        REAL_TIME_START, REAL_TIME_END, API_KEY)
        response = requests.get(url)
        observations = json.loads(response.text)['observations']
        
        df = pd.DataFrame(observations).sort_values(['date','realtime_start']
            ).groupby('date').first()
        df.index = pd.to_datetime(df.index)
        df.realtime_start = pd.to_datetime(df.realtime_start)

        df['datekey'] = df.realtime_start
        df['is_inferred'] = (df.datekey == df.datekey.shift(1))|(
            df.datekey == df.datekey.shift(-1))

        non_inferred_df = df[df['is_inferred']==False]
        lag_list = [(y-x).days for x,y in 
                        zip(non_inferred_df.index, non_inferred_df.datekey)]
        mean_lag, max_lag = int(np.mean(lag_list)+1), int(np.max(lag_list)+1)
        
        df.datekey = [
            date + relativedelta(days=mean_lag) if df.loc[date].is_inferred
            else df.loc[date].datekey
            for date in df.index]

        df = df[['value','datekey','is_inferred']]
        df['cdate'] = df.index
        df = df.set_index('datekey')
        return df

    def _get_PIT_market_df(self, ID):
        API_KEY = self.API_key
        today = dt.datetime.today()
        REAL_TIME_START, REAL_TIME_END = '2000-01-01', '9999-12-31'
        _REAL_TIME_START = dt.datetime.strptime(REAL_TIME_START, '%Y-%m-%d') 
        _REAL_TIME_END = dt.datetime.strptime(REAL_TIME_END, '%Y-%m-%d') 

        start = _REAL_TIME_START


        df0 = None
        # df0 = pd.DataFrame(columns=['date','value','ticker'])
        # df0 = df0.set_index('date')

        for i in range(10000):
            start = start + relativedelta(years = i * 5)
            end = start + relativedelta(years = 5)

            if today < start:
                break
            elif end > today:
                end = _REAL_TIME_END # 9999-12-31

            _start = start.strftime('%Y-%m-%d')
            _end = end.strftime('%Y-%m-%d')
            
            url = 'https://api.stlouisfed.org/fred/series/observations?series_id={}'.format(ID)
            url += '&observation_start={}&observation_end={}&api_key={}&frequency={}&file_type=json'.format(
                                            _start, _end,API_KEY,'d')
            # print(url)

            response = requests.get(url)
            observations = json.loads(response.text)['observations']

            df = pd.DataFrame(observations)
            df = df[['date','value']].sort_values(['date']).groupby('date').first()
            # df = df.set_index('date')
            df.index = pd.to_datetime(df.index)
            df0 = pd.concat([df, df0], axis=0)

        return df0.sort_values(['date'])


    def update_index(self, yfinance_list):
        df = None

        yf_ticker_list = ['SPY']
        
        # Basic Index
        # yf_ticker_list = [
        #     '^GSPC','^IXIC','^DJI','^RUT','^VIX','^TNX','^SP500TR',
        #     'GC=F', 'CL=F']

        # concatenate ticker list (basic and additional)
        yf_ticker_list = set(yf_ticker_list + yfinance_list)

        for ticker in yf_ticker_list:
            df_add = yf.Ticker(ticker).history(period='max')
            df_add.index.rename('date', inplace=True)
            df_add.columns = ['openadj', 'highadj', 'lowadj', 'closeadj', 
                'volume', 'dividends', 'stock splits']
            df_add['ticker'] = [ticker for _ in df_add.index]
            df = pd.concat([df, df_add],axis=0)
            
        df = df.sort_index()
        return df

    def get_universe(self, date, custom_universe):
        if custom_universe is not None:
            universe_list = custom_universe
        else:
            universe_list = []
            for ticker in self.cache['index'].keys():
                if date in self.cache['index'][ticker].index:
                    universe_list.append(ticker)
        return universe_list

    @timeis
    def run_backtest(self, target_generator, sdate, edate, 
                    period='M', transaction_cost=0, custom_universe=None):
        start_T = time.time()
        self.asset = {}
        self.transaction = {}
        
        sdate = mcal.get_calendar('NYSE').valid_days(
            start_date='2000-01-01', end_date=sdate)[-1].strftime('%Y-%m-%d')
        edate = mcal.get_calendar('NYSE').valid_days(
            start_date='2000-01-01', end_date=edate)[-1].strftime('%Y-%m-%d')

        self.bdates = mcal.get_calendar('NYSE').valid_days(
            start_date=sdate, end_date=edate)
        self.bdates = [x.tz_localize(None) for x in self.bdates]

        print('Backtest period: {} -- {}'.format(self.bdates[1], self.bdates[-1]))

        date = self.bdates[0]
        self.date = date # dh.kim added

        self.asset[date] = {'cash':1}
        universe_list = self.get_universe(date, custom_universe)
        self.delisted_tickers = []

        target_weight = self.compute_target(date, universe_list, target_generator)
        is_rebal = True

        for date in self.bdates[1:]:
            # self.date = date # dh.kim added
            self.update_asset(date)
            self.liquidate_delisted_tickers(date)
            
            if is_rebal:
                self.rebalance_asset(date, target_weight, transaction_cost)
                
            if self.set_rebal_condition(date, 'M'):
                end_T = time.time()
                print('===','date:{}'.format(date),'/',
                      'total_asset:{:.3f}'.format(sum(self.asset[date].values())),'/',
                      'time elapsed:{:.1f}'.format(end_T-start_T),'===',
                      end='\r')

            is_rebal = self.set_rebal_condition(date, period)
               
            if is_rebal:
                self.date = date # dh.kim added
                universe_list = self.get_universe(date, custom_universe)
                universe_list = list(set(universe_list)-set(self.delisted_tickers))
                self.delisted_tickers = []
                target_weight = self.compute_target(date, universe_list, target_generator)
                
        print('===','date:{}'.format(date),'/',
                      'total_asset:{:.3f}'.format(sum(self.asset[date].values())),'/',
                      'time elapsed:{:.1f}'.format(end_T-start_T),'===')
        self.asset_df = pd.DataFrame(self.asset).T.fillna(0).iloc[1:]
        self.transaction_df = pd.DataFrame(self.transaction).T.fillna(0)

    def update_asset(self, date):
        yesterday = self.bdates[self.bdates.index(date)-1]
        self.asset[date] = {
            ticker : self.asset[yesterday][ticker]*self.get_return(ticker, date)
            for ticker in self.asset[yesterday]}
        self.transaction[date] = {}

    def rebalance_asset(self, date, target_weight, transaction_cost):
        current_asset = self.asset[date].copy()
        total_asset = sum(current_asset.values())
        target_asset = {ticker:total_asset*target_weight[ticker] for ticker in target_weight}
        transaction_asset = {}
        updated_asset = {}

        for ticker in set(target_asset.keys()).union(set(current_asset.keys())):
            target = target_asset[ticker] if ticker in target_asset else 0
            current = current_asset[ticker] if ticker in current_asset else 0
            transaction = target - current

            if transaction > 0 :
                transaction = (1-transaction_cost)*transaction
                updated_asset[ticker] = current + transaction

            elif transaction <= 0:
                if ticker in target_asset.keys():
                    updated_asset[ticker] = current + transaction
                else:
                    pass

            transaction_asset[ticker] = transaction
            
        assert np.abs(1- sum(target_asset.values())/total_asset) < 1e-6

        self.asset[date] = updated_asset
        self.transaction[date] = transaction_asset

    def get_price(self, ticker, date):
        try:
            if ticker == 'cash':
                ticker_price = 1 
            elif ticker in self.cache['index'].keys():
                ticker_price = self.cache['index'][ticker].closeadj.loc[date]
        except:
            print('{} has no price at {}'.format(ticker, date))
            assert False
        return ticker_price

    def get_return(self, ticker, date):
        if ticker == 'cash':
            return 1
        try:
            curr_price = self.cache['index'][ticker]['closeadj'].loc[date]
            last_price = self.cache['index'][ticker]['closeadj'].shift().loc[date]
            return curr_price/last_price
        except:
            print('\n')
            print('{} is delisted at {}'.format(ticker, date) + '\n')
            self.delisted_tickers.append(ticker)
            return 1

    def liquidate_delisted_tickers(self, date):
        if 'cash' not in self.asset[date]: self.asset[date]['cash'] = 0

        for ticker in self.delisted_tickers:
            if ticker in self.asset[date]:
                self.asset[date]['cash'] += self.asset[date][ticker]
                self.asset[date].pop(ticker)

    def set_rebal_condition(self, date, period):
        try:
            tomorrow = self.bdates[self.bdates.index(date)+1]
        except:
            tomorrow = date

        if period == 'D':
            is_rebal = True 
        elif period == 'W':
            is_rebal = (date.weekday() == 0)
        elif period == 'M':
            is_rebal = (tomorrow.month != date.month)
        else:
            is_rebal = False

        return is_rebal

    def compute_target(self, date, universe_list, mpg):
        mpg.date = date
        target_weight = mpg.compute_target(universe_list)

        return target_weight

