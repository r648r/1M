import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import logging


# TODO
# Faire une fonction qui realise cela 
# 1) Multi-Timeframe Analysis
# 2) Crossover Strategy
# 3) Zero-Cross Strategy
# 4) Relative Vigor Index (RVI)
# https://alchemymarkets.com/education/indicators/macd/
# Faire un backtesting de chaque fonction avec les paramètres par default de ces differents algo avec td ou tv 
# Intégré un brutforce des paramètres des params du MACD
# Faire la page de monitoring pour afficher cette shit
# Regarder une nouvelle fois l'article pour trouver des indicateurs complémentaires

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(symbol='BTC-USD', period='2y', interval='1d'):
    """Télécharge les données de marché depuis Yahoo Finance."""
    logging.info(f'Téléchargement des données pour {symbol} sur {period} avec un intervalle de {interval}')
    try:
        df = yf.download(symbol, period=period, interval=interval)
        if df.empty:
            logging.warning('Aucune donnée récupérée. Vérifiez les paramètres de requête.')
        else:
            logging.info(f'{len(df)} lignes de données téléchargées avec succès.')
        df = df.dropna()

        df.index = pd.to_datetime(df.index).tz_localize(None)
        logging.info(f'Type de l\'index : {type(df.index)}')
        logging.info(f'Données disponibles : \n{df.head()}')
        return df
    except Exception as e:
        logging.error(f'Erreur lors du téléchargement des données : {e}')
        raise


def calculate_macd(df, fast_length=12, slow_length=26, signal_length=9):
    """Calcule les lignes MACD et Signal."""
    logging.info('Calcul des lignes MACD et Signal.')
    try:
        short_ema = df['Close'].ewm(span=fast_length, adjust=False).mean()
        long_ema = df['Close'].ewm(span=slow_length, adjust=False).mean()
        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span=signal_length, adjust=False).mean()
        logging.info('Calcul du MACD terminé avec succès.')
        logging.info(f'MACD line: \n{macd_line.head()}')
        logging.info(f'Signal line: \n{signal_line.head()}')
        return macd_line, signal_line
    except Exception as e:
        logging.error(f'Erreur lors du calcul du MACD : {e}')
        raise


def detect_crossovers(macd_line, signal_line):
    """Détecte les points de croisement du MACD et retourne une liste des signaux."""
    buy_signals = (macd_line > signal_line) & (macd_line.shift(1) <= signal_line.shift(1))
    sell_signals = (macd_line < signal_line) & (macd_line.shift(1) >= signal_line.shift(1))

    crossovers = []
    for idx in macd_line.index:
        if buy_signals.loc[idx].item():
            crossovers.append((idx, 'Achat'))
        elif sell_signals.loc[idx].item():
            crossovers.append((idx, 'Vente'))

    logging.info(f'Points de croisement détectés : {crossovers}')
    return crossovers


def plot_macd(df, macd_line, signal_line, crossovers):
    """Trace les graphiques des prix et du MACD avec des signaux d'achat et de vente."""
    logging.info('Préparation des graphiques.')
    try:
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 1, 1)
        plt.plot(df.index, df['Close'], label='BTC/USDT', color='black')
        plt.title('BTC/USDT Price')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)

        for crossover in crossovers:
            color = 'green' if crossover[1] == 'Achat' else 'red'
            marker = '^' if crossover[1] == 'Achat' else 'v'
            plt.scatter(crossover[0], df['Close'].loc[crossover[0]], color=color, marker=marker, s=100)

        plt.subplot(2, 1, 2)
        plt.plot(df.index, macd_line, label='MACD Line', color='blue')
        plt.plot(df.index, signal_line, label='Signal Line', color='orange')
        plt.axhline(0, color='gray', linewidth=0.5, linestyle='--')

        plt.title('MACD Indicator')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()
        logging.info('Graphiques tracés avec succès.')
    except Exception as e:
        logging.error(f'Erreur lors de la génération des graphiques : {e}')
        raise

logging.info('Début de l\'exécution du script.')
try:
    df = fetch_data()
    if not df.empty:
        macd_line, signal_line = calculate_macd(df)
        crossovers = detect_crossovers(macd_line, signal_line)
        logging.info(f'Points de croisement détectés : {crossovers}')
        print("Points de croisement MACD:", crossovers)
        plot_macd(df, macd_line, signal_line, crossovers)
    else:
        logging.warning('Aucune donnée à afficher. Fin du script.')
except Exception as e:
    logging.critical(f'Échec du script : {e}')

logging.info('Fin du script.')
