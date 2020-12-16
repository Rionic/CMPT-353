import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filename1 = sys.argv[1]
filename2 = sys.argv[2]

data = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])
data = data.sort_values(by=['views'], ascending=False)
# print(data)

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(data['views'].values) # build plot 1
plt.xlabel("Rank")
plt.ylabel("Views")
plt.title("Popularity Distribution")

data2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

data2 = data2.sort_values(by=['views'], ascending=False)
data2 = data2.rename(columns={"views": "views 2"})
# print(data2)

result = pd.concat([data['views'], data2['views 2']], axis=1, join='inner')
# print(result)

plt.subplot(1, 2, 2) # ... and then select the second
plt.scatter(result['views'].values, result['views 2'].values) # build plot 2
plt.xlabel("Day 1 Views")
plt.ylabel("Day 2 Views")
plt.title("Daily correlation")
plt.xscale('log')
plt.yscale('log')
plt.savefig('wikipedia.png')

