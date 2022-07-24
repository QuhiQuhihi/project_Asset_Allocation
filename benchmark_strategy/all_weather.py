import numpy as np
import pandas as pd

from backtest.backtest_engine import BacktestEngine
from backtest.target_generator import TargetGenerator


custom_universe=[
    "VTI", # Vanguard Total Stock Market ETF                        2001-05-24
    "TLT", # iShares 20+ Year Treasury Bond ETF                     2002-07-22
    "IEI", # iShares 3-7 Year Treasury Bond ETF                     2007-01-05
    "GLD", # SPDR Gold Trust                                        2004-11-18
    "GSG"  # iShares S&P GSCI Commodity Indexed Trust               2006-07-10
]

engine = BacktestEngine(yfinance_list=custom_universe)

class Sap_onlyWeightGenerator(TargetGenerator):
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
        target_weight['VTI'] = 0.300
        target_weight['TLT'] = 0.400
        target_weight['IEI'] = 0.150
        target_weight['GLD'] = 0.075
        target_weight['GSG'] = 0.075
        
        return target_weight
