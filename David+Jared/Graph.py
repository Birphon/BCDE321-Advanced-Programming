# CSV
import csv
# Pandas
import pandas as pd
# MathPlotLib
import matplotlib.pyplot as plt 
data = [
    # [Turn, Health]
    [1,6], # Actually this will break here lmao
    [2,9],
    [3,7],
    [4,3]
]

with open('..\David+Jared\CSV\player_health.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

plt.rcParams["figure.figsize"] = [7, 3]
plt.rcParams["figure.autolayout"] = True
headers = ['Turn', 'Health']
df = pd.read_csv('player_health.csv', names=headers)
df.set_index('Turn').plot()
plt.show()