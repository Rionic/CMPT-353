import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import sys

df = pd.read_csv('data.csv')

anova = stats.f_oneway(df.qs1, df.qs2, df.qs3, df.qs4, df.qs5, df.merge1, df.partition_sort)
melt = pd.melt(df)
print("anova p-value of", anova.pvalue, "means that there is a difference amongst")
print("the means of the algorithms and we can conduct a post-hoc analysis")
print()
posthoc = pairwise_tukeyhsd(melt['value'], melt['variable'], alpha=0.5)
print(posthoc)
fig = posthoc.plot_simultaneous()
print('qs1 mean running time:', df.qs1.mean())
print('qs2 mean running time:', df.qs2.mean())
print('qs3 mean running time:', df.qs3.mean())
print('qs4 mean running time:', df.qs4.mean())
print('qs5 mean running time:', df.qs5.mean())
print('merge1 mean running time:', df.merge1.mean())
print('partition_sort mean running time:', df.partition_sort.mean())
print()
print('All pairs have distinguishable different mean running times except pairs') 
print('(qs2, qs3), (qs4, qs5), (qs2, qs4), (qs2, qs5), (qs3, qs4), and (qs3, qs5)')
print('fastest algorithms in descending order are:')
print('partition_sort, qs1, qs4, qs3, qs2, qs5, merge1')
