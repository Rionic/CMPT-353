import numpy as np
data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

num_rows, num_cols = totals.shape

sums = np.sum(totals, 1)
print("Row with lowest total precipitation:")
print(np.argmin(sums))

print("Average precipitation in each month:")
print((np.sum(totals,0).astype(float))/(np.sum(counts,0).astype(float)))

print("Average precipitation in each city:")
print(np.sum(totals,1).astype(float)/np.sum(counts,1).astype(float))

a2 = np.reshape(totals,(4*num_rows,3))
a3 = np.sum(a2,1)
print("Quarterly precipitation totals:")
print(np.reshape(a3, (num_rows,4)))