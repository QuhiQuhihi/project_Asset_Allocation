import numpy as np
import pandas as pd

from backtest.backtest_engine import BacktestEngine
from backtest.target_generator import TargetGenerator


custom_universe=[
'IVV', # iShares Core S&P 500 ETF 2000-05-15
'AGG', # iShares Core U.S. Aggregate Bond ETF # 2003-09-22
]

engine = BacktestEngine(yfinance_list=custom_universe)

class _60_40_allocation(TargetGenerator):
    def __init__(self, cache):
        super().__init__(cache)

    def compute_target(self, universe_list):
        """
        Inputs
            universe_list(list) : list of ETFs that weights should be computed
        Outputs
            target_weight(dict)
        """
        target_weight = {}
        target_weight['IVV'] = 0.40
        target_weight['AGG'] = 0.60

        
        return target_weight