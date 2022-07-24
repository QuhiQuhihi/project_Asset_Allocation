import numpy as np
import pandas as pd

from backtest.backtest_engine import BacktestEngine
from backtest.target_generator import TargetGenerator


custom_universe=[
'VTI', # Vanguard Total Stock Market ETF 2001-05-24
'AGG', # iShares Core U.S. Aggregate Bond ETF # 2003-09-22
]

engine = BacktestEngine(yfinance_list=custom_universe)

class _50_50_allocation(TargetGenerator):
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
        target_weight['VTI'] = 0.50
        target_weight['AGG'] = 0.50

        
        return target_weight
    