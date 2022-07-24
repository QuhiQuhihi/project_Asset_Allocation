import numpy as np
import pandas as pd

from backtest.backtest_engine import BacktestEngine
from backtest.target_generator import TargetGenerator

custom_universe = ['SPY']
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
        target_weight['SPY'] = 1.00
        
        return target_weight
    