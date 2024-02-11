import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module='backtesting.*')
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

stats = bt.run()
print(stats)

bt.plot()