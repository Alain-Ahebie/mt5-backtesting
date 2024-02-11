import warnings
warnings.filterwarnings("ignore")
from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover

import talib



class RsiOscillator(Strategy):
    
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14
    
    # it run one time at the initialization of the classe
    # for example if you want calculate the RSI for the all data frame
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)
    
    # Goes throught each candle individualy one by one 
    # Evaluates the criteria and decide what to do on the next candle
    def next(self):
        # if the first series is bigger than the second series
        if crossover(self.rsi, self.upper_bound) :
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()
            

bt = Backtest(GOOG, RsiOscillator, cash= 10_000)

stats = bt.optimize(
    upper_bound = range(50, 85, 5),
    lower_bound = range(10, 45, 5),
    rsi_window = range(10, 30, 2),
    maximize= 'Sharpe Ratio'
)
print(stats)

bt.plot()