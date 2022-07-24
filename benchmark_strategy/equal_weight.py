import numpy as np
import pandas as pd

from backtest.backtest_engine import BacktestEngine
from backtest.target_generator import TargetGenerator



# engine = BacktestEngine(yfinance_list=custom_universe)
engine = BacktestEngine()


class EqualWeightGenerator(TargetGenerator):
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

        N = len(universe_list)

        for ticker in universe_list:
            target_weight[ticker] = 1/N

        return target_weight