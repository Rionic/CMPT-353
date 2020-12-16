import pandas as pd
import numpy as np
import time
from implementations import all_implementations

n_runs = 200
names = np.array(['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'])

data = np.zeros((n_runs, len(all_implementations)))

for runs in range(n_runs):
	r = np.random.rand(5000)
	for i, sort in enumerate(all_implementations):
	    st = time.time()
	    res = sort(r)
	    en = time.time()
	    data[runs,i] = en-st

df = pd.DataFrame(data, columns=names)
df.to_csv('data.csv', index=False)


