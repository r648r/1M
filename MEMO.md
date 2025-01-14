# Lookahead bias

*it's very likely future data was used without realizing it. Often happens when smoothing or resampling the data*

## Stratégie incorrecte 

```python
# Data[t+1] => Prise de position[t]

for i in range(len(data)):
    if data['Close'][i] > data['Open'][i]:  # Décision basée sur la clôture de la même bougie
        position = 'Acheter'
    else:
        position = 'Vendre'
    print(f"Temps {i}: {position}")
```

Le prix de clôture d'une bougie n'est connu qu'à la fin de la période. Ici, la stratégie utilise cette information future pour décider au début de la même période.

## Stratégie correcte

```
# Data[n-1] => Position[n]
for i in range(1, len(data)):  # Commencer à partir de la 2e bougie
    if data['Close'][i-1] > data['Open'][i-1]:  # Utiliser les données de la bougie précédente
        position = 'Acheter'
    else:
        position = 'Vendre'
    print(f"Temps {i}: {position}")
```
La décision pour la bougie actuelle est basée sur le prix de clôture et d'ouverture de la bougie précédente.
