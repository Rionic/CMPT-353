import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])
print(totals)

sums = totals.sum(axis=1)
print("City with lowest total precipitation:")
print(sums.idxmin())

print("Average precipitation in each month:")
print(totals.sum(axis=0)/counts.sum(axis=0))

print("Average precipitation in each city:")
print(totals.sum(axis=1)/counts.sum(axis=1))
