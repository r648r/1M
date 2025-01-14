import backtrader as bt
from datetime import datetime
import yfinance as yf
import pandas as pd
from icecream import ic
import pyfolio as pf

# Créez une nouvelle stratégie
class RSI_Strategy(bt.Strategy):
    params = (('rsi_period', 14),)

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)  # Acheter 1 unité
            ic("Buying at RSI:", self.rsi[0])
        elif self.rsi > 70 and self.position:
            self.sell(size=1)  # Vendre 1 unité
            ic("Selling at RSI:", self.rsi[0])

# Initialisez le cerebro
cerebro = bt.Cerebro()

# Ajouter l'analyseur PyFolio
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

# Ajouter la stratégie
cerebro.addstrategy(RSI_Strategy)

# Définir le budget initial
cerebro.broker.setcash(1000.00)

# Télécharger les données
data = yf.download('AAPL', start='2020-01-01', end='2021-01-01')
data.columns = [col[0] for col in data.columns]  # Aplatir le MultiIndex
data.reset_index(inplace=True)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Convertir les données en un DataFrame de Backtrader
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# Exécutez le backtest
results = cerebro.run()
strat = results[0]

# Récupérer l'analyseur PyFolio
pyfolio_analyzer = strat.analyzers.getbyname('pyfolio')
returns, positions, transactions, gross_lev = pyfolio_analyzer.get_pf_items()

# Générer le rapport avec PyFolio
pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    # Supprimer gross_lev si pas nécessaire
    # gross_lev=gross_lev,
    live_start_date='2005-05-01',  # Ajustez cette date selon votre stratégie
    round_trips=True
)
