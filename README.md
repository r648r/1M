# 1M

## Indicateurs Techniques

### 1. **MACD (Moving Average Convergence Divergence)**
Le MACD mesure la relation entre deux moyennes mobiles exponentielles (EMA) pour identifier des tendances et des signaux d'achat/vente.

#### Formule :
1. **MACD Line** = EMA(12) - EMA(26)
2. **Signal Line** = EMA(9) de la MACD Line
3. **Histogramme** = MACD Line - Signal Line

#### Interprétation :
- **MACD > Signal Line** : Tendance haussière (achat).
- **MACD < Signal Line** : Tendance baissière (vente).
- **Histogramme croissant** : Renforcement de la tendance.
- **Histogramme décroissant** : Affaiblissement de la tendance.

---

### 2. **EMA (Exponential Moving Average)**
L'EMA est une moyenne mobile qui donne plus de poids aux données récentes, la rendant plus sensible aux variations récentes.

#### Formule :
\[
EMA_{today} = Price_{today} * \alpha + EMA_{yesterday} * (1 - \alpha)
\]
avec :
- $\(\alpha = \frac{2}{N+1}\) (N = période)$

#### Interprétation :
- Réagit rapidement aux changements de prix.
- Utile pour détecter des inversions de tendance à court terme.

---

### 3. **SMA (Simple Moving Average)**
La SMA est une moyenne simple des prix sur une période donnée.

#### Formule :
\[
SMA = \frac{P_1 + P_2 + \dots + P_N}{N}
\]

avec :
- \(P_i\) : Prix à chaque intervalle.
- \(N\) : Nombre de périodes.

#### Interprétation :
- Moins sensible aux variations soudaines.
- Utilisée pour identifier des tendances générales.

---

### 4. **WMA (Weighted Moving Average)**
La WMA attribue des poids décroissants aux valeurs passées pour donner plus d'importance aux prix récents.

#### Formule :
\[
WMA = \frac{P_1 * W_1 + P_2 * W_2 + \dots + P_N * W_N}{W_1 + W_2 + \dots + W_N}
\]

avec :
- \(W_i = i\) (pondération linéaire croissante).

#### Interprétation :
- Utile pour suivre les tendances avec une réactivité modérée.
- Plus réactive que la SMA mais plus stable que l'EMA.

---

### Exemple en Python :
```python
import numpy as np
import pandas as pd

# Calcul EMA
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

# Calcul SMA
def sma(series, period):
    return series.rolling(window=period).mean()

# Calcul WMA
def wma(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

# Calcul MACD
def macd(series, short_period=12, long_period=26, signal_period=9):
    short_ema = ema(series, short_period)
    long_ema = ema(series, long_period)
    macd_line = short_ema - long_ema
    signal_line = ema(macd_line, signal_period)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# Exemple d'utilisation
data = pd.Series([10, 12, 15, 18, 20, 25, 28, 30, 35, 40])
print("EMA:", ema(data, 3))
print("SMA:", sma(data, 3))
print("WMA:", wma(data, 3))
macd_line, signal_line, histogram = macd(data)
print("MACD Line:", macd_line)
print("Signal Line:", signal_line)
print("Histogram:", histogram)
```
