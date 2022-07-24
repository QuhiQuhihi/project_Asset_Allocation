import pandas as pd
import numpy as np

class TargetGenerator():
    def __init__(self, cache):
        self.date = None
        self.cache = cache 

    # def compute_target(self, universe_list):
    #     target_weight = {}
    #     for ticker in universe_list:
    #         target_weight[ticker] = 1
    #     target_weight = self.normalize(target_weight)

    #     return target_weight
    
    # def default_factor(self, ticker, ftype):
    #     assert False

    # def custom_factor(self, ticker, ftype):
    #     assert False
    
    # def compute_factor(self, ticker, ftype):
    #     try:
    #         factor = self.default_factor(ticker, ftype)
    #     except:
    #         factor = self.custom_factor(ticker, ftype)
    #     return factor
    
    # def compute_factor_zscore(self, universe_list, ftype):
    #     ticker_to_factor = {}
    #     for ticker in universe_list:
    #         try:
    #             factor = self.compute_factor(ticker, ftype)
    #         except:
    #             factor = np.nan
    #         if np.isnan(factor):
    #             pass
    #         else:
    #             ticker_to_factor[ticker] = factor
    #     factor_series = pd.Series(ticker_to_factor).dropna().sort_values(ascending=False)
    #     factor_series = (factor_series-factor_series.mean())/factor_series.std()
        
    #     return factor_series
    
    def normalize(self, target_weight):
        target_sum = sum(target_weight.values())
        target_weight = {ticker:target_weight[ticker]/target_sum for ticker in target_weight}
        assert np.abs(sum(target_weight.values())-1) < 1e-6
        return target_weight
    
    def get_value(self, ticker, table, value, lag=0):
        try:
            x = self.cache[table][ticker][value].loc[:self.date].iloc[-1-lag]
        except:
            x = np.nan
        return x
    
    def get_value_series(self, ticker, table, value, lag='max'):
        try:
            if lag == 'max':
                x = self.cache[table][ticker][value].loc[:self.date]
            else:
                x = self.cache[table][ticker][value].loc[:self.date].iloc[-1-lag:]
        except:
            x = np.nan
        return x